from app.database.connection import get_connection


def list_countries() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_pais, nombre, es_anfitrion FROM paises ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()


def create_country(nombre: str, es_anfitrion: bool) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO paises (nombre, es_anfitrion) VALUES (%s, %s)",
                (nombre, 1 if es_anfitrion else 0),
            )
            conn.commit()
        finally:
            cursor.close()


def update_country(id_pais: int, nombre: str, es_anfitrion: bool) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE paises SET nombre = %s, es_anfitrion = %s WHERE id_pais = %s",
                (nombre, 1 if es_anfitrion else 0, id_pais),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_country(id_pais: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM paises WHERE id_pais = %s", (id_pais,))
            conn.commit()
        finally:
            cursor.close()
