"""
Test Suite para la aplicación de gestión del Mundial 2026
Prueba todas las funcionalidades requeridas sin afectar la aplicación
"""

import sys
import os
from datetime import datetime, timedelta
import traceback

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import get_connection
from app import services
import app.services.confederations_service as confederations_service
import app.services.countries_service as countries_service
import app.services.cities_service as cities_service
import app.services.stadiums_service as stadiums_service
import app.services.teams_service as teams_service
import app.services.coaches_service as coaches_service
import app.services.players_service as players_service
import app.services.groups_service as groups_service
import app.services.matches_service as matches_service
import app.services.user_service as user_service
from app.services.auth_service import authenticate


class TestReport:
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0

    def add_test(self, name, status, details=""):
        self.tests.append({
            "name": name,
            "status": status,
            "details": details
        })
        if status == "✅ PASSED":
            self.passed += 1
        else:
            self.failed += 1

    def print_report(self):
        print("\n" + "="*80)
        print("TEST SUITE REPORT - MUNDIAL 2026 APPLICATION")
        print("="*80 + "\n")
        
        for test in self.tests:
            print(f"{test['status']} - {test['name']}")
            if test['details']:
                print(f"   └─ {test['details']}\n")

        print("="*80)
        print(f"TOTAL: {self.passed} PASSED | {self.failed} FAILED")
        print("="*80)


def test_database_connection():
    """Prueba conexión a la base de datos"""
    report = TestReport()
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            report.add_test("Database Connection", "✅ PASSED", "Conectado a MySQL correctamente")
        return report
    except Exception as e:
        report.add_test("Database Connection", "❌ FAILED", str(e))
        return report


def test_authentication():
    """Prueba el sistema de autenticación"""
    report = TestReport()
    
    try:
        # Test login correcto
        result = authenticate("admin", "admin123")
        if result[0] is not None:
            user_id, nombre = result
            report.add_test("Login Admin", "✅ PASSED", f"Usuario: admin autenticado correctamente")
        else:
            report.add_test("Login Admin", "❌ FAILED", "Credenciales no válidas")
        
        # Test login incorrecto
        result = authenticate("admin", "wrongpassword")
        if result[0] is None:
            report.add_test("Login Invalid Credentials", "✅ PASSED", "Rechazó credenciales inválidas")
        else:
            report.add_test("Login Invalid Credentials", "❌ FAILED", "Aceptó credenciales inválidas")
            
    except Exception as e:
        report.add_test("Authentication", "❌ FAILED", str(e))
        traceback.print_exc()
    
    return report


