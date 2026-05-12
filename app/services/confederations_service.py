from app.database.connection import get_connection


def list_confederations() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_confederacion, nombre FROM confederaciones ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()


def create_confederation(nombre: str) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO confederaciones (nombre) VALUES (%s)", (nombre,))
            conn.commit()
        finally:
            cursor.close()


def update_confederation(id_confederacion: int, nombre: str) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE confederaciones SET nombre = %s WHERE id_confederacion = %s", (nombre, id_confederacion))
            conn.commit()
        finally:
            cursor.close()


def delete_confederation(id_confederacion: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM confederaciones WHERE id_confederacion = %s", (id_confederacion,))
            conn.commit()
        finally:
            cursor.close()
