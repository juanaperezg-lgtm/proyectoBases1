from app.database.connection import get_connection, run_statements
from app.database.realistic_seed import seed_realistic_data
from app.database.schema import DATABASE_STATEMENTS, SCHEMA_STATEMENTS, SEED_STATEMENTS
from app.security import hash_password


def create_admin() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_usuario FROM usuarios WHERE username = %s", ("admin",))
            if cursor.fetchone():
                return
            cursor.execute(
                """
                INSERT INTO usuarios (username, nombre_completo, password_hash, tipo_usuario, activo)
                VALUES (%s, %s, %s, 'ADMIN', 1)
                """,
                ("admin", "Administrador", hash_password("admin123")),
            )
            conn.commit()
        finally:
            cursor.close()


def main() -> None:
    run_statements(DATABASE_STATEMENTS, use_database=False)
    run_statements(SCHEMA_STATEMENTS, use_database=True)
    run_statements(SEED_STATEMENTS, use_database=True)
    seed_realistic_data()
    create_admin()
    print("Base de datos inicializada correctamente.")
    print("Usuario inicial -> admin / admin123")


if __name__ == "__main__":
    main()
