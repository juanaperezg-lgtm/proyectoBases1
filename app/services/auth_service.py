from datetime import datetime

from app.database.connection import get_connection
from app.security import verify_password


def authenticate(username: str, password: str):
    query = """
        SELECT id_usuario, username, nombre_completo, password_hash, tipo_usuario
        FROM usuarios
        WHERE username = %s AND activo = 1
    """
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if not row:
                return None, None
            if not verify_password(password, row["password_hash"]):
                return None, None

            cursor.execute(
                """
                INSERT INTO bitacora_sesiones (id_usuario, fecha_hora_entrada)
                VALUES (%s, %s)
                """,
                (row["id_usuario"], datetime.now()),
            )
            conn.commit()
            bitacora_id = cursor.lastrowid
            user = {
                "id_usuario": row["id_usuario"],
                "username": row["username"],
                "nombre_completo": row["nombre_completo"],
                "tipo_usuario": row["tipo_usuario"],
            }
            return user, bitacora_id
        finally:
            cursor.close()


def close_session(bitacora_id: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE bitacora_sesiones
                SET fecha_hora_salida = %s
                WHERE id_bitacora = %s
                """,
                (datetime.now(), bitacora_id),
            )
            conn.commit()
        finally:
            cursor.close()
