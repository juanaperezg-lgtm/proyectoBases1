from app.daos import coaches_dao
from app.dtos.entities import CoachCreateDTO, CoachUpdateDTO


def list_coaches() -> list[dict]:
    return coaches_dao.list_coaches()


def create_coach(nombre_completo: str, nacionalidad: str, edad: int, id_equipo: int) -> None:
    coaches_dao.create_coach(
        CoachCreateDTO(
            nombre_completo=nombre_completo,
            nacionalidad=nacionalidad,
            edad=edad,
            id_equipo=id_equipo,
        )
    )


def update_coach(id_dt: int, nombre_completo: str, nacionalidad: str, edad: int, id_equipo: int) -> None:
    coaches_dao.update_coach(
        CoachUpdateDTO(
            id_dt=id_dt,
            nombre_completo=nombre_completo,
            nacionalidad=nacionalidad,
            edad=edad,
            id_equipo=id_equipo,
        )
    )


def delete_coach(id_dt: int) -> None:
    coaches_dao.delete_coach(id_dt)
