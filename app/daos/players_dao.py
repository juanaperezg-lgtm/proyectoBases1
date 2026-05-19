from app.database.connection import get_connection
from app.dtos.entities import PlayerCreateDTO, PlayerUpdateDTO


def list_players() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT j.id_jugador, j.nombre_completo, j.posicion, j.fecha_nacimiento,
                       j.estatura_m, j.peso_kg, j.valor_mercado, e.nombre as equipo, j.id_equipo
                FROM jugadores j
                JOIN equipos e ON j.id_equipo = e.id_equipo
                ORDER BY e.nombre, j.nombre_completo
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_player(payload: PlayerCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO jugadores (nombre_completo, posicion, fecha_nacimiento,
                       estatura_m, peso_kg, valor_mercado, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    payload.nombre_completo,
                    payload.posicion,
                    payload.fecha_nacimiento,
                    payload.estatura_m,
                    payload.peso_kg,
                    payload.valor_mercado,
                    payload.id_equipo,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def update_player(payload: PlayerUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE jugadores SET nombre_completo = %s, posicion = %s, fecha_nacimiento = %s,
                       estatura_m = %s, peso_kg = %s, valor_mercado = %s, id_equipo = %s
                WHERE id_jugador = %s
                """,
                (
                    payload.nombre_completo,
                    payload.posicion,
                    payload.fecha_nacimiento,
                    payload.estatura_m,
                    payload.peso_kg,
                    payload.valor_mercado,
                    payload.id_equipo,
                    payload.id_jugador,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_player(id_jugador: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM jugadores WHERE id_jugador = %s", (id_jugador,))
            conn.commit()
        finally:
            cursor.close()

