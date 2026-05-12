# Aplicación de Gestión - Mundial de Fútbol 2026

Aplicación de escritorio en Python/Tkinter para la gestión completa de datos del Mundial de Fútbol 2026.

## Características

### 1. **Sistema de Autenticación**
- Login con 3 tipos de usuarios:
  - **Admin**: Acceso total (CRUD de datos, usuarios, consultas, reportes)
  - **Usuario Tradicional**: CRUD de datos + consultas + reportes
  - **Usuario Esporádico**: Solo lectura (consultas y reportes)
- Bitácora de entrada/salida para todos los usuarios
- Contraseñas hasheadas con PBKDF2-SHA256

### 2. **Gestión de Datos (CRUD)**
Panel de administración con 9 módulos CRUD:
- **Confederaciones**: Gestión de confederaciones (AFC, CAF, CONMEBOL, CONCACAF, UEFA, OFC)
- **Países**: Gestión de países con flag de anfitrión
- **Ciudades**: Ciudades por país anfitrión
- **Estadios**: Estadios con capacidad y ubicación
- **Equipos**: Equipos con país, confederación y valor de mercado
- **Directores Técnicos**: DT por equipo con edad y nacionalidad
- **Jugadores**: Jugadores con posición, peso, estatura, fecha nacimiento y valor
- **Grupos**: Asignación de equipos a 12 grupos (A-L)
- **Partidos**: Programación de partidos con grupo, estadio, equipos y fecha/hora,

### 3. **Consultas SQL**
4 consultas predefinidas con interfaz gráfica:
1. **Jugador más costoso por confederación** - Identifica el jugador más valioso de cada confederación
2. **Partidos por estadio** - Lista todos los partidos en un estadio específico
3. **Equipo más costoso por país anfitrión** - Equipo con mayor valor en México, USA, Canadá
4. **Jugadores menores de 21 años por equipo** - Cantidad de jugadores jóvenes por equipo

### 4. **Reportes PDF**
4 reportes generables en PDF:
1. **Bitácora de Sesiones** - Entrada/salida de usuarios por rango de fechas
2. **Jugadores Filtrados** - Filtro por peso, estatura y equipo
3. **Valor por Equipo** - Valor total de jugadores por equipo de una confederación
4. **Países Anfitriones** - Países participantes en cada país anfitrión

## Requisitos

- Python 3.8+
- MySQL Server
- Dependencias (ver `requirements.txt`)

## Instalación

### 1. Clonar/descargar el proyecto
```bash
cd proyecto-bases
```

### 2. Crear base de datos
```bash
python setup_db.py
```
**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (opcional)
Crear archivo `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=mundial_2026
```

### 5. Ejecutar la aplicación
```bash
python run.py
```

## Estructura del Proyecto

```
proyecto-bases/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuración de BD
│   ├── security.py               # Hashing de contraseñas
│   ├── database/
│   │   ├── connection.py         # Conexión a MySQL
│   │   └── schema.py             # Esquema y seed
│   ├── services/                 # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── confederations_service.py
│   │   ├── countries_service.py
│   │   ├── cities_service.py
│   │   ├── stadiums_service.py
│   │   ├── teams_service.py
│   │   ├── coaches_service.py
│   │   ├── players_service.py
│   │   ├── groups_service.py
│   │   ├── matches_service.py
│   │   └── reports_service.py
│   └── ui/                       # Interfaz gráfica
│       ├── login_window.py
│       ├── main_window.py
│       ├── users_view.py
│       ├── confederations_view.py
│       ├── countries_view.py
│       ├── cities_view.py
│       ├── stadiums_view.py
│       ├── teams_view.py
│       ├── coaches_view.py
│       ├── players_view.py
│       ├── groups_view.py
│       ├── matches_view.py
│       ├── queries_view.py
│       └── reports_view.py
├── run.py                        # Punto de entrada
├── setup_db.py                   # Inicialización de BD
└── requirements.txt              # Dependencias
```

## Base de Datos

### Tablas principales:
- `usuarios` - Usuarios del sistema con autenticación
- `bitacora_sesiones` - Registro de entrada/salida
- `confederaciones` - 6 confederaciones mundiales
- `paises` - Países (3 anfitriones + participantes)
- `ciudades` - Ciudades anfitrionas
- `estadios` - Estadios con capacidad
- `equipos` - 48 equipos
- `directores_tecnicos` - DT por equipo (1:1)
- `jugadores` - Jugadores por equipo
- `grupos` - 12 grupos (A-L)
- `grupo_equipos` - Asignación equipos a grupos
- `partidos` - Partidos de grupos

## Tipos de Usuario

### 1. Admin
- ✅ Crear usuarios
- ✅ CRUD completo de datos
- ✅ Consultas
- ✅ Reportes

### 2. Usuario Tradicional
- ❌ No crea usuarios
- ✅ CRUD de datos
- ✅ Consultas
- ✅ Reportes

### 3. Usuario Esporádico
- ❌ No crea usuarios
- ❌ No CRUD
- ✅ Solo consultas
- ✅ Solo reportes

## Funcionalidades Técnicas

### Seguridad
- Contraseñas hasheadas con PBKDF2-SHA256 (120k iteraciones)
- Sistema de permisos basado en roles
- Bitácora completa de sesiones

### UI
- Interfaz gráfica con Tkinter
- Formularios CRUD intuitivos
- Treeviews para visualización de datos
- Combobox con autocomplete

### Reportes
- PDF con ReportLab
- Tablas formateadas
- Múltiples filtros

### Base de Datos
- MySQL con caracteres UTF-8mb4
- Claves foráneas para integridad referencial
- Índices para búsquedas rápidas

## Notas de Desarrollo

- La aplicación NO usa frameworks (solo Tkinter nativo)
- MySQL connector Python 9.3.0
- ReportLab 4.4.1 para PDFs
- Compatible con Python 3.8+
- Validación de datos en formularios

## Autor
Proyecto Final - Bases de Datos I
Universidad del Quindío
