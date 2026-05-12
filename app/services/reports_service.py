from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from app.database.connection import get_connection


def generate_bitacora_report(fecha_inicio: str, fecha_fin: str) -> BytesIO:
    """Genera reporte PDF de bitácora de sesiones"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=1,
    )

    elements.append(Paragraph("Reporte de Bitácora de Sesiones", title_style))
    elements.append(Spacer(1, 0.2 * inch))

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
                (fecha_inicio, fecha_fin),
            )
            results = cursor.fetchall()

            if not results:
                elements.append(Paragraph("No hay registros para el período especificado.", styles['Normal']))
            else:
                data = [["Usuario", "Entrada", "Salida"]]
                for row in results:
                    entrada = str(row["fecha_hora_entrada"]) if row["fecha_hora_entrada"] else "-"
                    salida = str(row["fecha_hora_salida"]) if row["fecha_hora_salida"] else "-"
                    data.append([row["nombre_completo"], entrada, salida])

                table = Table(data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                elements.append(table)
        finally:
            cursor.close()

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_players_report(peso_min: float, peso_max: float, estatura_min: float,
                           estatura_max: float, id_equipo: int = None) -> BytesIO:
    """Genera reporte PDF de jugadores filtrados"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=20,
        alignment=1,
    )

    elements.append(Paragraph("Reporte de Jugadores Filtrados", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            if id_equipo:
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
                    (peso_min, peso_max, estatura_min, estatura_max, id_equipo),
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
                    (peso_min, peso_max, estatura_min, estatura_max),
                )
            
            results = cursor.fetchall()

            if not results:
                elements.append(Paragraph("No hay jugadores que coincidan con los filtros.", styles['Normal']))
            else:
                data = [["Jugador", "Posición", "Estatura (m)", "Peso (kg)", "Valor Mercado", "Equipo"]]
                for row in results:
                    data.append([
                        row["nombre_completo"],
                        row["posicion"],
                        f"{row['estatura_m']:.2f}",
                        f"{row['peso_kg']:.2f}",
                        f"${row['valor_mercado']:,.2f}",
                        row["equipo"],
                    ])

                table = Table(data, colWidths=[1.8*inch, 1*inch, 1.2*inch, 1*inch, 1.5*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                elements.append(table)
        finally:
            cursor.close()

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_team_value_report(id_confederacion: int) -> BytesIO:
    """Genera reporte PDF de valor total de jugadores por equipo"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=20,
        alignment=1,
    )

    elements.append(Paragraph("Reporte de Valor Total de Jugadores por Equipo", title_style))
    elements.append(Spacer(1, 0.2 * inch))

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
            results = cursor.fetchall()

            if not results:
                elements.append(Paragraph("No hay datos para esta confederación.", styles['Normal']))
            else:
                data = [["Equipo", "Cantidad Jugadores", "Valor Total"]]
                total_valor = 0
                for row in results:
                    valor = row["valor_total"] or 0
                    total_valor += valor
                    data.append([
                        row["equipo"],
                        str(row["cantidad_jugadores"]),
                        f"${valor:,.2f}",
                    ])

                data.append(["TOTAL", "", f"${total_valor:,.2f}"])

                table = Table(data, colWidths=[3*inch, 2*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                elements.append(table)
        finally:
            cursor.close()

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_host_countries_report() -> BytesIO:
    """Genera reporte PDF de países que jugarán en cada país anfitrión"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=20,
        alignment=1,
    )

    elements.append(Paragraph("Países que Jugarán en Cada País Anfitrión", title_style))
    elements.append(Spacer(1, 0.2 * inch))

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
            results = cursor.fetchall()

            if not results:
                elements.append(Paragraph("No hay datos disponibles.", styles['Normal']))
            else:
                paises_anfitrion = {}
                for row in results:
                    pais = row["pais_anfitrion"]
                    if pais not in paises_anfitrion:
                        paises_anfitrion[pais] = []
                    paises_anfitrion[pais].append(row["pais_equipo"])

                for pais_host in sorted(paises_anfitrion.keys()):
                    elementos = sorted(set(paises_anfitrion[pais_host]))
                    elements.append(Paragraph(f"<b>{pais_host}</b>", styles['Heading2']))
                    
                    data = [["País Participante"]]
                    for pais_eq in elementos:
                        data.append([pais_eq])

                    table = Table(data, colWidths=[4*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 0.3 * inch))
        finally:
            cursor.close()

    doc.build(elements)
    buffer.seek(0)
    return buffer
