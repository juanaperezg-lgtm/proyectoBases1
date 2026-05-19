from app.daos import groups_dao
from app.dtos.entities import GroupAssignmentDTO


def list_groups() -> list[dict]:
    return groups_dao.list_groups()


def list_group_teams(id_grupo: int) -> list[dict]:
    return groups_dao.list_group_teams(id_grupo)


def list_available_teams(id_grupo: int) -> list[dict]:
    return groups_dao.list_available_teams(id_grupo)


def add_team_to_group(id_grupo: int, id_equipo: int) -> None:
    groups_dao.add_team_to_group(GroupAssignmentDTO(id_grupo=id_grupo, id_equipo=id_equipo))


def remove_team_from_group(id_grupo: int, id_equipo: int) -> None:
    groups_dao.remove_team_from_group(GroupAssignmentDTO(id_grupo=id_grupo, id_equipo=id_equipo))
