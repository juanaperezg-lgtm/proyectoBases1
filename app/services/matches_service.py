from app.daos import matches_dao
from app.dtos.entities import MatchCreateDTO, MatchUpdateDTO


def list_matches() -> list[dict]:
    return matches_dao.list_matches()


def create_match(id_grupo: int, id_estadio: int, id_equipo_local: int,
                id_equipo_visitante: int, fecha_hora: str) -> None:
    matches_dao.create_match(
        MatchCreateDTO(
            id_grupo=id_grupo,
            id_estadio=id_estadio,
            id_equipo_local=id_equipo_local,
            id_equipo_visitante=id_equipo_visitante,
            fecha_hora=fecha_hora,
        )
    )


def update_match(id_partido: int, id_grupo: int, id_estadio: int, id_equipo_local: int,
                id_equipo_visitante: int, fecha_hora: str) -> None:
    matches_dao.update_match(
        MatchUpdateDTO(
            id_partido=id_partido,
            id_grupo=id_grupo,
            id_estadio=id_estadio,
            id_equipo_local=id_equipo_local,
            id_equipo_visitante=id_equipo_visitante,
            fecha_hora=fecha_hora,
        )
    )


def delete_match(id_partido: int) -> None:
    matches_dao.delete_match(id_partido)
