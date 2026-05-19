from tkinter import BooleanVar, StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.controllers import countries_service


class CountriesView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.es_anfitrion_var = BooleanVar(value=False)
        self.selected_id = None

        form = ttk.LabelFrame(self, text="Crear/Editar País", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=40).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="¿Es anfitrión?").grid(row=0, column=1, sticky="w", padx=(0, 10))
        ttk.Checkbutton(form, variable=self.es_anfitrion_var).grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 8))

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=2, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Países", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "anfitrion"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("anfitrion", text="Anfitrión")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("anfitrion", width=100, anchor="center")
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

        for row in countries_service.list_countries():
            anfitrion_text = "Sí" if row["es_anfitrion"] else "No"
            self.tree.insert("", "end", values=(row["id_pais"], row["nombre"], anfitrion_text))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        self.es_anfitrion_var.set(item[2] == "Sí")

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "Ingresa el nombre del país.")
            return

        try:
            es_anfitrion = self.es_anfitrion_var.get()
            if self.selected_id:
                countries_service.update_country(self.selected_id, nombre, es_anfitrion)
                messagebox.showinfo("OK", "País actualizado.")
            else:
                countries_service.create_country(nombre, es_anfitrion)
                messagebox.showinfo("OK", "País creado.")
            self._clear()
        except IntegrityError:
            messagebox.showerror("Error", "El país ya existe.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un país.")
            return

        item = self.tree.item(selection[0], "values")
        country_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este país?"):
            try:
                countries_service.delete_country(country_id)
                messagebox.showinfo("OK", "País eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.es_anfitrion_var.set(False)
        self.selected_id = None
        self.load_data()