def test_crud_operations():
    """Prueba operaciones CRUD para todas las entidades"""
    report = TestReport()
    
    try:
        # Test Confederaciones
        confederations = confederations_service.list_confederations()
        if confederations and len(confederations) > 0:
            report.add_test("CRUD: Get All Confederations", "✅ PASSED", f"Encontradas {len(confederations)} confederaciones")
        else:
            report.add_test("CRUD: Get All Confederations", "❌ FAILED", "No se encontraron confederaciones")
        
        # Test Países
        countries = countries_service.list_countries()
        if countries and len(countries) > 0:
            report.add_test("CRUD: Get All Countries", "✅ PASSED", f"Encontrados {len(countries)} países")
        else:
            report.add_test("CRUD: Get All Countries", "❌ FAILED", "No se encontraron países")
        
        # Test Ciudades
        cities = cities_service.list_cities()
        if cities and len(cities) > 0:
            report.add_test("CRUD: Get All Cities", "✅ PASSED", f"Encontradas {len(cities)} ciudades")
        else:
            report.add_test("CRUD: Get All Cities", "❌ FAILED", "No se encontraron ciudades")
        
        # Test Estadios
        stadiums = stadiums_service.list_stadiums()
        if stadiums and len(stadiums) > 0:
            report.add_test("CRUD: Get All Stadiums", "✅ PASSED", f"Encontrados {len(stadiums)} estadios")
        else:
            report.add_test("CRUD: Get All Stadiums", "❌ FAILED", "No se encontraron estadios")
        
        # Test Equipos
        teams = teams_service.list_teams()
        if teams and len(teams) > 0:
            report.add_test("CRUD: Get All Teams", "✅ PASSED", f"Encontrados {len(teams)} equipos")
        else:
            report.add_test("CRUD: Get All Teams", "❌ FAILED", "No se encontraron equipos")
        
        # Test Directores Técnicos
        coaches = coaches_service.list_coaches()
        if coaches and len(coaches) > 0:
            report.add_test("CRUD: Get All Coaches", "✅ PASSED", f"Encontrados {len(coaches)} directores técnicos")
        else:
            report.add_test("CRUD: Get All Coaches", "❌ FAILED", "No se encontraron directores técnicos")
        
        # Test Jugadores
        players = players_service.list_players()
        if players and len(players) > 0:
            report.add_test("CRUD: Get All Players", "✅ PASSED", f"Encontrados {len(players)} jugadores")
        else:
            report.add_test("CRUD: Get All Players", "❌ FAILED", "No se encontraron jugadores")
        
        # Test Grupos
        groups = groups_service.list_groups()
        if groups and len(groups) > 0:
            report.add_test("CRUD: Get All Groups", "✅ PASSED", f"Encontrados {len(groups)} grupos")
        else:
            report.add_test("CRUD: Get All Groups", "❌ FAILED", "No se encontraron grupos")
        
        # Test Partidos
        matches = matches_service.list_matches()
        if matches and len(matches) > 0:
            report.add_test("CRUD: Get All Matches", "✅ PASSED", f"Encontrados {len(matches)} partidos")
        else:
            report.add_test("CRUD: Get All Matches", "❌ FAILED", "No se encontraron partidos")
            
    except Exception as e:
        report.add_test("CRUD Operations", "❌ FAILED", str(e))
        traceback.print_exc()
    
    return report


