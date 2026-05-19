from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.controllers import user_service


class UsersView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.username_var = StringVar()
        self.nombre_var = StringVar()
        self.password_var = StringVar()
        self.tipo_var = StringVar(value="TRADICIONAL")

        form = ttk.LabelFrame(self, text="Crear usuario", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Usuario").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.username_var, width=20).grid(row=1, column=0, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Nombre completo").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=30).grid(row=1, column=1, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Contraseña").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.password_var, width=20, show="*").grid(row=1, column=2, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Tipo").grid(row=0, column=3, sticky="w")
        ttk.Combobox(
            form,
            textvariable=self.tipo_var,
            values=["TRADICIONAL", "ESPORADICO"],
            state="readonly",
            width=14,
        ).grid(row=1, column=3, padx=(0, 10), pady=(0, 8))

        ttk.Button(form, text="Guardar", command=self._create_user).grid(row=1, column=4, sticky="ew")

        list_frame = ttk.LabelFrame(self, text="Usuarios", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "username", "nombre", "tipo", "activo"),
            show="headings",
            height=10,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Usuario")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("activo", text="Activo")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("username", width=120)
        self.tree.column("nombre", width=220)
        self.tree.column("tipo", width=120, anchor="center")
        self.tree.column("activo", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Activar", command=lambda: self._set_status(True)).pack(side="left")
        ttk.Button(actions, text="Desactivar", command=lambda: self._set_status(False)).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self.load_data()

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in user_service.list_users():
            self.tree.insert(
                "",
                "end",
                values=(
                    row["id_usuario"],
                    row["username"],
                    row["nombre_completo"],
                    row["tipo_usuario"],
                    "Sí" if row["activo"] else "No",
                ),
            )

    def _create_user(self) -> None:
        username = self.username_var.get().strip()
        nombre = self.nombre_var.get().strip()
        password = self.password_var.get()
        tipo = self.tipo_var.get()
        if not username or not nombre or not password:
            messagebox.showwarning("Campos requeridos", "Completa usuario, nombre y contraseña.")
            return
        try:
            user_service.create_user(username, nombre, password, tipo)
        except IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return
        messagebox.showinfo("OK", "Usuario creado.")
        self.username_var.set("")
        self.nombre_var.set("")
        self.password_var.set("")
        self.tipo_var.set("TRADICIONAL")
        self.load_data()

    def _set_status(self, active: bool) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un usuario.")
            return
        item = self.tree.item(selection[0], "values")
        user_id = int(item[0])
        user_service.update_user_status(user_id, active)
        self.load_data()
