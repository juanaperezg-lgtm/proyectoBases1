from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.services import confederations_service


class ConfederationsView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.selected_id = None

        form = ttk.LabelFrame(self, text="Crear/Editar Confederación", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=40).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=1, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Confederaciones", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=300)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self.load_data()

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in confederations_service.list_confederations():
            self.tree.insert("", "end", values=(row["id_confederacion"], row["nombre"]))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "Ingresa el nombre de la confederación.")
            return

        try:
            if self.selected_id:
                confederations_service.update_confederation(self.selected_id, nombre)
                messagebox.showinfo("OK", "Confederación actualizada.")
            else:
                confederations_service.create_confederation(nombre)
                messagebox.showinfo("OK", "Confederación creada.")
            self._clear()
        except IntegrityError:
            messagebox.showerror("Error", "La confederación ya existe.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona una confederación.")
            return

        item = self.tree.item(selection[0], "values")
        conf_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar esta confederación?"):
            try:
                confederations_service.delete_confederation(conf_id)
                messagebox.showinfo("OK", "Confederación eliminada.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.selected_id = None
        self.load_data()
