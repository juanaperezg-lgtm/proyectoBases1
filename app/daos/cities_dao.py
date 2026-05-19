from app.database.connection import get_connection
from app.dtos.entities import CityCreateDTO, CityUpdateDTO


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


def create_city(payload: CityCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ciudades (nombre, id_pais) VALUES (%s, %s)", (payload.nombre, payload.id_pais))
            conn.commit()
        finally:
            cursor.close()


def update_city(payload: CityUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE ciudades SET nombre = %s, id_pais = %s WHERE id_ciudad = %s",
                (payload.nombre, payload.id_pais, payload.id_ciudad),
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

