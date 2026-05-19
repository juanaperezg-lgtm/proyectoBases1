from app.database.connection import get_connection
from app.dtos.entities import BitacoraDateRangeDTO, PlayerReportFilterDTO


def fetch_bitacora_entries(payload: BitacoraDateRangeDTO) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT u.nombre_completo, b.fecha_hora_entrada, b.fecha_hora_salida
                FROM bitacora_sesiones b
                JOIN usuarios u ON b.id_usuario = u.id_usuario
                WHERE DATE(b.fecha_hora_entrada) BETWEEN %s AND %s
                ORDER BY b.fecha_hora_entrada
                """,
                (payload.fecha_inicio, payload.fecha_fin),
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_players_for_report(payload: PlayerReportFilterDTO) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            if payload.id_equipo:
                cursor.execute(
                    """
                    SELECT j.nombre_completo, j.posicion, j.estatura_m, j.peso_kg,
                           j.valor_mercado, e.nombre as equipo
                    FROM jugadores j
                    JOIN equipos e ON j.id_equipo = e.id_equipo
                    WHERE j.peso_kg BETWEEN %s AND %s
                    AND j.estatura_m BETWEEN %s AND %s
                    AND j.id_equipo = %s
                    ORDER BY e.nombre, j.nombre_completo
                    """,
                    (
                        payload.peso_min,
                        payload.peso_max,
                        payload.estatura_min,
                        payload.estatura_max,
                        payload.id_equipo,
                    ),
                )
            else:
                cursor.execute(
                    """
                    SELECT j.nombre_completo, j.posicion, j.estatura_m, j.peso_kg,
                           j.valor_mercado, e.nombre as equipo
                    FROM jugadores j
                    JOIN equipos e ON j.id_equipo = e.id_equipo
                    WHERE j.peso_kg BETWEEN %s AND %s
                    AND j.estatura_m BETWEEN %s AND %s
                    ORDER BY e.nombre, j.nombre_completo
                    """,
                    (payload.peso_min, payload.peso_max, payload.estatura_min, payload.estatura_max),
                )
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_team_values_by_confederation(id_confederacion: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT e.nombre as equipo, c.nombre as confederacion,
                       SUM(j.valor_mercado) as valor_total, COUNT(j.id_jugador) as cantidad_jugadores
                FROM equipos e
                JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
                LEFT JOIN jugadores j ON e.id_equipo = j.id_equipo
                WHERE e.id_confederacion = %s
                GROUP BY e.id_equipo, e.nombre, c.nombre
                ORDER BY e.nombre
                """,
                (id_confederacion,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_host_country_participants() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT DISTINCT p.nombre as pais_anfitrion, pa.nombre as pais_equipo
                FROM paises p
                JOIN ciudades c ON p.id_pais = c.id_pais
                JOIN estadios e ON c.id_ciudad = e.id_ciudad
                JOIN partidos pr ON e.id_estadio = pr.id_estadio
                JOIN equipos eq ON (pr.id_equipo_local = eq.id_equipo OR pr.id_equipo_visitante = eq.id_equipo)
                JOIN paises pa ON eq.id_pais = pa.id_pais
                WHERE p.es_anfitrion = 1
                ORDER BY p.nombre, pa.nombre
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()

