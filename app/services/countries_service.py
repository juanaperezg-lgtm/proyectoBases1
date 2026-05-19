from app.daos import countries_dao
from app.dtos.entities import CountryCreateDTO, CountryUpdateDTO


def list_countries() -> list[dict]:
    return countries_dao.list_countries()


def create_country(nombre: str, es_anfitrion: bool) -> None:
    countries_dao.create_country(CountryCreateDTO(nombre=nombre, es_anfitrion=es_anfitrion))


def update_country(id_pais: int, nombre: str, es_anfitrion: bool) -> None:
    countries_dao.update_country(
        CountryUpdateDTO(id_pais=id_pais, nombre=nombre, es_anfitrion=es_anfitrion)
    )


def delete_country(id_pais: int) -> None:
    countries_dao.delete_country(id_pais)
