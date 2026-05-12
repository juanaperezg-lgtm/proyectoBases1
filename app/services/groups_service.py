from app.database.connection import get_connection


def list_groups() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_grupo, nombre FROM grupos ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()


def list_group_teams(id_grupo: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT e.id_equipo, e.nombre, c.nombre as confederacion
                FROM grupo_equipos ge
                JOIN equipos e ON ge.id_equipo = e.id_equipo
                JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                WHERE ge.id_grupo = %s
                ORDER BY e.nombre
                """,
                (id_grupo,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def list_available_teams(id_grupo: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT e.id_equipo, e.nombre, c.nombre as confederacion
                FROM equipos e
                JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                WHERE e.id_equipo NOT IN (
                    SELECT id_equipo FROM grupo_equipos WHERE id_grupo = %s
                )
                ORDER BY e.nombre
                """,
                (id_grupo,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def add_team_to_group(id_grupo: int, id_equipo: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO grupo_equipos (id_grupo, id_equipo) VALUES (%s, %s)",
                (id_grupo, id_equipo),
            )
            conn.commit()
        finally:
            cursor.close()


def remove_team_from_group(id_grupo: int, id_equipo: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM grupo_equipos WHERE id_grupo = %s AND id_equipo = %s",
                (id_grupo, id_equipo),
            )
            conn.commit()
        finally:
            cursor.close()
