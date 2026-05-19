from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ConfederationCreateDTO:
    nombre: str


@dataclass(frozen=True)
class ConfederationUpdateDTO:
    id_confederacion: int
    nombre: str


@dataclass(frozen=True)
class CountryCreateDTO:
    nombre: str
    es_anfitrion: bool


@dataclass(frozen=True)
class CountryUpdateDTO:
    id_pais: int
    nombre: str
    es_anfitrion: bool


@dataclass(frozen=True)
class CityCreateDTO:
    nombre: str
    id_pais: int


@dataclass(frozen=True)
class CityUpdateDTO:
    id_ciudad: int
    nombre: str
    id_pais: int


@dataclass(frozen=True)
class StadiumCreateDTO:
    nombre: str
    capacidad: int
    id_ciudad: int


@dataclass(frozen=True)
class StadiumUpdateDTO:
    id_estadio: int
    nombre: str
    capacidad: int
    id_ciudad: int


@dataclass(frozen=True)
class TeamCreateDTO:
    nombre: str
    id_pais: int
    id_confederacion: int
    valor_mercado_total: float


@dataclass(frozen=True)
class TeamUpdateDTO:
    id_equipo: int
    nombre: str
    id_pais: int
    id_confederacion: int
    valor_mercado_total: float


@dataclass(frozen=True)
class CoachCreateDTO:
    nombre_completo: str
    nacionalidad: str
    edad: int
    id_equipo: int


@dataclass(frozen=True)
class CoachUpdateDTO:
    id_dt: int
    nombre_completo: str
    nacionalidad: str
    edad: int
    id_equipo: int


@dataclass(frozen=True)
class PlayerCreateDTO:
    nombre_completo: str
    posicion: str
    fecha_nacimiento: str
    estatura_m: float
    peso_kg: float
    valor_mercado: float
    id_equipo: int


@dataclass(frozen=True)
class PlayerUpdateDTO:
    id_jugador: int
    nombre_completo: str
    posicion: str
    fecha_nacimiento: str
    estatura_m: float
    peso_kg: float
    valor_mercado: float
    id_equipo: int


@dataclass(frozen=True)
class GroupAssignmentDTO:
    id_grupo: int
    id_equipo: int


@dataclass(frozen=True)
class MatchCreateDTO:
    id_grupo: int
    id_estadio: int
    id_equipo_local: int
    id_equipo_visitante: int
    fecha_hora: str


@dataclass(frozen=True)
class MatchUpdateDTO:
    id_partido: int
    id_grupo: int
    id_estadio: int
    id_equipo_local: int
    id_equipo_visitante: int
    fecha_hora: str


@dataclass(frozen=True)
class UserCreateDTO:
    username: str
    nombre_completo: str
    password_hash: str
    tipo_usuario: str


@dataclass(frozen=True)
class UserStatusUpdateDTO:
    id_usuario: int
    active: bool


@dataclass(frozen=True)
class BitacoraDateTimeDTO:
    fecha_hora_entrada: str
    fecha_hora_salida: str


@dataclass(frozen=True)
class PlayerReportFilterDTO:
    peso_min: float
    peso_max: float
    estatura_min: float
    estatura_max: float
    id_equipo: Optional[int] = None
