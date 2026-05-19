from datetime import datetime

from app.daos import auth_dao
from app.security import verify_password


def authenticate(username: str, password: str):
    row = auth_dao.find_active_user_by_username(username)
    if not row:
        return None, None
    if not verify_password(password, row["password_hash"]):
        return None, None

    bitacora_id = auth_dao.create_session_log(row["id_usuario"], datetime.now())
    user = {
        "id_usuario": row["id_usuario"],
        "username": row["username"],
        "nombre_completo": row["nombre_completo"],
        "tipo_usuario": row["tipo_usuario"],
    }
    return user, bitacora_id


def close_session(bitacora_id: int) -> None:
    auth_dao.close_session_log(bitacora_id, datetime.now())
