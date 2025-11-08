from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime


def generate_invoice_pdf(payment):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=12,
    )
    
    normal_style = styles['Normal']
    
    title = Paragraph("INVOICE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    company_data = [
        ["Global Swift Courier", ""],
        ["123 Logistics Avenue", f"Invoice #: {payment.invoice_number}"],
        ["New York, NY 10001", f"Date: {payment.created_at.strftime('%B %d, %Y')}"],
        ["Phone: +1 (555) 123-4567", f"Payment ID: {payment.id}"],
    ]
    
    company_table = Table(company_data, colWidths=[3*inch, 3*inch])
    company_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))
    
    elements.append(company_table)
    elements.append(Spacer(1, 0.4*inch))
    
    bill_to = Paragraph(f"<b>Bill To:</b>", header_style)
    elements.append(bill_to)
    elements.append(Paragraph(f"{payment.user.get_full_name_or_username()}", normal_style))
    elements.append(Paragraph(f"{payment.user.email}", normal_style))
    elements.append(Paragraph(f"{payment.user.phone or 'N/A'}", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    items_header = Paragraph("<b>Items</b>", header_style)
    elements.append(items_header)
    
    item_data = [
        ['Description', 'Tracking #', 'Amount'],
        [
            payment.get_payment_type_display_full(),
            payment.parcel.tracking_number,
            f"${payment.amount:.2f}"
        ],
    ]
    
    items_table = Table(item_data, colWidths=[3*inch, 2*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    total_data = [
        ['Subtotal:', f'${payment.amount:.2f}'],
        ['Tax (0%):', '$0.00'],
        ['Total:', f'${payment.amount:.2f}'],
    ]
    
    total_table = Table(total_data, colWidths=[5*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (-1, 2), 14),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#2563EB')),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.black),
    ]))
    
    elements.append(total_table)
    elements.append(Spacer(1, 0.5*inch))
    
    footer_text = """
    <para alignment="center">
    <b>Thank you for your business!</b><br/>
    For questions about this invoice, please contact support@globalswift.com
    </para>
    """
    elements.append(Paragraph(footer_text, normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_receipt_pdf(payment):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#10B981'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    elements.append(Paragraph("PAYMENT RECEIPT", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    receipt_data = [
        ["Receipt Number:", payment.receipt_number],
        ["Payment Date:", payment.updated_at.strftime('%B %d, %Y at %I:%M %p')],
        ["Payment Method:", payment.get_provider_display()],
        ["Transaction ID:", payment.transaction_id or 'N/A'],
        ["Amount Paid:", f"${payment.amount:.2f} {payment.currency}"],
        ["Status:", payment.get_status_display()],
    ]
    
    receipt_table = Table(receipt_data, colWidths=[2.5*inch, 3.5*inch])
    receipt_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
    ]))
    
    elements.append(receipt_table)
    elements.append(Spacer(1, 0.5*inch))
    
    confirmation_text = f"""
    <para alignment="center" fontSize="14">
    <b>✓ Payment Confirmed</b><br/><br/>
    This receipt confirms your payment for parcel <b>{payment.parcel.tracking_number}</b>.<br/>
    Your payment has been processed successfully.<br/><br/>
    Thank you for choosing Global Swift Courier!
    </para>
    """
    elements.append(Paragraph(confirmation_text, styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
