from app.database.connection import get_connection


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


def create_coach(nombre_completo: str, nacionalidad: str, edad: int, id_equipo: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO directores_tecnicos (nombre_completo, nacionalidad, edad, id_equipo)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre_completo, nacionalidad, edad, id_equipo),
            )
            conn.commit()
        finally:
            cursor.close()


def update_coach(id_dt: int, nombre_completo: str, nacionalidad: str, edad: int, id_equipo: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE directores_tecnicos SET nombre_completo = %s, nacionalidad = %s,
                       edad = %s, id_equipo = %s
                WHERE id_dt = %s
                """,
                (nombre_completo, nacionalidad, edad, id_equipo, id_dt),
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
