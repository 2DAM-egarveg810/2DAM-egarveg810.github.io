#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import subprocess
import os
import sys
import re
from pathlib import Path

# === CONFIGURACIÓN ASTRAÏS ===
COMMIT_TYPES = [
    ("feat", "✨ Nueva funcionalidad"),
    ("fix", "🐛 Corrección de bug"),
    ("refactor", "♻️  Mejora de código"),
    ("perf", "⚡ Optimización"),
    ("docs", "📚 Documentación"),
    ("test", "✅ Tests"),
    ("chore", "🧹 Mantenimiento"),
    ("ci", "🚀 CI/CD"),
    ("style", "💄 Estilo"),
    ("revert", "⏪ Reversión")
]
SCOPES = ["auth", "tasks", "groups", "economy", "shop", "achievements", 
          "avatar", "pet", "minigames", "calendar", "android", "web", 
          "backend", "db", "docker", "other"]
MAX_SUBJECT = 72

class GitCommitHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Astraïs Git Helper: add → commit → push")
        self.root.geometry("780x680")
        self.root.resizable(False, False)
        self.repo_path = Path.cwd()
        self.validate_git_env()
        self.create_widgets()
        self.refresh_git_status()
    
    def validate_git_env(self):
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=5
            )
            if result.returncode != 0:
                raise Exception("No es un repositorio Git válido")
        except Exception as e:
            messagebox.showerror("❌ Error crítico", 
                f"No se detectó repositorio Git:\n{str(e)}\n\n"
                f"Ruta actual: {self.repo_path}\n\n"
                "Ejecuta el script desde la carpeta raíz de tu proyecto.")
            sys.exit(1)
    
    def refresh_git_status(self):
        """Obtiene estado actual de Git (staged/unstaged)"""
        try:
            # Archivos staged
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=3
            ).stdout.strip().splitlines()
            
            # Archivos unstaged (no ignorados)
            unstaged = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=3
            ).stdout.strip().splitlines()
            
            # Archivos nuevos no trackeados
            untracked = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=3
            ).stdout.strip().splitlines()
            
            self.staged_files = [f for f in staged if f]
            self.unstaged_files = [f for f in unstaged + untracked if f]
            self.current_branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=2
            ).stdout.strip() or "main"
            
            # Actualizar UI
            self.update_status_display()
            
        except Exception as e:
            self.status_var.set(f"⚠️ Error al obtener estado: {str(e)[:50]}")
            self.staged_files = []
            self.unstaged_files = []
            self.current_branch = "main"
    
    def update_status_display(self):
        # Limpiar área de estado
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Header de rama
        branch_label = tk.Label(
            self.status_frame, 
            text=f"🌿 Rama actual: {self.current_branch}",
            bg="#e3f2fd", fg="#1565c0", font=("Segoe UI", 10, "bold")
        )
        branch_label.pack(anchor="w", padx=10, pady=(5,0))
        
        # Archivos unstaged
        if self.unstaged_files:
            tk.Label(
                self.status_frame,
                text=f"🔴 {len(self.unstaged_files)} archivos sin stagear:",
                bg="#e3f2fd", fg="#d32f2f", font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=10, pady=(5,0))
            
            files_text = "\n".join(f"  • {f[:40]}..." if len(f) > 40 else f"  • {f}" 
                                 for f in self.unstaged_files[:5])
            if len(self.unstaged_files) > 5:
                files_text += f"\n  • ... y {len(self.unstaged_files)-5} más"
            
            tk.Label(
                self.status_frame,
                text=files_text,
                bg="#e3f2fd", fg="#546e7a", font=("Segoe UI", 8),
                justify="left", anchor="w"
            ).pack(anchor="w", padx=20, pady=(0,5))
            
            # Botón Stage all
            tk.Button(
                self.status_frame,
                text="➕ Stage all changes",
                command=self.stage_all_changes,
                bg="#1976d2", fg="white", font=("Segoe UI", 9, "bold"),
                padx=10, pady=3, relief="flat", cursor="hand2"
            ).pack(anchor="w", padx=20, pady=(0,10))
        else:
            tk.Label(
                self.status_frame,
                text="✅ Sin cambios sin stagear",
                bg="#e3f2fd", fg="#2e7d32", font=("Segoe UI", 9)
            ).pack(anchor="w", padx=10, pady=5)
        
        # Archivos staged
        if self.staged_files:
            tk.Label(
                self.status_frame,
                text=f"🟢 {len(self.staged_files)} archivos staged:",
                bg="#e3f2fd", fg="#2e7d32", font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=10, pady=(5,0))
            
            files_text = "\n".join(f"  • {f[:40]}..." if len(f) > 40 else f"  • {f}" 
                                 for f in self.staged_files[:5])
            if len(self.staged_files) > 5:
                files_text += f"\n  • ... y {len(self.staged_files)-5} más"
            
            tk.Label(
                self.status_frame,
                text=files_text,
                bg="#e3f2fd", fg="#546e7a", font=("Segoe UI", 8),
                justify="left", anchor="w"
            ).pack(anchor="w", padx=20, pady=(0,5))
        else:
            tk.Label(
                self.status_frame,
                text="⚠️  No hay archivos staged (necesario para commit)",
                bg="#e3f2fd", fg="#ed6c02", font=("Segoe UI", 9)
            ).pack(anchor="w", padx=10, pady=5)
    
    def stage_all_changes(self):
        if not self.unstaged_files:
            messagebox.showinfo("ℹ️ Información", "No hay cambios para stagear")
            return
        
        # Confirmación inteligente
        msg = f"¿Stagear {len(self.unstaged_files)} archivos?\n\n"
        msg += "\n".join(f"  • {f}" for f in self.unstaged_files[:8])
        if len(self.unstaged_files) > 8:
            msg += f"\n  • ... y {len(self.unstaged_files)-8} más"
        
        if not messagebox.askyesno("➕ Stage changes", msg):
            return
        
        try:
            result = subprocess.run(
                ["git", "add", "."],
                capture_output=True, text=True, cwd=self.repo_path, timeout=10
            )
            if result.returncode == 0:
                messagebox.showinfo("✅ Éxito", f"Staged {len(self.unstaged_files)} archivos")
                self.refresh_git_status()
            else:
                raise Exception(result.stderr.strip() or "Error desconocido al stagear")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron stagear los cambios:\n{str(e)}")
    
    def create_widgets(self):
        # Frame de estado Git (arriba)
        self.status_frame = tk.Frame(self.root, bg="#e3f2fd", height=200)
        self.status_frame.pack(fill="x", padx=15, pady=10)
        self.status_frame.pack_propagate(False)
        
        # Separador
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=15, pady=5)
        
        # Formulario de commit (igual que antes pero ajustado)
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tipo
        tk.Label(main_frame, text="Tipo:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, 
                                 values=[f"{t[0]} - {t[1]}" for t in COMMIT_TYPES], 
                                 state="readonly", width=38)
        type_combo.grid(row=0, column=1, columnspan=2, sticky="w", pady=5)
        type_combo.current(0)
        
        # Ámbito
        tk.Label(main_frame, text="Ámbito:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.scope_var = tk.StringVar(value="tasks")
        scope_combo = ttk.Combobox(main_frame, textvariable=self.scope_var, 
                                  values=SCOPES, state="readonly", width=22)
        scope_combo.grid(row=1, column=1, sticky="w", pady=5)
        
        # Asunto
        tk.Label(main_frame, text=f"Asunto (≤{MAX_SUBJECT} chars):", 
                font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.subject_var = tk.StringVar()
        self.subject_var.trace("w", self.update_counter)
        tk.Entry(main_frame, textvariable=self.subject_var, width=48, 
                font=("Segoe UI", 10)).grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        self.counter_label = tk.Label(main_frame, text="0/72", fg="gray", 
                                    font=("Segoe UI", 9))
        self.counter_label.grid(row=2, column=3, padx=5, pady=5)
        
        # Cuerpo
        tk.Label(main_frame, text="Descripción (opcional):", 
                font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="nw", pady=5)
        self.body_text = scrolledtext.ScrolledText(main_frame, width=65, height=8, 
                                                 font=("Segoe UI", 9))
        self.body_text.grid(row=3, column=1, columnspan=3, pady=5)
        
        # Footer
        tk.Label(main_frame, text="Footer (ej: Closes #123):", 
                font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.footer_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.footer_var, width=50, 
                font=("Segoe UI", 10)).grid(row=4, column=1, columnspan=2, sticky="w", pady=5)
        
        # Botones principales
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=15)
        
        tk.Button(btn_frame, text="✨ COMMIT + PUSH", command=self.execute_full_flow, 
                 bg="#0288d1", fg="white", font=("Segoe UI", 11, "bold"), 
                 padx=25, pady=10, relief="flat", cursor="hand2", width=18).pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_frame, text="🔄 Refresh estado", command=self.refresh_git_status, 
                 bg="#6c757d", fg="white", font=("Segoe UI", 9), 
                 padx=15, pady=7, relief="flat").pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=self.root.quit, 
                 bg="#d32f2f", fg="white", font=("Segoe UI", 10), 
                 padx=20, pady=7, relief="flat").pack(side=tk.RIGHT, padx=8)
        
        # Mensaje de estado
        self.status_var = tk.StringVar(value="")
        tk.Label(main_frame, textvariable=self.status_var, fg="#d32f2f", 
                font=("Segoe UI", 9, "bold"), wraplength=700).grid(row=6, column=0, columnspan=4, pady=5)
        
        # Footer informativo
        tk.Label(main_frame, 
                text="💡 Flujo: 1) Stagea cambios → 2) Completa commit → 3) ¡Commit + Push automático!",
                fg="#546e7a", font=("Segoe UI", 8, "italic")).grid(row=7, column=0, columnspan=4, pady=(10,0))
    
    def update_counter(self, *args):
        count = len(self.subject_var.get())
        color = "red" if count > MAX_SUBJECT else "gray"
        self.counter_label.config(text=f"{count}/{MAX_SUBJECT}", fg=color)
    
    def execute_full_flow(self):
        # Validar staged files
        if not self.staged_files:
            if not self.unstaged_files:
                messagebox.showwarning("⚠️ Advertencia", "No hay cambios en el repositorio")
                return
            
            if not messagebox.askyesno("⚠️ Sin cambios staged", 
                "No hay archivos staged para commit.\n\n"
                "¿Stagear TODOS los cambios sin stagear y continuar?"):
                return
            
            self.stage_all_changes()
            if not self.staged_files:  # Verificar si funcionó
                return
        
        # Validar formulario
        if not self.type_var.get():
            self.status_var.set("❌ Selecciona un tipo de commit")
            return
        if not self.scope_var.get():
            self.status_var.set("❌ Selecciona un ámbito")
            return
        subject = self.subject_var.get().strip()
        if not subject:
            self.status_var.set("❌ El asunto no puede estar vacío")
            return
        if len(subject) > MAX_SUBJECT:
            if not messagebox.askyesno("⚠️ Advertencia", 
                f"El asunto excede {MAX_SUBJECT} caracteres ({len(subject)}).\n"
                "¿Forzar commit? (no recomendado para estándares)"):
                return
        
        # Confirmación final
        commit_type = self.type_var.get().split(" - ")[0]
        scope = self.scope_var.get().strip()
        summary = f"{commit_type}({scope}): {subject[:50]}{'...' if len(subject)>50 else ''}"
        
        if not messagebox.askyesno("✅ Confirmar operación", 
            f"Se ejecutará:\n"
            f"1. git commit -m \"{summary}\"\n"
            f"2. git push origin {self.current_branch}\n\n"
            f"¿Continuar?"):
            return
        
        # Ejecutar commit
        try:
            # Construir mensaje
            body = self.body_text.get("1.0", tk.END).strip()
            footer = self.footer_var.get().strip()
            lines = [f"{commit_type}({scope}): {subject}", ""]
            if body: lines.extend([body, ""])
            if footer: lines.append(footer)
            commit_msg = "\n".join(lines)
            
            # Ejecutar commit
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True, text=True, cwd=self.repo_path, timeout=15
            )
            
            if commit_result.returncode != 0:
                self.handle_git_error(commit_result, "commit")
                return
            
            commit_hash = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=5
            ).stdout.strip()
            
            # Ejecutar push
            self.status_var.set(f"⬆️ Haciendo push a origin/{self.current_branch}...")
            self.root.update()
            
            push_result = subprocess.run(
                ["git", "push", "origin", self.current_branch],
                capture_output=True, text=True, cwd=self.repo_path, timeout=30
            )
            
            if push_result.returncode != 0:
                self.handle_git_error(push_result, "push")
                return
            
            # Éxito total
            messagebox.showinfo("🎉 ¡Éxito total!", 
                f"✅ Commit creado: {commit_hash}\n"
                f"✅ Push completado a origin/{self.current_branch}\n\n"
                f"Mensaje: {summary}")
            self.root.quit()
            
        except subprocess.TimeoutExpired as e:
            op = "commit" if "commit" in str(e) else "push"
            messagebox.showerror("⏱️ Timeout", 
                f"Operación {op} tardó demasiado (>15s).\n"
                "Posible causa: hooks complejos, conexión lenta o muchos archivos.")
        except Exception as e:
            messagebox.showerror("💥 Error inesperado", 
                f"Tipo: {type(e).__name__}\nMensaje: {str(e)}")
    
    def handle_git_error(self, result, operation):
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        
        # Diagnóstico inteligente
        if "husky" in stderr.lower() or "pre-commit" in stderr.lower():
            hint = "💡 Hooks de pre-commit fallidos. Ejecuta manualmente:\ngit commit --no-verify"
        elif "rejected" in stderr.lower() and "non-fast-forward" in stderr.lower():
            hint = f"💡 ¡Tu rama está desactualizada!\nPrimero haz: git pull --rebase origin {self.current_branch}"
        elif "authentication" in stderr.lower() or "password" in stderr.lower() or "ssh" in stderr.lower():
            hint = "💡 Error de autenticación. Verifica:\n- SSH key configurada\n- Token de acceso para HTTPS"
        elif "nothing to commit" in stdout.lower():
            hint = "💡 No hay cambios para commitear (¿ya commiteaste?)"
        else:
            hint = f"stderr:\n{stderr[:400]}"
        
        messagebox.showerror(f"❌ Error en {operation}", 
            f"Código: {result.returncode}\n\n{hint}")
        self.status_var.set(f"❌ Falló {operation} - revisa mensajes anteriores")

if __name__ == "__main__":
    try:
        # Verificar Tkinter
        import tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana temporal
        root.update()
        root.destroy()
        
        # Ejecutar app
        root = tk.Tk()
        app = GitCommitHelper(root)
        root.mainloop()
        
    except ModuleNotFoundError as e:
        if "tkinter" in str(e).lower():
            print("❌ ERROR: Tkinter no está instalado")
            print("\nSolución según tu sistema:")
            print("  • Ubuntu/Debian: sudo apt install python3-tk")
            print("  • macOS: brew install python-tk")
            print("  • Windows: Reinstala Python y marca 'tcl/tk and IDLE' en el instalador")
            print("\nAlternativa rápida (terminal):")
            print("  git add .")
            print('  git commit -m "feat(auth): ejemplo"')
            print("  git push")
        else:
            raise
    except Exception as e:
        print(f"❌ Error crítico: {type(e).__name__}: {str(e)}")
        sys.exit(1)