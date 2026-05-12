from datetime import datetime, timedelta

from app.database.connection import get_connection


CONFEDERACIONES = ["AFC", "CAF", "CONMEBOL", "CONCACAF", "UEFA", "OFC"]
GROUP_NAMES = [chr(code) for code in range(ord("A"), ord("L") + 1)]
POSITIONS = [
    "POR",
    "DEF",
    "DEF",
    "DEF",
    "DEF",
    "MED",
    "MED",
    "MED",
    "MED",
    "DEL",
    "DEL",
    "POR",
    "DEF",
    "DEF",
    "DEF",
    "MED",
    "MED",
    "MED",
    "DEL",
    "DEL",
    "DEF",
    "MED",
    "DEL",
]
CONFED_BASE_PLAYER_VALUE = {
    "UEFA": 14_000_000,
    "CONMEBOL": 12_000_000,
    "CONCACAF": 7_000_000,
    "AFC": 6_000_000,
    "CAF": 7_000_000,
    "OFC": 1_000_000,
}

TEAMS = [
    ("Argentina", "Argentina", "CONMEBOL", 980_000_000),
    ("Brazil", "Brazil", "CONMEBOL", 1_120_000_000),
    ("Uruguay", "Uruguay", "CONMEBOL", 520_000_000),
    ("Colombia", "Colombia", "CONMEBOL", 480_000_000),
    ("Ecuador", "Ecuador", "CONMEBOL", 420_000_000),
    ("Chile", "Chile", "CONMEBOL", 250_000_000),
    ("Mexico", "Mexico", "CONCACAF", 260_000_000),
    ("USA", "USA", "CONCACAF", 420_000_000),
    ("Canada", "Canada", "CONCACAF", 210_000_000),
    ("Costa Rica", "Costa Rica", "CONCACAF", 120_000_000),
    ("Panama", "Panama", "CONCACAF", 95_000_000),
    ("Jamaica", "Jamaica", "CONCACAF", 90_000_000),
    ("France", "France", "UEFA", 1_250_000_000),
    ("England", "England", "UEFA", 1_300_000_000),
    ("Spain", "Spain", "UEFA", 1_200_000_000),
    ("Germany", "Germany", "UEFA", 1_000_000_000),
    ("Portugal", "Portugal", "UEFA", 950_000_000),
    ("Netherlands", "Netherlands", "UEFA", 900_000_000),
    ("Italy", "Italy", "UEFA", 850_000_000),
    ("Belgium", "Belgium", "UEFA", 700_000_000),
    ("Croatia", "Croatia", "UEFA", 500_000_000),
    ("Denmark", "Denmark", "UEFA", 450_000_000),
    ("Switzerland", "Switzerland", "UEFA", 400_000_000),
    ("Serbia", "Serbia", "UEFA", 350_000_000),
    ("Poland", "Poland", "UEFA", 380_000_000),
    ("Austria", "Austria", "UEFA", 320_000_000),
    ("Ukraine", "Ukraine", "UEFA", 300_000_000),
    ("Czech Republic", "Czech Republic", "UEFA", 280_000_000),
    ("Japan", "Japan", "AFC", 340_000_000),
    ("South Korea", "South Korea", "AFC", 210_000_000),
    ("Iran", "Iran", "AFC", 180_000_000),
    ("Australia", "Australia", "AFC", 190_000_000),
    ("Saudi Arabia", "Saudi Arabia", "AFC", 175_000_000),
    ("Qatar", "Qatar", "AFC", 140_000_000),
    ("Iraq", "Iraq", "AFC", 115_000_000),
    ("Uzbekistan", "Uzbekistan", "AFC", 100_000_000),
    ("Morocco", "Morocco", "CAF", 360_000_000),
    ("Senegal", "Senegal", "CAF", 290_000_000),
    ("Nigeria", "Nigeria", "CAF", 330_000_000),
    ("Egypt", "Egypt", "CAF", 260_000_000),
    ("Algeria", "Algeria", "CAF", 240_000_000),
    ("Tunisia", "Tunisia", "CAF", 170_000_000),
    ("Cameroon", "Cameroon", "CAF", 190_000_000),
    ("Ghana", "Ghana", "CAF", 200_000_000),
    ("Ivory Coast", "Ivory Coast", "CAF", 250_000_000),
    ("South Africa", "South Africa", "CAF", 130_000_000),
    ("New Zealand", "New Zealand", "OFC", 38_000_000),
    ("Solomon Islands", "Solomon Islands", "OFC", 7_500_000),
]

