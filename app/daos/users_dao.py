from app.database.connection import get_connection
from app.dtos.entities import UserCreateDTO, UserStatusUpdateDTO


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


def create_user(payload: UserCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (username, nombre_completo, password_hash, tipo_usuario, activo)
                VALUES (%s, %s, %s, %s, 1)
                """,
                (payload.username, payload.nombre_completo, payload.password_hash, payload.tipo_usuario),
            )
            conn.commit()
        finally:
            cursor.close()


def update_user_status(payload: UserStatusUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET activo = %s WHERE id_usuario = %s",
                (1 if payload.active else 0, payload.id_usuario),
            )
            conn.commit()
        finally:
            cursor.close()

