from app.daos import cities_dao
from app.dtos.entities import CityCreateDTO, CityUpdateDTO


def list_cities() -> list[dict]:
    return cities_dao.list_cities()


def create_city(nombre: str, id_pais: int) -> None:
    cities_dao.create_city(CityCreateDTO(nombre=nombre, id_pais=id_pais))


def update_city(id_ciudad: int, nombre: str, id_pais: int) -> None:
    cities_dao.update_city(CityUpdateDTO(id_ciudad=id_ciudad, nombre=nombre, id_pais=id_pais))


def delete_city(id_ciudad: int) -> None:
    cities_dao.delete_city(id_ciudad)
