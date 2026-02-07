#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import re

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

class CommitHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Astraïs Commit Helper")
        self.root.geometry("720x620")
        self.root.resizable(False, False)
        self.validate_git_env()  # Validación temprana
        self.create_widgets()
    
    def validate_git_env(self):
        # Verificar repositorio Git
        if subprocess.run(["git", "rev-parse", "--git-dir"], 
                         capture_output=True, text=True).returncode != 0:
            messagebox.showerror("❌ Error crítico", 
                "¡No estás en un repositorio Git!\n"
                "Ejecuta desde la carpeta raíz del proyecto.")
            sys.exit(1)
        
        # Verificar cambios staged
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip()
        
        if not staged:
            msg = ("⚠️  No hay cambios staged (git add)\n\n"
                   "¿Quieres continuar igual? (commit vacío no recomendado)")
            if not messagebox.askyesno("Advertencia", msg):
                sys.exit(0)
            self.has_staged = False
        else:
            self.has_staged = True
            self.staged_files = staged.splitlines()[:3]  # Mostrar primeros 3 archivos
    
    def create_widgets(self):
        # Header con estado de staged
        header = tk.Frame(self.root, bg="#f8f9fa", height=60)
        header.pack(fill="x", padx=15, pady=10)
        
        if self.has_staged:
            files_text = "✅ " + ", ".join(self.staged_files)
            if len(self.staged_files) < len(self.staged_files):
                files_text += f" (+{len(self.staged_files) - 3} más)"
            tk.Label(header, text=files_text, bg="#f8f9fa", fg="#28a745", 
                    font=("Segoe UI", 9, "bold")).pack(anchor="w")
        else:
            tk.Label(header, text="⚠️  Sin cambios staged", bg="#f8f9fa", 
                    fg="#ffc107", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        # Tipo
        tk.Label(self.root, text="Tipo:", font=("Segoe UI", 10, "bold")).place(x=20, y=70)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(self.root, textvariable=self.type_var, 
                                 values=[f"{t[0]} - {t[1]}" for t in COMMIT_TYPES], 
                                 state="readonly", width=38)
        type_combo.place(x=120, y=70)
        type_combo.current(0)
        
        # Ámbito
        tk.Label(self.root, text="Ámbito:", font=("Segoe UI", 10, "bold")).place(x=20, y=110)
        self.scope_var = tk.StringVar(value="tasks")
        scope_combo = ttk.Combobox(self.root, textvariable=self.scope_var, 
                                  values=SCOPES, state="readonly", width=22)
        scope_combo.place(x=120, y=110)
        
        # Asunto
        tk.Label(self.root, text=f"Asunto (≤{MAX_SUBJECT} chars):", 
                font=("Segoe UI", 10, "bold")).place(x=20, y=150)
        self.subject_var = tk.StringVar()
        self.subject_var.trace("w", self.update_counter)
        tk.Entry(self.root, textvariable=self.subject_var, width=48, 
                font=("Segoe UI", 10)).place(x=120, y=150)
        self.counter_label = tk.Label(self.root, text="0/72", fg="gray", 
                                    font=("Segoe UI", 9))
        self.counter_label.place(x=550, y=150)
        
        # Cuerpo
        tk.Label(self.root, text="Descripción (opcional):", 
                font=("Segoe UI", 10, "bold")).place(x=20, y=190)
        self.body_text = scrolledtext.ScrolledText(self.root, width=72, height=10, 
                                                 font=("Segoe UI", 9))
        self.body_text.place(x=20, y=215)
        
        # Footer
        tk.Label(self.root, text="Footer (ej: Closes #123):", 
                font=("Segoe UI", 10, "bold")).place(x=20, y=395)
        self.footer_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.footer_var, width=50, 
                font=("Segoe UI", 10)).place(x=180, y=395)
        
        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.place(x=20, y=440, width=680)
        
        tk.Button(btn_frame, text="✨ COMMIT", command=self.execute_commit, 
                 bg="#4361ee", fg="white", font=("Segoe UI", 11, "bold"), 
                 padx=30, pady=10, relief="flat", cursor="hand2").pack(side=tk.LEFT, padx=15)
        
        tk.Button(btn_frame, text="❓ Diagnóstico Git", command=self.show_git_status, 
                 bg="#6c757d", fg="white", font=("Segoe UI", 9), 
                 padx=15, pady=8, relief="flat").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=self.root.quit, 
                 bg="#e63946", fg="white", font=("Segoe UI", 10), 
                 padx=25, pady=8, relief="flat").pack(side=tk.RIGHT, padx=15)
        
        # Footer informativo
        tk.Label(self.root, 
                text="💡 Tip: Usa imperativo ('añadir login', no 'añadido login') | Formato: tipo(ámbito): asunto", 
                fg="#6c757d", font=("Segoe UI", 8)).place(x=20, y=500, width=680)
        
        # Mensaje de estado
        self.status_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status_var, fg="#e63946", 
                font=("Segoe UI", 9, "bold")).place(x=20, y=530, width=680)
    
    def update_counter(self, *args):
        count = len(self.subject_var.get())
        color = "red" if count > MAX_SUBJECT else "gray"
        self.counter_label.config(text=f"{count}/{MAX_SUBJECT}", fg=color)
    
    def show_git_status(self):
        try:
            status = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True, text=True, cwd=os.getcwd()
            ).stdout.strip() or "✓ Repositorio limpio (sin cambios)"
            
            messagebox.showinfo("🔍 Estado Git", 
                f"Archivos staged:\n{chr(10).join(self.staged_files) if self.has_staged else 'Ninguno'}\n\n"
                f"Todos los cambios:\n{status}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo obtener estado Git:\n{str(e)}")
    
    def execute_commit(self):
        # Validaciones
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
                "Git lo permitirá, pero rompe el estándar. ¿Continuar?"):
                return
        
        # Formatear mensaje
        commit_type = self.type_var.get().split(" - ")[0]
        scope = self.scope_var.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        footer = self.footer_var.get().strip()
        
        # Construir mensaje completo
        lines = [f"{commit_type}({scope}): {subject}", ""]
        if body:
            # Asegurar sangría de 72 chars para cuerpo
            for line in body.splitlines():
                lines.append(line)
            lines.append("")
        if footer:
            lines.append(footer)
        
        commit_msg = "\n".join(lines)
        
        # Diagnóstico previo si hay errores recurrentes
        if not self.has_staged:
            self.status_var.set("⚠️  Advertencia: Sin cambios staged (commit vacío)")
        
        # Ejecutar commit con captura completa de errores
        try:
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=10  # Evitar bloqueos
            )
            
            if result.returncode == 0:
                messagebox.showinfo("✅ ¡Éxito!", 
                    f"Commit creado:\n{commit_type}({scope}): {subject[:50]}...")
                self.root.quit()
            else:
                # Diagnóstico inteligente de errores comunes
                stderr = result.stderr.strip()
                if "husky" in stderr.lower() or "pre-commit" in stderr.lower():
                    hint = "\n\n💡 ¿Tienes hooks de pre-commit fallidos?\nEjecuta: git commit --no-verify"
                elif "empty" in stderr.lower() or "nothing" in stderr.lower():
                    hint = "\n\n💡 No hay cambios staged. Ejecuta primero:\ngit add ."
                elif "name" in stderr.lower() or "email" in stderr.lower():
                    hint = "\n\n💡 Configura tu identidad Git:\ngit config --global user.name 'Tu Nombre'\ngit config --global user.email 'tu@email.com'"
                else:
                    hint = f"\n\nstderr completo:\n{stderr[:500]}"
                
                messagebox.showerror("❌ Error Git", 
                    f"Código: {result.returncode}\n\n{stderr[:300]}{hint}")
                self.status_var.set("❌ Commit fallido - revisa consola para detalles")
                
        except subprocess.TimeoutExpired:
            messagebox.showerror("⏱️  Timeout", 
                "El commit tardó demasiado (>10s).\n¿Tienes hooks complejos o muchos archivos?")
        except Exception as e:
            messagebox.showerror("💥 Excepción", f"Error inesperado:\n{type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CommitHelper(root)
        root.mainloop()
    except ModuleNotFoundError as e:
        if "tkinter" in str(e).lower():
            print("❌ ERROR: Tkinter no está instalado")
            print("\nSolución para tu sistema:")
            print("  • Ubuntu/Debian: sudo apt install python3-tk")
            print("  • macOS: brew install python-tk")
            print("  • Windows: Reinstala Python y marca 'tcl/tk and IDLE' en el instalador")
            print("\nAlternativa rápida (sin GUI):")
            print("  git commit -m \"feat(auth): ejemplo\"")
        else:
            raise
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {str(e)}")
        sys.exit(1)