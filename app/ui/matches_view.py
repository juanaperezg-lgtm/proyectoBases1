from tkinter import StringVar, messagebox, ttk

from app.controllers import matches_service, groups_service, stadiums_service, teams_service


class MatchesView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.grupo_var = StringVar()
        self.estadio_var = StringVar()
        self.equipo_local_var = StringVar()
        self.equipo_visitante_var = StringVar()
        self.fecha_hora_var = StringVar()
        self.selected_id = None
        self.grupos_dict = {}
        self.estadios_dict = {}
        self.equipos_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Partido", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Grupo").grid(row=0, column=0, sticky="w")
        self.grupo_combo = ttk.Combobox(form, textvariable=self.grupo_var, state="readonly", width=15)
        self.grupo_combo.grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")
        self.grupo_combo.bind("<<ComboboxSelected>>", self._on_group_changed)

        ttk.Label(form, text="Estadio").grid(row=0, column=1, sticky="w")
        self.estadio_combo = ttk.Combobox(form, textvariable=self.estadio_var, state="readonly", width=20)
        self.estadio_combo.grid(row=1, column=1, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Equipo Local").grid(row=0, column=2, sticky="w")
        self.local_combo = ttk.Combobox(form, textvariable=self.equipo_local_var, state="readonly", width=18)
        self.local_combo.grid(row=1, column=2, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Equipo Visitante").grid(row=0, column=3, sticky="w")
        self.visitante_combo = ttk.Combobox(form, textvariable=self.equipo_visitante_var, state="readonly", width=18)
        self.visitante_combo.grid(row=1, column=3, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Fecha/Hora (YYYY-MM-DD HH:MM)").grid(row=0, column=4, sticky="w")
        ttk.Entry(form, textvariable=self.fecha_hora_var, width=22).grid(row=1, column=4, padx=(0, 10), pady=(0, 8))

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=5, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        for i in range(6):
            form.columnconfigure(i, weight=1)

        list_frame = ttk.LabelFrame(self, text="Partidos", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "grupo", "local", "visitante", "estadio", "fecha_hora"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("grupo", text="Grupo")
        self.tree.heading("local", text="Equipo Local")
        self.tree.heading("visitante", text="Equipo Visitante")
        self.tree.heading("estadio", text="Estadio")
        self.tree.heading("fecha_hora", text="Fecha/Hora")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("grupo", width=60, anchor="center")
        self.tree.column("local", width=140)
        self.tree.column("visitante", width=140)
        self.tree.column("estadio", width=150)
        self.tree.column("fecha_hora", width=150)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self._load_data_sources()
        self.load_data()

    def _load_data_sources(self) -> None:
        self.grupos_dict = {}
        grupos_list = []
        for grupo in groups_service.list_groups():
            self.grupos_dict[grupo["nombre"]] = grupo["id_grupo"]
            grupos_list.append(grupo["nombre"])
        self.grupo_combo["values"] = grupos_list

        self.estadios_dict = {}
        estadios_list = []
        for estadio in stadiums_service.list_stadiums():
            label = f"{estadio['nombre']} ({estadio['ciudad']})"
            self.estadios_dict[label] = estadio["id_estadio"]
            estadios_list.append(label)
        self.estadio_combo["values"] = estadios_list

        self.equipos_dict = {}
        equipos_list = []
        for equipo in teams_service.list_teams():
            self.equipos_dict[equipo["nombre"]] = equipo["id_equipo"]
            equipos_list.append(equipo["nombre"])
        self.local_combo["values"] = equipos_list
        self.visitante_combo["values"] = equipos_list

    def _on_group_changed(self, event) -> None:
        grupo_name = self.grupo_var.get()
        if grupo_name:
            equipos_en_grupo = groups_service.list_group_teams(self.grupos_dict.get(grupo_name))
            equipos_names = [e["nombre"] for e in equipos_en_grupo]
            self.local_combo["values"] = equipos_names
            self.visitante_combo["values"] = equipos_names

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in matches_service.list_matches():
            self.tree.insert("", "end", values=(
                row["id_partido"],
                row["grupo"],
                row["equipo_local"],
                row["equipo_visitante"],
                row["estadio"],
                row["fecha_hora"]
            ))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.grupo_var.set(item[1])
        self.equipo_local_var.set(item[2])
        self.equipo_visitante_var.set(item[3])
        
        estadio_text = None
        for estadio in stadiums_service.list_stadiums():
            if estadio["nombre"] == item[4]:
                estadio_text = f"{estadio['nombre']} ({estadio['ciudad']})"
                break
        if estadio_text:
            self.estadio_var.set(estadio_text)
        
        self.fecha_hora_var.set(str(item[5]))

    def _save(self) -> None:
        grupo = self.grupo_var.get().strip()
        estadio_label = self.estadio_var.get().strip()
        equipo_local = self.equipo_local_var.get().strip()
        equipo_visitante = self.equipo_visitante_var.get().strip()
        fecha_hora = self.fecha_hora_var.get().strip()

        if not all([grupo, estadio_label, equipo_local, equipo_visitante, fecha_hora]):
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        if equipo_local == equipo_visitante:
            messagebox.showerror("Error", "Los equipos local y visitante no pueden ser iguales.")
            return

        try:
            id_grupo = self.grupos_dict.get(grupo)
            id_estadio = self.estadios_dict.get(estadio_label)
            id_local = self.equipos_dict.get(equipo_local)
            id_visitante = self.equipos_dict.get(equipo_visitante)

            if not all([id_grupo, id_estadio, id_local, id_visitante]):
                messagebox.showerror("Error", "Selecciones inválidas.")
                return

            if self.selected_id:
                matches_service.update_match(self.selected_id, id_grupo, id_estadio, id_local, id_visitante, fecha_hora)
                messagebox.showinfo("OK", "Partido actualizado.")
            else:
                matches_service.create_match(id_grupo, id_estadio, id_local, id_visitante, fecha_hora)
                messagebox.showinfo("OK", "Partido creado.")
            self._clear()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un partido.")
            return

        item = self.tree.item(selection[0], "values")
        match_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este partido?"):
            try:
                matches_service.delete_match(match_id)
                messagebox.showinfo("OK", "Partido eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.grupo_var.set("")
        self.estadio_var.set("")
        self.equipo_local_var.set("")
        self.equipo_visitante_var.set("")
        self.fecha_hora_var.set("")
        self.selected_id = None
        self.load_data()
