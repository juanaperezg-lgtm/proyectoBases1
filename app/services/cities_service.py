from app.database.connection import get_connection


def list_cities() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id_ciudad, c.nombre, p.nombre as pais, c.id_pais
                FROM ciudades c
                JOIN paises p ON c.id_pais = p.id_pais
                ORDER BY p.nombre, c.nombre
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_city(nombre: str, id_pais: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ciudades (nombre, id_pais) VALUES (%s, %s)", (nombre, id_pais))
            conn.commit()
        finally:
            cursor.close()


def update_city(id_ciudad: int, nombre: str, id_pais: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE ciudades SET nombre = %s, id_pais = %s WHERE id_ciudad = %s",
                (nombre, id_pais, id_ciudad),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_city(id_ciudad: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM ciudades WHERE id_ciudad = %s", (id_ciudad,))
            conn.commit()
        finally:
            cursor.close()
