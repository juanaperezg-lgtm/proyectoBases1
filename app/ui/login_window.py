from tkinter import StringVar, Tk, Toplevel, messagebox, ttk

from app.config import APP_TITLE
from app.services.auth_service import authenticate
from app.ui.main_window import MainWindow


class LoginWindow:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title(f"{APP_TITLE} - Login")
        self.root.geometry("420x220")
        self.root.resizable(False, False)

        self.username_var = StringVar()
        self.password_var = StringVar()

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Usuario").grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(frame, textvariable=self.username_var, width=35).grid(row=1, column=0, sticky="ew", pady=(0, 12))

        ttk.Label(frame, text="Contraseña").grid(row=2, column=0, sticky="w", pady=(0, 8))
        password_entry = ttk.Entry(frame, textvariable=self.password_var, show="*", width=35)
        password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 16))

        ttk.Button(frame, text="Iniciar sesión", command=self._login).grid(row=4, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        password_entry.bind("<Return>", lambda _: self._login())

    def _login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning("Campos requeridos", "Debes ingresar usuario y contraseña.")
            return

        user, bitacora_id = authenticate(username, password)
        if not user:
            messagebox.showerror("Acceso denegado", "Credenciales inválidas o usuario inactivo.")
            return

        self.root.withdraw()
        MainWindow(Toplevel(self.root), user, bitacora_id, self._on_main_closed)

    def _on_main_closed(self) -> None:
        self.password_var.set("")
        self.root.deiconify()
