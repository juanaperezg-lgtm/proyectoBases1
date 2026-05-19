from app.daos import players_dao
from app.dtos.entities import PlayerCreateDTO, PlayerUpdateDTO


def list_players() -> list[dict]:
    return players_dao.list_players()


def create_player(nombre_completo: str, posicion: str, fecha_nacimiento: str,
                 estatura_m: float, peso_kg: float, valor_mercado: float, id_equipo: int) -> None:
    players_dao.create_player(
        PlayerCreateDTO(
            nombre_completo=nombre_completo,
            posicion=posicion,
            fecha_nacimiento=fecha_nacimiento,
            estatura_m=estatura_m,
            peso_kg=peso_kg,
            valor_mercado=valor_mercado,
            id_equipo=id_equipo,
        )
    )


def update_player(id_jugador: int, nombre_completo: str, posicion: str, fecha_nacimiento: str,
                 estatura_m: float, peso_kg: float, valor_mercado: float, id_equipo: int) -> None:
    players_dao.update_player(
        PlayerUpdateDTO(
            id_jugador=id_jugador,
            nombre_completo=nombre_completo,
            posicion=posicion,
            fecha_nacimiento=fecha_nacimiento,
            estatura_m=estatura_m,
            peso_kg=peso_kg,
            valor_mercado=valor_mercado,
            id_equipo=id_equipo,
        )
    )


def delete_player(id_jugador: int) -> None:
    players_dao.delete_player(id_jugador)
