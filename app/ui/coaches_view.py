from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.services import coaches_service, teams_service


class CoachesView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.nacionalidad_var = StringVar()
        self.edad_var = StringVar()
        self.equipo_var = StringVar()
        self.selected_id = None
        self.equipos_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Director Técnico", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre Completo").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=25).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Nacionalidad").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.nacionalidad_var, width=20).grid(row=1, column=1, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Edad").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.edad_var, width=10).grid(row=1, column=2, padx=(0, 10), pady=(0, 8))

        ttk.Label(form, text="Equipo").grid(row=0, column=3, sticky="w")
        self.equipo_combo = ttk.Combobox(form, textvariable=self.equipo_var, state="readonly", width=20)
        self.equipo_combo.grid(row=1, column=3, padx=(0, 10), pady=(0, 8), sticky="ew")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=4, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Directores Técnicos", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "nacionalidad", "edad", "equipo"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("nacionalidad", text="Nacionalidad")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("equipo", text="Equipo")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=160)
        self.tree.column("nacionalidad", width=120)
        self.tree.column("edad", width=60, anchor="center")
        self.tree.column("equipo", width=160)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self._load_equipos()
        self.load_data()

    def _load_equipos(self) -> None:
        self.equipos_dict = {}
        equipos_list = []
        for equipo in teams_service.list_teams():
            self.equipos_dict[equipo["nombre"]] = equipo["id_equipo"]
            equipos_list.append(equipo["nombre"])
        self.equipo_combo["values"] = equipos_list

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in coaches_service.list_coaches():
            self.tree.insert("", "end", values=(
                row["id_dt"],
                row["nombre_completo"],
                row["nacionalidad"],
                row["edad"],
                row["equipo"]
            ))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        self.nacionalidad_var.set(item[2])
        self.edad_var.set(item[3])
        self.equipo_var.set(item[4])

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        nacionalidad = self.nacionalidad_var.get().strip()
        edad_str = self.edad_var.get().strip()
        equipo = self.equipo_var.get().strip()

        if not all([nombre, nacionalidad, edad_str, equipo]):
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        try:
            edad = int(edad_str)
            id_equipo = self.equipos_dict.get(equipo)
            if not id_equipo:
                messagebox.showerror("Error", "Equipo inválido.")
                return

            if self.selected_id:
                coaches_service.update_coach(self.selected_id, nombre, nacionalidad, edad, id_equipo)
                messagebox.showinfo("OK", "Director técnico actualizado.")
            else:
                coaches_service.create_coach(nombre, nacionalidad, edad, id_equipo)
                messagebox.showinfo("OK", "Director técnico creado.")
            self._clear()
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número.")
        except IntegrityError:
            messagebox.showerror("Error", "El equipo ya tiene un director técnico asignado.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un director técnico.")
            return

        item = self.tree.item(selection[0], "values")
        coach_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este director técnico?"):
            try:
                coaches_service.delete_coach(coach_id)
                messagebox.showinfo("OK", "Director técnico eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.nacionalidad_var.set("")
        self.edad_var.set("")
        self.equipo_var.set("")
        self.selected_id = None
        self.load_data()
