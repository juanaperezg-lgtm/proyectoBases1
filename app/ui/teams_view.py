from tkinter import StringVar, messagebox, ttk

from mysql.connector.errors import IntegrityError

from app.controllers import teams_service, countries_service, confederations_service


class TeamsView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        self.nombre_var = StringVar()
        self.pais_var = StringVar()
        self.confederacion_var = StringVar()
        self.valor_var = StringVar()
        self.selected_id = None
        self.paises_dict = {}
        self.confederaciones_dict = {}

        form = ttk.LabelFrame(self, text="Crear/Editar Equipo", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nombre_var, width=25).grid(row=1, column=0, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="País").grid(row=0, column=1, sticky="w")
        self.pais_combo = ttk.Combobox(form, textvariable=self.pais_var, state="readonly", width=18)
        self.pais_combo.grid(row=1, column=1, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Confederación").grid(row=0, column=2, sticky="w")
        self.conf_combo = ttk.Combobox(form, textvariable=self.confederacion_var, state="readonly", width=18)
        self.conf_combo.grid(row=1, column=2, padx=(0, 10), pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Valor Mercado").grid(row=0, column=3, sticky="w")
        ttk.Entry(form, textvariable=self.valor_var, width=18).grid(row=1, column=3, padx=(0, 10), pady=(0, 8))

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=4, sticky="ew")
        ttk.Button(btn_frame, text="Guardar", command=self._save).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Nuevo", command=self._clear).pack(side="left")

        form.columnconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(self, text="Equipos", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "pais", "confederacion", "valor"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Equipo")
        self.tree.heading("pais", text="País")
        self.tree.heading("confederacion", text="Confederación")
        self.tree.heading("valor", text="Valor Mercado")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=150)
        self.tree.column("pais", width=100)
        self.tree.column("confederacion", width=120)
        self.tree.column("valor", width=120, anchor="e")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_select)

        actions = ttk.Frame(list_frame)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Eliminar", command=self._delete).pack(side="left")
        ttk.Button(actions, text="Refrescar", command=self.load_data).pack(side="right")

        self._load_data_sources()
        self.load_data()

    def _load_data_sources(self) -> None:
        self.paises_dict = {}
        paises_list = []
        for pais in countries_service.list_countries():
            self.paises_dict[pais["nombre"]] = pais["id_pais"]
            paises_list.append(pais["nombre"])
        self.pais_combo["values"] = paises_list

        self.confederaciones_dict = {}
        confederaciones_list = []
        for conf in confederations_service.list_confederations():
            self.confederaciones_dict[conf["nombre"]] = conf["id_confederacion"]
            confederaciones_list.append(conf["nombre"])
        self.conf_combo["values"] = confederaciones_list

    def load_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in teams_service.list_teams():
            self.tree.insert("", "end", values=(
                row["id_equipo"],
                row["nombre"],
                row["pais"],
                row["confederacion"],
                f"${row['valor_mercado_total']:,.2f}"
            ))

    def _on_select(self, event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0], "values")
        self.selected_id = int(item[0])
        self.nombre_var.set(item[1])
        self.pais_var.set(item[2])
        self.confederacion_var.set(item[3])
        valor_clean = item[4].replace("$", "").replace(",", "")
        self.valor_var.set(valor_clean)

    def _save(self) -> None:
        nombre = self.nombre_var.get().strip()
        pais = self.pais_var.get().strip()
        confederacion = self.confederacion_var.get().strip()
        valor_str = self.valor_var.get().strip()

        if not all([nombre, pais, confederacion, valor_str]):
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        try:
            valor = float(valor_str)
            id_pais = self.paises_dict.get(pais)
            id_confederacion = self.confederaciones_dict.get(confederacion)

            if not id_pais or not id_confederacion:
                messagebox.showerror("Error", "País o confederación inválida.")
                return

            if self.selected_id:
                teams_service.update_team(self.selected_id, nombre, id_pais, id_confederacion, valor)
                messagebox.showinfo("OK", "Equipo actualizado.")
            else:
                teams_service.create_team(nombre, id_pais, id_confederacion, valor)
                messagebox.showinfo("OK", "Equipo creado.")
            self._clear()
        except ValueError:
            messagebox.showerror("Error", "El valor debe ser un número.")
        except IntegrityError:
            messagebox.showerror("Error", "El equipo ya existe.")

    def _delete(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un equipo.")
            return

        item = self.tree.item(selection[0], "values")
        team_id = int(item[0])

        if messagebox.askyesno("Confirmar", "¿Eliminar este equipo?"):
            try:
                teams_service.delete_team(team_id)
                messagebox.showinfo("OK", "Equipo eliminado.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")

    def _clear(self) -> None:
        self.nombre_var.set("")
        self.pais_var.set("")
        self.confederacion_var.set("")
        self.valor_var.set("")
        self.selected_id = None
        self.load_data()
