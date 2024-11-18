from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from datetime import datetime

from django.conf import settings
import os


def generate_pdf(transactions):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(settings.BASE_DIR, "transactions", "static", "pdf", f"/transaction_report_{timestamp}.pdf")


    p = canvas.Canvas(file_path, pagesize=A4)

    logo_path = os.path.join(settings.BASE_DIR, "static", "images", "logo.avif")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 40, 750, width=120, height=60)

    p.setFont("Helvetica", 14)
    p.drawString(200, 770, "Transaction Report")

    headers = ["Transaction ID", "Name", "Phone", "Email", "Amount", "Date"]

    x = 40
    y = 700
    row_height = 20
    col_widths = [100, 120, 100, 150, 80, 100]

    p.setFont("Helvetica-Bold", 10)
    for col_num, header in enumerate(headers):
        p.rect(
            x + sum(col_widths[:col_num]),
            y,
            col_widths[col_num],
            row_height,
            fill=1,
            stroke=1,
        )
        p.setFillColor(colors.white)
        p.drawString(x + sum(col_widths[:col_num]) + 5, y + 5, header)
    y -= row_height

    p.setFont("Helvetica", 10)
    for transaction in transactions:
        data = [
            transaction.transaction_id,
            transaction.name,
            transaction.phone,
            transaction.email,
            str(transaction.amount),
            str(transaction.transaction_date),
        ]

        for col_num, item in enumerate(data):
            p.rect(
                x + sum(col_widths[:col_num]),
                y,
                col_widths[col_num],
                row_height,
                fill=0,
                stroke=1,
            )
            p.drawString(x + sum(col_widths[:col_num]) + 5, y + 5, item)

        y -= row_height

        if y < 100:
            p.showPage()
            y = 700

    p.showPage()
    p.save()
