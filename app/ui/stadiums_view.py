from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.services import stadiums_service, cities_service


class StadiumsView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.capacidad_var = StringVar()
        self.ciudad_var = StringVar()
        self.selected_id = None
        self.ciudades_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Estadio", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=30).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Capacidad").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.capacidad_var, width=15).grid(row=1, column=1, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Ciudad").grid(row=0, column=2, sticky="w")
        self.ciudad_combo = ttk.Combobox(form, textvariable=self.ciudad_var, state="readonly", width=20)
        self.ciudad_combo.grid(row=1, column=2, padx=(0, 10), pady=(0, 8), sticky="ew")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=3, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Estadios", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "ciudad", "capacidad"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("ciudad", text="Ciudad")
        self.tree.heading("capacidad", text="Capacidad")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=220)
        self.tree.column("ciudad", width=150)
        self.tree.column("capacidad", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self._load_ciudades()
        self.load_data()

    def _load_ciudades(self) -> None:
        self.ciudades_dict = {}
        ciudades_list = []
        for ciudad in cities_service.list_cities():
            label = f"{ciudad['nombre']} ({ciudad['pais']})"
            self.ciudades_dict[label] = ciudad["id_ciudad"]
            ciudades_list.append(label)
        self.ciudad_combo["values"] = ciudades_list

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in stadiums_service.list_stadiums():
            self.tree.insert("", "end", values=(row["id_estadio"], row["nombre"], row["ciudad"], row["capacidad"]))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        
        ciudad_text = None
        for ciudad in cities_service.list_cities():
            if ciudad["nombre"] == item[2]:
                ciudad_text = f"{ciudad['nombre']} ({ciudad['pais']})"
                break
        
        if ciudad_text:
            self.ciudad_var.set(ciudad_text)
        self.capacidad_var.set(item[3])

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        capacidad_str = self.capacidad_var.get().strip()
        ciudad_label = self.ciudad_var.get().strip()

        if not nombre or not capacidad_str or not ciudad_label:
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        try:
            capacidad = int(capacidad_str)
            id_ciudad = self.ciudades_dict.get(ciudad_label)
            if not id_ciudad:
                messagebox.showerror("Error", "Ciudad inválida.")
                return

            if self.selected_id:
                stadiums_service.update_stadium(self.selected_id, nombre, capacidad, id_ciudad)
                messagebox.showinfo("OK", "Estadio actualizado.")
            else:
                stadiums_service.create_stadium(nombre, capacidad, id_ciudad)
                messagebox.showinfo("OK", "Estadio creado.")
            self._clear()
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número.")
        except IntegrityError:
            messagebox.showerror("Error", "El estadio ya existe en esa ciudad.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un estadio.")
            return

        item = self.tree.item(selection[0], "values")
        stadium_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este estadio?"):
            try:
                stadiums_service.delete_stadium(stadium_id)
                messagebox.showinfo("OK", "Estadio eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.capacidad_var.set("")
        self.ciudad_var.set("")
        self.selected_id = None
        self.load_data()