def test_queries():
    """Prueba todas las consultas requeridas"""
    report = TestReport()
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            
            # CONSULTA 1: Jugador más costoso por confederación
            print("\n[TESTING QUERIES]")
            query1 = """
            SELECT c.nombre AS confederacion, j.nombre_completo, j.valor_mercado
            FROM jugadores j
            JOIN equipos e ON j.id_equipo = e.id_equipo
            JOIN confederaciones c ON e.id_confederacion = c.id_confederacion
            WHERE j.valor_mercado = (
                SELECT MAX(j2.valor_mercado)
                FROM jugadores j2
                JOIN equipos e2 ON j2.id_equipo = e2.id_equipo
                WHERE e2.id_confederacion = c.id_confederacion
            )
            ORDER BY c.nombre;
            """
            
            cursor.execute(query1)
            result = cursor.fetchall()
            if result and len(result) > 0:
                report.add_test(
                    "QUERY 1: Jugador más costoso por confederación",
                    "✅ PASSED",
                    f"Encontrados {len(result)} resultados"
                )
            else:
                report.add_test(
                    "QUERY 1: Jugador más costoso por confederación",
                    "❌ FAILED",
                    "No se retornaron resultados"
                )
            
            # CONSULTA 2: Partidos por estadio
            query2 = """
            SELECT s.nombre, COUNT(p.id_partido) as cantidad_partidos
            FROM estadios s
            LEFT JOIN partidos p ON s.id_estadio = p.id_estadio
            GROUP BY s.id_estadio, s.nombre
            ORDER BY s.nombre;
            """
            
            cursor.execute(query2)
            result = cursor.fetchall()
            if result and len(result) > 0:
                report.add_test(
                    "QUERY 2: Partidos por estadio",
                    "✅ PASSED",
                    f"Encontrados {len(result)} estadios con sus partidos"
                )
            else:
                report.add_test(
                    "QUERY 2: Partidos por estadio",
                    "❌ FAILED",
                    "No se retornaron resultados"
                )
            
            # CONSULTA 3: Equipo más costoso por país anfitrión
            query3 = """
            SELECT p.nombre AS pais, e.nombre AS equipo, SUM(j.valor_mercado) as valor_total
            FROM equipos e
            JOIN jugadores j ON e.id_equipo = j.id_equipo
            JOIN paises p ON e.id_pais = p.id_pais
            WHERE p.es_anfitrion = 1
            GROUP BY p.id_pais, p.nombre, e.id_equipo, e.nombre
            HAVING valor_total = (
                SELECT MAX(total_valor)
                FROM (
                    SELECT SUM(j2.valor_mercado) as total_valor
                    FROM equipos e2
                    JOIN jugadores j2 ON e2.id_equipo = j2.id_equipo
                    WHERE e2.id_pais = p.id_pais
                    GROUP BY e2.id_equipo
                ) as subquery
            )
            ORDER BY p.nombre;
            """
            
            cursor.execute(query3)
            result = cursor.fetchall()
            if result and len(result) > 0:
                report.add_test(
                    "QUERY 3: Equipo más costoso por país anfitrión",
                    "✅ PASSED",
                    f"Encontrados {len(result)} equipos"
                )
            else:
                report.add_test(
                    "QUERY 3: Equipo más costoso por país anfitrión",
                    "❌ FAILED",
                    "No se retornaron resultados"
                )
            
            # CONSULTA 4: Jugadores menores de 21 años por equipo
            query4 = """
            SELECT e.nombre AS equipo, COUNT(j.id_jugador) as jugadores_menores_21
            FROM equipos e
            LEFT JOIN jugadores j ON e.id_equipo = j.id_equipo 
                AND YEAR(CURDATE()) - YEAR(j.fecha_nacimiento) < 21
            GROUP BY e.id_equipo, e.nombre
            ORDER BY e.nombre;
            """
            
            cursor.execute(query4)
            result = cursor.fetchall()
            if result and len(result) > 0:
                report.add_test(
                    "QUERY 4: Jugadores menores de 21 años por equipo",
                    "✅ PASSED",
                    f"Encontrados {len(result)} equipos con conteo de menores de 21"
                )
            else:
                report.add_test(
                    "QUERY 4: Jugadores menores de 21 años por equipo",
                    "❌ FAILED",
                    "No se retornaron resultados"
                )
            
            cursor.close()
        
    except Exception as e:
        report.add_test("Queries", "❌ FAILED", str(e))
        traceback.print_exc()
    
    return report


def test_reports():
    """Prueba funcionalidades de reportes"""
    report = TestReport()
    
    try:
        from app.services.reports_service import (
            generate_bitacora_report,
            generate_players_report,
            generate_team_value_report,
            generate_host_countries_report
        )
        
        # Test bitácora de sesiones
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            pdf_data = generate_bitacora_report(start_date, end_date)
            if pdf_data and pdf_data.getbuffer().nbytes > 0:
                report.add_test(
                    "REPORT 1: Bitácora de sesiones",
                    "✅ PASSED",
                    f"PDF generado ({pdf_data.getbuffer().nbytes} bytes)"
                )
            else:
                report.add_test(
                    "REPORT 1: Bitácora de sesiones",
                    "⚠️ PARTIAL",
                    "PDF retornó contenido vacío"
                )
        except Exception as e:
            report.add_test(
                "REPORT 1: Bitácora de sesiones",
                "❌ FAILED",
                str(e)[:80]
            )
        
        # Test jugadores filtrados
        try:
            pdf_data = generate_players_report(70, 90, 1.70, 1.90)
            if pdf_data and pdf_data.getbuffer().nbytes > 0:
                report.add_test(
                    "REPORT 2: Jugadores filtrados",
                    "✅ PASSED",
                    f"PDF generado ({pdf_data.getbuffer().nbytes} bytes)"
                )
            else:
                report.add_test(
                    "REPORT 2: Jugadores filtrados",
                    "⚠️ PARTIAL",
                    "PDF retornó contenido vacío"
                )
        except Exception as e:
            report.add_test(
                "REPORT 2: Jugadores filtrados",
                "❌ FAILED",
                str(e)[:80]
            )
        
        # Test valor por equipo
        try:
            pdf_data = generate_team_value_report(1)
            if pdf_data and pdf_data.getbuffer().nbytes > 0:
                report.add_test(
                    "REPORT 3: Valor total por equipo y confederación",
                    "✅ PASSED",
                    f"PDF generado ({pdf_data.getbuffer().nbytes} bytes)"
                )
            else:
                report.add_test(
                    "REPORT 3: Valor total por equipo y confederación",
                    "⚠️ PARTIAL",
                    "PDF retornó contenido vacío"
                )
        except Exception as e:
            report.add_test(
                "REPORT 3: Valor total por equipo y confederación",
                "❌ FAILED",
                str(e)[:80]
            )
        
        # Test países por anfitrión
        try:
            pdf_data = generate_host_countries_report()
            if pdf_data and pdf_data.getbuffer().nbytes > 0:
                report.add_test(
                    "REPORT 4: Países por país anfitrión",
                    "✅ PASSED",
                    f"PDF generado ({pdf_data.getbuffer().nbytes} bytes)"
                )
            else:
                report.add_test(
                    "REPORT 4: Países por país anfitrión",
                    "⚠️ PARTIAL",
                    "PDF retornó contenido vacío"
                )
        except Exception as e:
            report.add_test(
                "REPORT 4: Países por país anfitrión",
                "❌ FAILED",
                str(e)[:80]
            )
            
    except Exception as e:
        report.add_test("Reports", "❌ FAILED", str(e))
        traceback.print_exc()
    
    return report


