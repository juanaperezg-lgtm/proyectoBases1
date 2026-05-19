from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.controllers import cities_service, countries_service


class CitiesView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.pais_var = StringVar()
        self.selected_id = None
        self.paises_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Ciudad", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=30).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="País").grid(row=0, column=1, sticky="w")
        self.pais_combo = ttk.Combobox(form, textvariable=self.pais_var, state="readonly", width=25)
        self.pais_combo.grid(row=1, column=1, padx=(0, 10), pady=(0, 8), sticky="ew")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=2, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Ciudades", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "pais"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("pais", text="País")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("pais", width=200)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self._load_paises()
        self.load_data()

    def _load_paises(self) -> None:
        self.paises_dict = {}
        paises_list = []
        for pais in countries_service.list_countries():
            self.paises_dict[pais["nombre"]] = pais["id_pais"]
            paises_list.append(pais["nombre"])
        self.pais_combo["values"] = paises_list

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in cities_service.list_cities():
            self.tree.insert("", "end", values=(row["id_ciudad"], row["nombre"], row["pais"]))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        self.pais_var.set(item[2])

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        pais = self.pais_var.get().strip()
        if not nombre or not pais:
            messagebox.showwarning("Campos requeridos", "Ingresa nombre y país.")
            return

        try:
            id_pais = self.paises_dict.get(pais)
            if not id_pais:
                messagebox.showerror("Error", "País inválido.")
                return

            if self.selected_id:
                cities_service.update_city(self.selected_id, nombre, id_pais)
                messagebox.showinfo("OK", "Ciudad actualizada.")
            else:
                cities_service.create_city(nombre, id_pais)
                messagebox.showinfo("OK", "Ciudad creada.")
            self._clear()
        except IntegrityError:
            messagebox.showerror("Error", "La ciudad ya existe en ese país.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona una ciudad.")
            return

        item = self.tree.item(selection[0], "values")
        city_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar esta ciudad?"):
            try:
                cities_service.delete_city(city_id)
                messagebox.showinfo("OK", "Ciudad eliminada.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.pais_var.set("")
        self.selected_id = None
        self.load_data()
