from app.database.connection import get_connection
from app.dtos.entities import MatchCreateDTO, MatchUpdateDTO


def list_matches() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT p.id_partido, g.nombre as grupo, el.nombre as equipo_local,
                       ev.nombre as equipo_visitante, e.nombre as estadio, p.fecha_hora
                FROM partidos p
                JOIN grupos g ON p.id_grupo = g.id_grupo
                JOIN equipos el ON p.id_equipo_local = el.id_equipo
                JOIN equipos ev ON p.id_equipo_visitante = ev.id_equipo
                JOIN estadios e ON p.id_estadio = e.id_estadio
                ORDER BY p.fecha_hora
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_match(payload: MatchCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO partidos (id_grupo, id_estadio, id_equipo_local,
                       id_equipo_visitante, fecha_hora, fase)
                VALUES (%s, %s, %s, %s, %s, 'GRUPOS')
                """,
                (
                    payload.id_grupo,
                    payload.id_estadio,
                    payload.id_equipo_local,
                    payload.id_equipo_visitante,
                    payload.fecha_hora,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def update_match(payload: MatchUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE partidos SET id_grupo = %s, id_estadio = %s, id_equipo_local = %s,
                       id_equipo_visitante = %s, fecha_hora = %s
                WHERE id_partido = %s
                """,
                (
                    payload.id_grupo,
                    payload.id_estadio,
                    payload.id_equipo_local,
                    payload.id_equipo_visitante,
                    payload.fecha_hora,
                    payload.id_partido,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_match(id_partido: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM partidos WHERE id_partido = %s", (id_partido,))
            conn.commit()
        finally:
            cursor.close()

