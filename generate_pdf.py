from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


def generate_portfolio_pdf(name, age, occupation, risk, portfolio):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    
    GOLD = colors.HexColor("#C9A84C")
    BLACK = colors.HexColor("#0A0A0A")
    DARK = colors.HexColor("#161616")
    LIGHT = colors.HexColor("#E8E0D0")
    DIM = colors.HexColor("#8A8070")

    styles = getSampleStyleSheet()

   
    title_style = ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName="Helvetica",
        fontSize=12,
        textColor=DIM,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "Heading",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=GOLD,
        spaceAfter=8,
        spaceBefore=16
    )

    body_style = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
        leading=16
    )

    label_style = ParagraphStyle(
        "Label",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=DIM,
        spaceAfter=2
    )

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=DIM,
        leading=12,
        spaceAfter=6
    )

    elements = []

   
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("PortfolioIQ", title_style))
    elements.append(Paragraph("Smart Investing for India", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    elements.append(Spacer(1, 0.5*cm))

   
    elements.append(Paragraph("Investment Portfolio Report", heading_style))
    elements.append(Paragraph(f"Personalised for <b>{name}</b>", body_style))

    
    user_data = [
        ["Name", name],
        ["Age", age],
        ["Occupation", occupation.replace("_", " ").title()],
        ["Risk Appetite", risk.title()],
    ]

    user_table = Table(user_data, colWidths=[4*cm, 12*cm])
    user_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F5F0E8")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#8A8070")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#111111")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUND", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0D8C8")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(user_table)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E0D8C8")))

    
    elements.append(Paragraph(f"Recommended Portfolio: {portfolio['name']}", heading_style))
    elements.append(Paragraph(portfolio["description"], body_style))
    elements.append(Spacer(1, 0.3*cm))

    
    stats_data = [
        ["Risk Level", "Expected Return", "Asset Classes"],
        [portfolio["risk_level"], portfolio["expected_return"], str(len(portfolio["allocation"]))],
    ]

    stats_table = Table(stats_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C9A84C")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FDF8F0")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#111111")),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 12),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0D8C8")),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(stats_table)
    elements.append(Spacer(1, 0.5*cm))

    
    elements.append(Paragraph("Asset Allocation Breakdown", heading_style))

    alloc_data = [["Asset Class", "Allocation %", "Recommended Fund"]]
    for item in portfolio["allocation"]:
        alloc_data.append([item["asset"], f"{item['percent']}%", item["example"]])

    alloc_table = Table(alloc_data, colWidths=[5*cm, 3*cm, 8.5*cm])
    alloc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111111")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#C9A84C")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ROWBACKGROUND", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#111111")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0D8C8")),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#C9A84C")),
    ]))

    elements.append(alloc_table)
    elements.append(Spacer(1, 1*cm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E0D8C8")))
    elements.append(Spacer(1, 0.3*cm))

    
    elements.append(Paragraph(
        "<b>Disclaimer:</b> This portfolio report is for educational and informational purposes only and does not constitute personalised financial advice. Past performance is not indicative of future results. Please consult a SEBI-registered investment adviser before making any investment decisions.",
        disclaimer_style
    ))

    elements.append(Paragraph("Generated by PortfolioIQ", disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer