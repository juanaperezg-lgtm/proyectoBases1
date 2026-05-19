from app.daos import users_dao
from app.dtos.entities import UserCreateDTO, UserStatusUpdateDTO
from app.security import hash_password


def list_users() -> list[dict]:
    return users_dao.list_users()


def create_user(username: str, nombre_completo: str, password: str, tipo_usuario: str) -> None:
    users_dao.create_user(
        UserCreateDTO(
            username=username,
            nombre_completo=nombre_completo,
            password_hash=hash_password(password),
            tipo_usuario=tipo_usuario,
        )
    )


def update_user_status(id_usuario: int, active: bool) -> None:
    users_dao.update_user_status(UserStatusUpdateDTO(id_usuario=id_usuario, active=active))
