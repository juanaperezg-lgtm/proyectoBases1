from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from app.daos import reports_dao
from app.dtos.entities import BitacoraDateRangeDTO, PlayerReportFilterDTO


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

    results = reports_dao.fetch_bitacora_entries(
        BitacoraDateRangeDTO(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    )

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

    results = reports_dao.fetch_players_for_report(
        PlayerReportFilterDTO(
            peso_min=peso_min,
            peso_max=peso_max,
            estatura_min=estatura_min,
            estatura_max=estatura_max,
            id_equipo=id_equipo,
        )
    )

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

    results = reports_dao.fetch_team_values_by_confederation(id_confederacion)

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

    results = reports_dao.fetch_host_country_participants()

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

    doc.build(elements)
    buffer.seek(0)
    return buffer
