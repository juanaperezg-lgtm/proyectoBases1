from app.database.connection import get_connection
from app.dtos.entities import CoachCreateDTO, CoachUpdateDTO


def list_coaches() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT dt.id_dt, dt.nombre_completo, dt.nacionalidad, dt.edad,
                       e.nombre as equipo, dt.id_equipo
                FROM directores_tecnicos dt
                JOIN equipos e ON dt.id_equipo = e.id_equipo
                ORDER BY e.nombre
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_coach(payload: CoachCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO directores_tecnicos (nombre_completo, nacionalidad, edad, id_equipo)
                VALUES (%s, %s, %s, %s)
                """,
                (payload.nombre_completo, payload.nacionalidad, payload.edad, payload.id_equipo),
            )
            conn.commit()
        finally:
            cursor.close()


def update_coach(payload: CoachUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE directores_tecnicos SET nombre_completo = %s, nacionalidad = %s,
                       edad = %s, id_equipo = %s
                WHERE id_dt = %s
                """,
                (
                    payload.nombre_completo,
                    payload.nacionalidad,
                    payload.edad,
                    payload.id_equipo,
                    payload.id_dt,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_coach(id_dt: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM directores_tecnicos WHERE id_dt = %s", (id_dt,))
            conn.commit()
        finally:
            cursor.close()