HOST_CITIES = [
    ("Mexico", "Mexico City"),
    ("Mexico", "Guadalajara"),
    ("Mexico", "Monterrey"),
    ("USA", "Los Angeles"),
    ("USA", "New York"),
    ("USA", "Dallas"),
    ("Canada", "Toronto"),
    ("Canada", "Vancouver"),
    ("Canada", "Edmonton"),
]

HOST_STADIUMS = [
    ("Mexico City", "Estadio Azteca", 87523),
    ("Guadalajara", "Estadio Akron", 49850),
    ("Monterrey", "Estadio BBVA", 53500),
    ("Los Angeles", "SoFi Stadium", 70240),
    ("New York", "MetLife Stadium", 82500),
    ("Dallas", "AT&T Stadium", 80000),
    ("Toronto", "BMO Field", 30000),
    ("Vancouver", "BC Place", 54500),
    ("Edmonton", "Commonwealth Stadium", 56000),
]

STAR_PLAYERS = {
    "Argentina": [
        ("Lautaro Martinez", "DEL", "1997-08-22", 1.74, 72.0, 95_000_000),
        ("Julian Alvarez", "DEL", "2000-01-31", 1.70, 71.0, 90_000_000),
        ("Enzo Fernandez", "MED", "2001-01-17", 1.78, 76.0, 75_000_000),
    ],
    "Brazil": [
        ("Vinicius Junior", "DEL", "2000-07-12", 1.76, 73.0, 200_000_000),
        ("Rodrygo", "DEL", "2001-01-09", 1.74, 64.0, 120_000_000),
        ("Endrick", "DEL", "2006-07-21", 1.73, 66.0, 60_000_000),
    ],
    "France": [
        ("Kylian Mbappe", "DEL", "1998-12-20", 1.78, 75.0, 180_000_000),
        ("Aurelien Tchouameni", "MED", "2000-01-27", 1.87, 81.0, 90_000_000),
        ("Warren Zaire-Emery", "MED", "2006-03-08", 1.78, 68.0, 70_000_000),
    ],
    "England": [
        ("Jude Bellingham", "MED", "2003-06-29", 1.86, 75.0, 180_000_000),
        ("Bukayo Saka", "DEL", "2001-09-05", 1.78, 72.0, 150_000_000),
        ("Cole Palmer", "DEL", "2002-05-06", 1.85, 74.0, 130_000_000),
    ],
    "Spain": [
        ("Rodri", "MED", "1996-06-22", 1.91, 82.0, 110_000_000),
        ("Lamine Yamal", "DEL", "2007-07-13", 1.80, 72.0, 140_000_000),
        ("Pedri", "MED", "2002-11-25", 1.74, 60.0, 100_000_000),
    ],
    "Germany": [
        ("Jamal Musiala", "MED", "2003-02-26", 1.84, 72.0, 140_000_000),
        ("Florian Wirtz", "MED", "2003-05-03", 1.76, 70.0, 140_000_000),
        ("Kai Havertz", "DEL", "1999-06-11", 1.93, 83.0, 70_000_000),
    ],
    "Portugal": [
        ("Rafael Leao", "DEL", "1999-06-10", 1.88, 81.0, 95_000_000),
        ("Bruno Fernandes", "MED", "1994-09-08", 1.79, 69.0, 65_000_000),
        ("Goncalo Ramos", "DEL", "2001-06-20", 1.85, 79.0, 60_000_000),
    ],
    "USA": [
        ("Christian Pulisic", "DEL", "1998-09-18", 1.78, 73.0, 45_000_000),
        ("Weston McKennie", "MED", "1998-08-28", 1.85, 84.0, 28_000_000),
        ("Yunus Musah", "MED", "2002-11-29", 1.78, 75.0, 30_000_000),
    ],
    "Mexico": [
        ("Santiago Gimenez", "DEL", "2001-04-18", 1.82, 76.0, 70_000_000),
        ("Edson Alvarez", "MED", "1997-10-24", 1.90, 82.0, 40_000_000),
        ("Ramon Juarez", "DEF", "2001-05-09", 1.82, 75.0, 6_500_000),
    ],
    "Japan": [
        ("Takefusa Kubo", "DEL", "2001-06-04", 1.73, 67.0, 60_000_000),
        ("Kaoru Mitoma", "DEL", "1997-05-20", 1.78, 73.0, 50_000_000),
        ("Zion Suzuki", "POR", "2002-08-21", 1.90, 91.0, 15_000_000),
    ],
    "South Korea": [
        ("Son Heung-min", "DEL", "1992-07-08", 1.84, 78.0, 35_000_000),
        ("Lee Kang-in", "MED", "2001-02-19", 1.74, 70.0, 45_000_000),
        ("Yang Min-hyeok", "DEL", "2006-04-16", 1.77, 68.0, 12_000_000),
    ],
    "Morocco": [
        ("Achraf Hakimi", "DEF", "1998-11-04", 1.81, 73.0, 70_000_000),
        ("Brahim Diaz", "MED", "1999-08-03", 1.71, 68.0, 45_000_000),
        ("Bilal El Khannouss", "MED", "2004-05-10", 1.80, 70.0, 35_000_000),
    ],
    "Nigeria": [
        ("Victor Osimhen", "DEL", "1998-12-29", 1.86, 78.0, 110_000_000),
        ("Ademola Lookman", "DEL", "1997-10-20", 1.74, 71.0, 40_000_000),
        ("Alex Iwobi", "MED", "1996-05-03", 1.83, 75.0, 22_000_000),
    ],
    "Egypt": [
        ("Mohamed Salah", "DEL", "1992-06-15", 1.75, 71.0, 55_000_000),
        ("Omar Marmoush", "DEL", "1999-02-07", 1.83, 81.0, 30_000_000),
        ("Mohamed Abdelmonem", "DEF", "1999-02-01", 1.83, 79.0, 8_000_000),
    ],
}


