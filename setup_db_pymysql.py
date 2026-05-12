import pymysql
from app.database.schema import DATABASE_STATEMENTS, SCHEMA_STATEMENTS, SEED_STATEMENTS
from app.security import hash_password
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "mundial_2026"),
}

def create_connection(use_database=True):
    try:
        config = dict(DB_CONFIG)
        if not use_database:
            config.pop("database", None)
        config["auth_plugin_map"] = {"mysql_native_password": "mysql_native_password"}
        config["autocommit"] = True
        conn = pymysql.connect(**config)
        return conn
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def run_statements(statements, use_database=True):
    conn = create_connection(use_database)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        for statement in statements:
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Statement error: {statement[:50]}... -> {e}")
                cursor.close()
                conn.close()
                return False
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Execution error: {e}")
        return False

def create_admin():
    conn = create_connection(use_database=True)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios WHERE username = %s", ("admin",))
        if cursor.fetchone():
            print("Admin ya existe")
            cursor.close()
            conn.close()
            return True
        
        cursor.execute(
            """
            INSERT INTO usuarios (username, nombre_completo, password_hash, tipo_usuario, activo)
            VALUES (%s, %s, %s, 'ADMIN', 1)
            """,
            ("admin", "Administrador", hash_password("admin123")),
        )
        conn.commit()
        print("Admin creado: admin / admin123")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Admin creation error: {e}")
        return False

if __name__ == "__main__":
    print("Creando base de datos...")
    if not run_statements(DATABASE_STATEMENTS, use_database=False):
        print("Error al crear base de datos")
        exit(1)
    
    print("Creando esquema...")
    if not run_statements(SCHEMA_STATEMENTS, use_database=True):
        print("Error al crear esquema")
        exit(1)
    
    print("Insertando datos iniciales...")
    if not run_statements(SEED_STATEMENTS, use_database=True):
        print("Error al insertar datos")
        exit(1)
    
    print("Creando usuario admin...")
    if not create_admin():
        print("Error al crear admin")
        exit(1)
    
    print("\n✅ Base de datos inicializada correctamente.")
    print("Usuario inicial -> admin / admin123")
