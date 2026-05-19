from datetime import datetime
from typing import Optional

from app.database.connection import get_connection


def find_active_user_by_username(username: str) -> Optional[dict]:
    query = """
        SELECT id_usuario, username, nombre_completo, password_hash, tipo_usuario
        FROM usuarios
        WHERE username = %s AND activo = 1
    """
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (username,))
            return cursor.fetchone()
        finally:
            cursor.close()


def create_session_log(id_usuario: int, fecha_hora_entrada: datetime) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO bitacora_sesiones (id_usuario, fecha_hora_entrada)
                VALUES (%s, %s)
                """,
                (id_usuario, fecha_hora_entrada),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()


def close_session_log(id_bitacora: int, fecha_hora_salida: datetime) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE bitacora_sesiones
                SET fecha_hora_salida = %s
                WHERE id_bitacora = %s
                """,
                (fecha_hora_salida, id_bitacora),
            )
            conn.commit()
        finally:
            cursor.close()