def _build_country_rows() -> list[tuple[str, int]]:
    host_map = {"Mexico": 1, "USA": 1, "Canada": 1}
    countries = sorted({country for _, country, _, _ in TEAMS})
    return [(country, host_map.get(country, 0)) for country in countries]


def _generate_player_rows(team: str, confederation: str) -> list[tuple[str, str, str, float, float, int]]:
    stars = STAR_PLAYERS.get(team, [])
    players = [tuple(star) for star in stars]
    missing = 23 - len(players)
    team_seed = sum(ord(ch) for ch in team)
    base_value = CONFED_BASE_PLAYER_VALUE[confederation]

    for idx in range(missing):
        pos = POSITIONS[(idx + len(stars)) % len(POSITIONS)]
        year = 1994 + ((team_seed + idx) % 14)
        if idx % 7 == 0:
            year = 2006 + ((team_seed + idx) % 2)
        month = ((team_seed + idx) % 12) + 1
        day = ((team_seed * 3 + idx * 5) % 28) + 1
        birthdate = f"{year:04d}-{month:02d}-{day:02d}"
        height = round(1.70 + ((team_seed + idx * 2) % 25) / 100, 2)
        weight = round(66 + ((team_seed + idx * 4) % 24), 1)
        value = max(250_000, base_value + (missing - idx) * 900_000 - (idx % 4) * 200_000)
        players.append((f"{team} Player {idx + 1:02d}", pos, birthdate, height, weight, value))

    return players