def test_user_management():
    """Prueba gestión de usuarios"""
    report = TestReport()
    
    try:
        # Verificar que exista admin
        users = user_service.list_users()
        if users and len(users) > 0:
            admin_exists = any(u.get('tipo_usuario') == "ADMIN" for u in users)
            if admin_exists:
                report.add_test(
                    "USER: Admin exists",
                    "✅ PASSED",
                    f"Total usuarios: {len(users)}, Admin existe"
                )
            else:
                report.add_test(
                    "USER: Admin exists",
                    "❌ FAILED",
                    "Admin no existe"
                )
        else:
            report.add_test(
                "USER: Get all users",
                "❌ FAILED",
                "No se encontraron usuarios"
            )
            
    except Exception as e:
        report.add_test("User Management", "❌ FAILED", str(e))
        traceback.print_exc()
    
    return report


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*80)
    print("INICIANDO TEST SUITE - MUNDIAL 2026")
    print("="*80 + "\n")
    
    all_reports = []
    
    # Test 1: Conexión
    print("[1/6] Probando conexión a base de datos...")
    report = test_database_connection()
    report.print_report()
    all_reports.append(report)
    
    # Test 2: Autenticación
    print("\n[2/6] Probando autenticación...")
    report = test_authentication()
    report.print_report()
    all_reports.append(report)
    
    # Test 3: CRUD
    print("\n[3/6] Probando operaciones CRUD...")
    report = test_crud_operations()
    report.print_report()
    all_reports.append(report)
    
    # Test 4: Consultas
    print("\n[4/6] Probando consultas SQL requeridas...")
    report = test_queries()
    report.print_report()
    all_reports.append(report)
    
    # Test 5: Reportes
    print("\n[5/6] Probando funcionalidades de reportes...")
    report = test_reports()
    report.print_report()
    all_reports.append(report)
    
    # Test 6: Gestión de usuarios
    print("\n[6/6] Probando gestión de usuarios...")
    report = test_user_management()
    report.print_report()
    all_reports.append(report)
    
    # Resumen final
    total_passed = sum(r.passed for r in all_reports)
    total_failed = sum(r.failed for r in all_reports)
    
    print("\n" + "="*80)
    print("RESUMEN FINAL DEL TEST SUITE")
    print("="*80)
    print(f"Total PASSED: {total_passed}")
    print(f"Total FAILED: {total_failed}")
    print(f"Total TESTS: {total_passed + total_failed}")
    print("="*80 + "\n")
    
    return total_passed, total_failed


if __name__ == "__main__":
    try:
        passed, failed = run_all_tests()
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        traceback.print_exc()
        sys.exit(1)
