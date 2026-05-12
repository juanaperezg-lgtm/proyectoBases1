from tkinter import StringVar, messagebox, ttk

from app.services import groups_service, teams_service


class GroupsView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.selected_group_id = None
        self.equipos_dict = {}

        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(top_frame, text="Selecciona Grupo:").pack(side="left", padx=(0, 10))
        self.grupo_var = StringVar()
        self.grupo_combo = ttk.Combobox(top_frame, textvariable=self.grupo_var, state="readonly", width=20)
        self.grupo_combo.pack(side="left", padx=(0, 20))
        self.grupo_combo.bind("<<ComboboxSelected>>", self._on_group_selected)

        left_frame = ttk.LabelFrame(self, text="Equipos en el Grupo", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.group_tree = ttk.Treeview(
            left_frame,
            columns=("id", "nombre", "confederacion"),
            show="headings",
            height=15,
        )
        self.group_tree.heading("id", text="ID")
        self.group_tree.heading("nombre", text="Equipo")
        self.group_tree.heading("confederacion", text="Confederación")
        self.group_tree.column("id", width=50, anchor="center")
        self.group_tree.column("nombre", width=150)
        self.group_tree.column("confederacion", width=120)
        self.group_tree.pack(fill="both", expand=True)

        group_actions = ttk.Frame(left_frame)
        group_actions.pack(fill="x", pady=(8, 0))
        ttk.Button(group_actions, text="Remover Equipo", command=self._remove_team).pack(side="left")

        right_frame = ttk.LabelFrame(self, text="Equipos Disponibles", padding=10)
        right_frame.pack(side="right", fill="both", expand=True)

        self.available_tree = ttk.Treeview(
            right_frame,
            columns=("id", "nombre", "confederacion"),
            show="headings",
            height=15,
        )
        self.available_tree.heading("id", text="ID")
        self.available_tree.heading("nombre", text="Equipo")
        self.available_tree.heading("confederacion", text="Confederación")
        self.available_tree.column("id", width=50, anchor="center")
        self.available_tree.column("nombre", width=150)
        self.available_tree.column("confederacion", width=120)
        self.available_tree.pack(fill="both", expand=True)

        available_actions = ttk.Frame(right_frame)
        available_actions.pack(fill="x", pady=(8, 0))
        ttk.Button(available_actions, text="Agregar Equipo", command=self._add_team).pack(side="left")
        ttk.Button(available_actions, text="Refrescar", command=self._refresh_lists).pack(side="right")

        self._load_groups()

    def _load_groups(self) -> None:
        grupos = groups_service.list_groups()
        grupos_list = [f"{g['nombre']}" for g in grupos]
        self.grupo_combo["values"] = grupos_list
        if grupos_list:
            self.grupo_combo.current(0)
            self._on_group_selected(None)

    def _on_group_selected(self, event) -> None:
        grupo_nombre = self.grupo_var.get()
        if not grupo_nombre:
            return
        
        grupos = groups_service.list_groups()
        for g in grupos:
            if str(g["nombre"]) == grupo_nombre:
                self.selected_group_id = g["id_grupo"]
                break
        
        self._refresh_lists()

    def _refresh_lists(self) -> None:
        if not self.selected_group_id:
            messagebox.showwarning("Error", "Selecciona un grupo.")
            return

        for item in self.group_tree.get_children():
            self.group_tree.delete(item)
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)

        for row in groups_service.list_group_teams(self.selected_group_id):
            self.group_tree.insert("", "end", values=(
                row["id_equipo"],
                row["nombre"],
                row["confederacion"]
            ))

        for row in groups_service.list_available_teams(self.selected_group_id):
            self.available_tree.insert("", "end", values=(
                row["id_equipo"],
                row["nombre"],
                row["confederacion"]
            ))

    def _add_team(self) -> None:
        if not self.selected_group_id:
            messagebox.showwarning("Error", "Selecciona un grupo.")
            return

        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un equipo de la lista disponible.")
            return

        item = self.available_tree.item(selection[0], "values")
        team_id = int(item[0])

        try:
            groups_service.add_team_to_group(self.selected_group_id, team_id)
            messagebox.showinfo("OK", "Equipo agregado al grupo.")
            self._refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", f"No se puede agregar: {str(e)}")

    def _remove_team(self) -> None:
        if not self.selected_group_id:
            messagebox.showwarning("Error", "Selecciona un grupo.")
            return

        selection = self.group_tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un equipo del grupo.")
            return

        item = self.group_tree.item(selection[0], "values")
        team_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Remover este equipo del grupo?"):
            try:
                groups_service.remove_team_from_group(self.selected_group_id, team_id)
                messagebox.showinfo("OK", "Equipo removido del grupo.")
                self._refresh_lists()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede remover: {str(e)}")
