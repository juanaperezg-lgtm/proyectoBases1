from app.daos import confederations_dao
from app.dtos.entities import ConfederationCreateDTO, ConfederationUpdateDTO


def list_confederations() -> list[dict]:
    return confederations_dao.list_confederations()


def create_confederation(nombre: str) -> None:
    confederations_dao.create_confederation(ConfederationCreateDTO(nombre=nombre))


def update_confederation(id_confederacion: int, nombre: str) -> None:
    confederations_dao.update_confederation(
        ConfederationUpdateDTO(id_confederacion=id_confederacion, nombre=nombre)
    )


def delete_confederation(id_confederacion: int) -> None:
    confederations_dao.delete_confederation(id_confederacion)
