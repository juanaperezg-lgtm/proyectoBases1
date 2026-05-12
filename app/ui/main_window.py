from tkinter import Toplevel, ttk

from app.config import APP_TITLE
from app.services.auth_service import close_session
from app.ui.users_view import UsersView
from app.ui.confederations_view import ConfederationsView
from app.ui.countries_view import CountriesView
from app.ui.cities_view import CitiesView
from app.ui.stadiums_view import StadiumsView
from app.ui.teams_view import TeamsView
from app.ui.coaches_view import CoachesView
from app.ui.players_view import PlayersView
from app.ui.groups_view import GroupsView
from app.ui.matches_view import MatchesView
from app.ui.queries_view import QueriesView
from app.ui.reports_view import ReportsView


class MainWindow:
    def __init__(self, window: Toplevel, user: dict, bitacora_id: int, on_close_callback) -> None:
        self.window = window
        self.user = user
        self.bitacora_id = bitacora_id
        self.on_close_callback = on_close_callback

        self.window.title(APP_TITLE)
        self.window.geometry("1200x700")
        self.window.protocol("WM_DELETE_WINDOW", self._close)

        header = ttk.Frame(self.window, padding=12)
        header.pack(fill="x")
        ttk.Label(
            header,
            text=f"Usuario: {user['nombre_completo']} ({user['tipo_usuario']})",
            font=("", 10, "bold"),
        ).pack(side="left")
        ttk.Button(header, text="Cerrar sesión", command=self._close).pack(side="right")

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        if user["tipo_usuario"] in ["ADMIN", "TRADICIONAL"]:
            data_notebook = ttk.Notebook(notebook)
            notebook.add(data_notebook, text="Gestión de Datos")
            data_notebook.add(ConfederationsView(data_notebook), text="Confederaciones")
            data_notebook.add(CountriesView(data_notebook), text="Países")
            data_notebook.add(CitiesView(data_notebook), text="Ciudades")
            data_notebook.add(StadiumsView(data_notebook), text="Estadios")
            data_notebook.add(TeamsView(data_notebook), text="Equipos")
            data_notebook.add(CoachesView(data_notebook), text="Dir. Técnicos")
            data_notebook.add(PlayersView(data_notebook), text="Jugadores")
            data_notebook.add(GroupsView(data_notebook), text="Grupos")
            data_notebook.add(MatchesView(data_notebook), text="Partidos")

        notebook.add(QueriesView(notebook), text="Consultas")

        if user["tipo_usuario"] in ["ADMIN", "TRADICIONAL"]:
            notebook.add(ReportsView(notebook), text="Reportes")

        if user["tipo_usuario"] == "ADMIN":
            notebook.add(UsersView(notebook), text="Usuarios")

    def _close(self) -> None:
        close_session(self.bitacora_id)
        self.window.destroy()
        self.on_close_callback()
