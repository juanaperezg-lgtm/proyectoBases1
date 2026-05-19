from app.daos import stadiums_dao
from app.dtos.entities import StadiumCreateDTO, StadiumUpdateDTO


def list_stadiums() -> list[dict]:
    return stadiums_dao.list_stadiums()


def create_stadium(nombre: str, capacidad: int, id_ciudad: int) -> None:
    stadiums_dao.create_stadium(
        StadiumCreateDTO(nombre=nombre, capacidad=capacidad, id_ciudad=id_ciudad)
    )


def update_stadium(id_estadio: int, nombre: str, capacidad: int, id_ciudad: int) -> None:
    stadiums_dao.update_stadium(
        StadiumUpdateDTO(id_estadio=id_estadio, nombre=nombre, capacidad=capacidad, id_ciudad=id_ciudad)
    )


def delete_stadium(id_estadio: int) -> None:
    stadiums_dao.delete_stadium(id_estadio)
