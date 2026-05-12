from tkinter import messagebox, ttk
from app.database.connection import get_connection


class QueriesView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        query_notebook = ttk.Notebook(self)
        query_notebook.pack(fill="both", expand=True)

        query_notebook.add(self._build_most_expensive_player(), text="Jugador Más Caro")
        query_notebook.add(self._build_matches_by_stadium(), text="Partidos por Estadio")
        query_notebook.add(self._build_most_expensive_team(), text="Equipo Más Caro")
        query_notebook.add(self._build_players_under_21(), text="Jugadores <21 años")

    def _build_most_expensive_player(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Jugador más costoso por confederación", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        self.tree_expensive = ttk.Treeview(
            frame,
            columns=("confederacion", "jugador", "equipo", "valor"),
            show="headings",
            height=15,
        )
        self.tree_expensive.heading("confederacion", text="Confederación")
        self.tree_expensive.heading("jugador", text="Jugador")
        self.tree_expensive.heading("equipo", text="Equipo")
        self.tree_expensive.heading("valor", text="Valor Mercado")
        self.tree_expensive.column("confederacion", width=150)
        self.tree_expensive.column("jugador", width=180)
        self.tree_expensive.column("equipo", width=150)
        self.tree_expensive.column("valor", width=150, anchor="e")
        self.tree_expensive.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(8, 0))
        ttk.Button(btn_frame, text="Ejecutar Consulta", command=self._query_most_expensive).pack(side="right")

        return frame

    def _query_most_expensive(self) -> None:
        for item in self.tree_expensive.get_children():
            self.tree_expensive.delete(item)

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT c.nombre as confederacion, j.nombre_completo as jugador,
                           e.nombre as equipo, j.valor_mercado
                    FROM jugadores j
                    JOIN equipos e ON j.id_equipo = e.id_equipo
                    JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM jugadores j2
                        JOIN equipos e2 ON j2.id_equipo = e2.id_equipo
                        WHERE e2.id_confederacion = e.id_confederacion
                          AND (
                              j2.valor_mercado > j.valor_mercado
                              OR (
                                  j2.valor_mercado = j.valor_mercado
                                  AND j2.id_jugador < j.id_jugador
                              )
                          )
                    )
                    ORDER BY c.nombre
                    """
                )
                results = cursor.fetchall()
                if not results:
                    messagebox.showinfo("Resultado", "No hay datos para mostrar.")
                    return

                for row in results:
                    self.tree_expensive.insert("", "end", values=(
                        row["confederacion"],
                        row["jugador"],
                        row["equipo"],
                        f"${row['valor_mercado']:,.2f}"
                    ))
            finally:
                cursor.close()

    def _build_matches_by_stadium(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Partidos por estadio", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        ttk.Label(frame, text="Selecciona un estadio:").pack(anchor="w", pady=(0, 5))
        self.stadium_combo = ttk.Combobox(frame, state="readonly", width=50)
        self.stadium_combo.pack(fill="x", pady=(0, 12))

        self.tree_matches = ttk.Treeview(
            frame,
            columns=("grupo", "local", "visitante", "fecha"),
            show="headings",
            height=15,
        )
        self.tree_matches.heading("grupo", text="Grupo")
        self.tree_matches.heading("local", text="Equipo Local")
        self.tree_matches.heading("visitante", text="Equipo Visitante")
        self.tree_matches.heading("fecha", text="Fecha/Hora")
        self.tree_matches.column("grupo", width=80, anchor="center")
        self.tree_matches.column("local", width=180)
        self.tree_matches.column("visitante", width=180)
        self.tree_matches.column("fecha", width=150)
        self.tree_matches.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(8, 0))
        ttk.Button(btn_frame, text="Ejecutar Consulta", command=self._query_matches_by_stadium).pack(side="right")

        self._load_stadiums()
        return frame

    def _load_stadiums(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    "SELECT id_estadio, nombre, nombre as ciudad FROM estadios ORDER BY nombre"
                )
                stadiums = cursor.fetchall()
                stadium_list = [f"{s['nombre']}" for s in stadiums]
                self.stadium_combo["values"] = stadium_list
            finally:
                cursor.close()

    def _query_matches_by_stadium(self) -> None:
        stadium_name = self.stadium_combo.get()
        if not stadium_name:
            messagebox.showwarning("Error", "Selecciona un estadio.")
            return

        for item in self.tree_matches.get_children():
            self.tree_matches.delete(item)

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT g.nombre as grupo, el.nombre as local, ev.nombre as visitante,
                           p.fecha_hora
                    FROM partidos p
                    JOIN grupos g ON p.id_grupo = g.id_grupo
                    JOIN equipos el ON p.id_equipo_local = el.id_equipo
                    JOIN equipos ev ON p.id_equipo_visitante = ev.id_equipo
                    JOIN estadios e ON p.id_estadio = e.id_estadio
                    WHERE e.nombre = %s
                    ORDER BY p.fecha_hora
                    """,
                    (stadium_name,),
                )
                results = cursor.fetchall()
                if not results:
                    messagebox.showinfo("Resultado", "No hay partidos en ese estadio.")
                    return

                for row in results:
                    self.tree_matches.insert("", "end", values=(
                        row["grupo"],
                        row["local"],
                        row["visitante"],
                        str(row["fecha_hora"])
                    ))
            finally:
                cursor.close()

    def _build_most_expensive_team(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Equipo más costoso por país anfitrión", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        self.tree_team = ttk.Treeview(
            frame,
            columns=("pais", "equipo", "valor"),
            show="headings",
            height=15,
        )
        self.tree_team.heading("pais", text="País")
        self.tree_team.heading("equipo", text="Equipo")
        self.tree_team.heading("valor", text="Valor Mercado")
        self.tree_team.column("pais", width=150)
        self.tree_team.column("equipo", width=250)
        self.tree_team.column("valor", width=200, anchor="e")
        self.tree_team.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(8, 0))
        ttk.Button(btn_frame, text="Ejecutar Consulta", command=self._query_most_expensive_team).pack(side="right")

        return frame

    def _query_most_expensive_team(self) -> None:
        for item in self.tree_team.get_children():
            self.tree_team.delete(item)

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT b.pais, b.equipo, b.valor_mercado_total
                    FROM (
                        SELECT DISTINCT
                            p_host.id_pais,
                            p_host.nombre AS pais,
                            e.id_equipo,
                            e.nombre AS equipo,
                            e.valor_mercado_total
                        FROM paises p_host
                        JOIN ciudades c ON c.id_pais = p_host.id_pais
                        JOIN estadios s ON s.id_ciudad = c.id_ciudad
                        JOIN partidos pr ON pr.id_estadio = s.id_estadio
                        JOIN equipos e
                          ON e.id_equipo = pr.id_equipo_local
                          OR e.id_equipo = pr.id_equipo_visitante
                        WHERE p_host.es_anfitrion = 1
                          AND pr.fase = 'GRUPOS'
                    ) b
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM (
                            SELECT DISTINCT
                                p_host.id_pais,
                                e.id_equipo,
                                e.valor_mercado_total
                            FROM paises p_host
                            JOIN ciudades c ON c.id_pais = p_host.id_pais
                            JOIN estadios s ON s.id_ciudad = c.id_ciudad
                            JOIN partidos pr ON pr.id_estadio = s.id_estadio
                            JOIN equipos e
                              ON e.id_equipo = pr.id_equipo_local
                              OR e.id_equipo = pr.id_equipo_visitante
                            WHERE p_host.es_anfitrion = 1
                              AND pr.fase = 'GRUPOS'
                        ) b2
                        WHERE b2.id_pais = b.id_pais
                          AND (
                              b2.valor_mercado_total > b.valor_mercado_total
                              OR (
                                  b2.valor_mercado_total = b.valor_mercado_total
                                  AND b2.id_equipo < b.id_equipo
                              )
                          )
                    )
                    ORDER BY b.pais
                    """
                )
                results = cursor.fetchall()
                if not results:
                    messagebox.showinfo("Resultado", "No hay datos para mostrar.")
                    return

                for row in results:
                    self.tree_team.insert("", "end", values=(
                        row["pais"],
                        row["equipo"],
                        f"${row['valor_mercado_total']:,.2f}"
                    ))
            finally:
                cursor.close()

    def _build_players_under_21(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Cantidad de jugadores menores de 21 años por equipo", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        self.tree_under21 = ttk.Treeview(
            frame,
            columns=("equipo", "confederacion", "cantidad"),
            show="headings",
            height=15,
        )
        self.tree_under21.heading("equipo", text="Equipo")
        self.tree_under21.heading("confederacion", text="Confederación")
        self.tree_under21.heading("cantidad", text="Jugadores <21")
        self.tree_under21.column("equipo", width=200)
        self.tree_under21.column("confederacion", width=200)
        self.tree_under21.column("cantidad", width=150, anchor="center")
        self.tree_under21.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(8, 0))
        ttk.Button(btn_frame, text="Ejecutar Consulta", command=self._query_players_under_21).pack(side="right")

        return frame

    def _query_players_under_21(self) -> None:
        for item in self.tree_under21.get_children():
            self.tree_under21.delete(item)

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT e.nombre as equipo, c.nombre as confederacion,
                           COUNT(j.id_jugador) as cantidad
                    FROM equipos e
                    JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                    LEFT JOIN jugadores j ON e.id_equipo = j.id_equipo
                        AND YEAR(CURDATE()) - YEAR(j.fecha_nacimiento) < 21
                    GROUP BY e.id_equipo, e.nombre, c.nombre
                    ORDER BY c.nombre, e.nombre
                    """
                )
                results = cursor.fetchall()
                if not results:
                    messagebox.showinfo("Resultado", "No hay datos para mostrar.")
                    return

                for row in results:
                    self.tree_under21.insert("", "end", values=(
                        row["equipo"],
                        row["confederacion"],
                        row["cantidad"]
                    ))
            finally:
                cursor.close()