def _build_groups() -> list[tuple[str, str]]:
    group_rows = []
    for index, (team, _, _, _) in enumerate(TEAMS):
        group_rows.append((GROUP_NAMES[index // 4], team))
    return group_rows


def _build_matches(group_rows: list[tuple[str, str]]) -> list[tuple[str, str, str, str, str]]:
    stadiums = [stadium for _, stadium, _ in HOST_STADIUMS]
    start_date = datetime(2026, 6, 11, 14, 0, 0)
    pairings = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]
    matches = []
    cursor = 0

    for group in GROUP_NAMES:
        teams_in_group = [team for g, team in group_rows if g == group]
        for local_idx, away_idx in pairings:
            kick_off = start_date + timedelta(hours=6 * (cursor % 3), days=cursor // 3)
            matches.append(
                (
                    group,
                    stadiums[cursor % len(stadiums)],
                    teams_in_group[local_idx],
                    teams_in_group[away_idx],
                    kick_off.strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            cursor += 1

    return matches


def seed_realistic_data() -> None:
    country_rows = _build_country_rows()
    group_rows = _build_groups()
    match_rows = _build_matches(group_rows)

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE partidos")
            cursor.execute("TRUNCATE TABLE grupo_equipos")
            cursor.execute("TRUNCATE TABLE jugadores")
            cursor.execute("TRUNCATE TABLE directores_tecnicos")
            cursor.execute("TRUNCATE TABLE equipos")
            cursor.execute("TRUNCATE TABLE estadios")
            cursor.execute("TRUNCATE TABLE ciudades")
            cursor.execute("TRUNCATE TABLE grupos")
            cursor.execute("TRUNCATE TABLE paises")
            cursor.execute("TRUNCATE TABLE confederaciones")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            for conf in CONFEDERACIONES:
                cursor.execute("INSERT INTO confederaciones (nombre) VALUES (%s)", (conf,))

            for country, is_host in country_rows:
                cursor.execute(
                    "INSERT INTO paises (nombre, es_anfitrion) VALUES (%s, %s)",
                    (country, is_host),
                )

            for country, city in HOST_CITIES:
                cursor.execute(
                    """
                    INSERT INTO ciudades (id_pais, nombre)
                    SELECT p.id_pais, %s
                    FROM paises p
                    WHERE p.nombre = %s
                    """,
                    (city, country),
                )

            for city, stadium, capacity in HOST_STADIUMS:
                cursor.execute(
                    """
                    INSERT INTO estadios (id_ciudad, nombre, capacidad)
                    SELECT c.id_ciudad, %s, %s
                    FROM ciudades c
                    WHERE c.nombre = %s
                    """,
                    (stadium, capacity, city),
                )

            for group in GROUP_NAMES:
                cursor.execute("INSERT INTO grupos (nombre) VALUES (%s)", (group,))

            for team, country, confederation, value in TEAMS:
                cursor.execute(
                    """
                    INSERT INTO equipos (id_pais, id_confederacion, nombre, valor_mercado_total)
                    SELECT p.id_pais, c.id_confederacion, %s, %s
                    FROM paises p
                    JOIN confederaciones c ON c.nombre = %s
                    WHERE p.nombre = %s
                    """,
                    (team, value, confederation, country),
                )

                cursor.execute(
                    """
                    INSERT INTO directores_tecnicos (id_equipo, nombre_completo, nacionalidad, edad)
                    SELECT e.id_equipo, %s, %s, %s
                    FROM equipos e
                    WHERE e.nombre = %s
                    """,
                    (f"Coach {team}", country, 44 + (len(team) % 20), team),
                )

                for name, position, birthdate, height, weight, player_value in _generate_player_rows(team, confederation):
                    cursor.execute(
                        """
                        INSERT INTO jugadores (
                            id_equipo, nombre_completo, posicion, fecha_nacimiento, estatura_m, peso_kg, valor_mercado
                        )
                        SELECT e.id_equipo, %s, %s, %s, %s, %s, %s
                        FROM equipos e
                        WHERE e.nombre = %s
                        """,
                        (name, position, birthdate, height, weight, player_value, team),
                    )

            for group, team in group_rows:
                cursor.execute(
                    """
                    INSERT INTO grupo_equipos (id_grupo, id_equipo)
                    SELECT g.id_grupo, e.id_equipo
                    FROM grupos g
                    JOIN equipos e ON e.nombre = %s
                    WHERE g.nombre = %s
                    """,
                    (team, group),
                )

            for group, stadium, home, away, kick_off in match_rows:
                cursor.execute(
                    """
                    INSERT INTO partidos (
                        id_grupo, id_estadio, id_equipo_local, id_equipo_visitante, fecha_hora, fase
                    )
                    SELECT g.id_grupo, s.id_estadio, h.id_equipo, a.id_equipo, %s, 'GRUPOS'
                    FROM grupos g
                    JOIN estadios s ON s.nombre = %s
                    JOIN equipos h ON h.nombre = %s
                    JOIN equipos a ON a.nombre = %s
                    WHERE g.nombre = %s
                    """,
                    (kick_off, stadium, home, away, group),
                )

            conn.commit()
        finally:
            cursor.close()
