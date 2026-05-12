from app.database.connection import get_connection
from app.security import hash_password


def list_users() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_usuario, username, nombre_completo, tipo_usuario, activo, fecha_creacion
                FROM usuarios
                ORDER BY id_usuario
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_user(username: str, nombre_completo: str, password: str, tipo_usuario: str) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (username, nombre_completo, password_hash, tipo_usuario, activo)
                VALUES (%s, %s, %s, %s, 1)
                """,
                (username, nombre_completo, hash_password(password), tipo_usuario),
            )
            conn.commit()
        finally:
            cursor.close()


def update_user_status(id_usuario: int, active: bool) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET activo = %s WHERE id_usuario = %s",
                (1 if active else 0, id_usuario),
            )
            conn.commit()
        finally:
            cursor.close()
