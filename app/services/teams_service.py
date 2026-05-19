from app.daos import teams_dao
from app.dtos.entities import TeamCreateDTO, TeamUpdateDTO


def list_teams() -> list[dict]:
    return teams_dao.list_teams()


def create_team(nombre: str, id_pais: int, id_confederacion: int, valor_mercado_total: float) -> None:
    teams_dao.create_team(
        TeamCreateDTO(
            nombre=nombre,
            id_pais=id_pais,
            id_confederacion=id_confederacion,
            valor_mercado_total=valor_mercado_total,
        )
    )


def update_team(id_equipo: int, nombre: str, id_pais: int, id_confederacion: int, valor_mercado_total: float) -> None:
    teams_dao.update_team(
        TeamUpdateDTO(
            id_equipo=id_equipo,
            nombre=nombre,
            id_pais=id_pais,
            id_confederacion=id_confederacion,
            valor_mercado_total=valor_mercado_total,
        )
    )


def delete_team(id_equipo: int) -> None:
    teams_dao.delete_team(id_equipo)
