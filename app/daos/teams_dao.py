from app.database.connection import get_connection
from app.dtos.entities import TeamCreateDTO, TeamUpdateDTO


def list_teams() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT e.id_equipo, e.nombre, p.nombre as pais, c.nombre as confederacion,
                       e.valor_mercado_total
                FROM equipos e
                JOIN paises p ON e.id_pais = p.id_pais
                JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                ORDER BY e.nombre
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def create_team(payload: TeamCreateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO equipos (nombre, id_pais, id_confederacion, valor_mercado_total)
                VALUES (%s, %s, %s, %s)
                """,
                (payload.nombre, payload.id_pais, payload.id_confederacion, payload.valor_mercado_total),
            )
            conn.commit()
        finally:
            cursor.close()


def update_team(payload: TeamUpdateDTO) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE equipos SET nombre = %s, id_pais = %s, id_confederacion = %s,
                       valor_mercado_total = %s
                WHERE id_equipo = %s
                """,
                (
                    payload.nombre,
                    payload.id_pais,
                    payload.id_confederacion,
                    payload.valor_mercado_total,
                    payload.id_equipo,
                ),
            )
            conn.commit()
        finally:
            cursor.close()


def delete_team(id_equipo: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
            conn.commit()
        finally:
            cursor.close()

