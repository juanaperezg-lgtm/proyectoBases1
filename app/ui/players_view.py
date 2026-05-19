from tkinter import StringVar, messagebox, ttk

from app.controllers import players_service, teams_service


class PlayersView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.posicion_var = StringVar()
        self.fecha_nac_var = StringVar()
        self.estatura_var = StringVar()
        self.peso_var = StringVar()
        self.valor_var = StringVar()
        self.equipo_var = StringVar()
        self.selected_id = None
        self.equipos_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Jugador", padding=10)
        form.pack(fill="x")

        row1 = ttk.Frame(form)
        row1.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(0, 8))
        ttk.Label(row1, text="Nombre Completo:").pack(side="left")
        ttk.Entry(row1, textvariable=self.nombre_var, width=30).pack(side="left", padx=(5, 15))
        
        ttk.Label(row1, text="Posición:").pack(side="left")
        ttk.Entry(row1, textvariable=self.posicion_var, width=15).pack(side="left", padx=(5, 0))

        row2 = ttk.Frame(form)
        row2.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 8))
        ttk.Label(row2, text="Fecha Nacimiento (YYYY-MM-DD):").pack(side="left")
        ttk.Entry(row2, textvariable=self.fecha_nac_var, width=18).pack(side="left", padx=(5, 15))
        
        ttk.Label(row2, text="Estatura (m):").pack(side="left")
        ttk.Entry(row2, textvariable=self.estatura_var, width=10).pack(side="left", padx=(5, 15))
        
        ttk.Label(row2, text="Peso (kg):").pack(side="left")
        ttk.Entry(row2, textvariable=self.peso_var, width=10).pack(side="left", padx=(5, 0))

        row3 = ttk.Frame(form)
        row3.grid(row=2, column=0, columnspan=6, sticky="ew", pady=(0, 8))
        ttk.Label(row3, text="Valor Mercado:").pack(side="left")
        ttk.Entry(row3, textvariable=self.valor_var, width=15).pack(side="left", padx=(5, 15))
        
        ttk.Label(row3, text="Equipo:").pack(side="left")
        self.equipo_combo = ttk.Combobox(row3, textvariable=self.equipo_var, state="readonly", width=25)
        self.equipo_combo.pack(side="left", padx=(5, 15))

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=3, column=0, columnspan=6, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        list_frame = ttk.LabelFrame(self, text="Jugadores", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "posicion", "fecha_nac", "estatura", "peso", "valor", "equipo"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Jugador")
        self.tree.heading("posicion", text="Posición")
        self.tree.heading("fecha_nac", text="F. Nac")
        self.tree.heading("estatura", text="Est(m)")
        self.tree.heading("peso", text="Peso(kg)")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("equipo", text="Equipo")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=140)
        self.tree.column("posicion", width=70)
        self.tree.column("fecha_nac", width=80)
        self.tree.column("estatura", width=60, anchor="center")
        self.tree.column("peso", width=60, anchor="center")
        self.tree.column("valor", width=100, anchor="e")
        self.tree.column("equipo", width=120)
        
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

        for row in players_service.list_players():
            self.tree.insert("", "end", values=(
                row["id_jugador"],
                row["nombre_completo"],
                row["posicion"],
                str(row["fecha_nacimiento"]),
                f"{row['estatura_m']:.2f}",
                f"{row['peso_kg']:.2f}",
                f"${row['valor_mercado']:,.2f}",
                row["equipo"]
            ))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        self.posicion_var.set(item[2])
        self.fecha_nac_var.set(item[3])
        self.estatura_var.set(item[4])
        self.peso_var.set(item[5])
        valor_clean = item[6].replace("$", "").replace(",", "")
        self.valor_var.set(valor_clean)
        self.equipo_var.set(item[7])

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        posicion = self.posicion_var.get().strip()
        fecha_nac = self.fecha_nac_var.get().strip()
        estatura_str = self.estatura_var.get().strip()
        peso_str = self.peso_var.get().strip()
        valor_str = self.valor_var.get().strip()
        equipo = self.equipo_var.get().strip()

        if not all([nombre, posicion, fecha_nac, estatura_str, peso_str, valor_str, equipo]):
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        try:
            estatura = float(estatura_str)
            peso = float(peso_str)
            valor = float(valor_str)
            id_equipo = self.equipos_dict.get(equipo)
            if not id_equipo:
                messagebox.showerror("Error", "Equipo inválido.")
                return

            if self.selected_id:
                players_service.update_player(self.selected_id, nombre, posicion, fecha_nac,
                                             estatura, peso, valor, id_equipo)
                messagebox.showinfo("OK", "Jugador actualizado.")
            else:
                players_service.create_player(nombre, posicion, fecha_nac,
                                             estatura, peso, valor, id_equipo)
                messagebox.showinfo("OK", "Jugador creado.")
            self._clear()
        except ValueError:
            messagebox.showerror("Error", "Verifica que estatura, peso y valor sean números válidos.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un jugador.")
            return

        item = self.tree.item(selection[0], "values")
        player_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este jugador?"):
            try:
                players_service.delete_player(player_id)
                messagebox.showinfo("OK", "Jugador eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.posicion_var.set("")
        self.fecha_nac_var.set("")
        self.estatura_var.set("")
        self.peso_var.set("")
        self.valor_var.set("")
        self.equipo_var.set("")
        self.selected_id = None
        self.load_data()
