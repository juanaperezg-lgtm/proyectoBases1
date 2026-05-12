from app.database.connection import get_connection


def list_stadiums() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT e.id_estadio, e.nombre, c.nombre as ciudad, e.capacidad, e.id_ciudad
                FROM estadios e
                JOIN ciudades c ON e.id_ciudad = c.id_ciudad
                ORDER BY c.nombre, e.nombre
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_stadium(nombre: str, capacidad: int, id_ciudad: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO estadios (nombre, capacidad, id_ciudad) VALUES (%s, %s, %s)",
                (nombre, capacidad, id_ciudad),
            )
            conn.commit()
        finally:
            cursor.close()


def update_stadium(id_estadio: int, nombre: str, capacidad: int, id_ciudad: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE estadios SET nombre = %s, capacidad = %s, id_ciudad = %s WHERE id_estadio = %s",
                (nombre, capacidad, id_ciudad, id_estadio),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_stadium(id_estadio: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM estadios WHERE id_estadio = %s", (id_estadio,))
            conn.commit()
        finally:
            cursor.close()
