from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.decorators import action

from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import Transaction
from datetime import datetime

from .permissions import (
    CanReadTransactionPermission,
    CanCreateTransactionPermission,
    CanDeleteTransactionPermission,
    CanUpdateTransactionPermission,
)
from .models import Transaction
from .serializers import TransactionSerializer

import os


# Create your views here.
class TransactionViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    permission_classes = [
        CanReadTransactionPermission,
        CanCreateTransactionPermission,
        CanUpdateTransactionPermission,
    ]

    def list(self, request):
        objs = Transaction.objects.all()
        serializer = TransactionSerializer(objs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"transaction_id": serializer.data.get("transaction_id")}, status=201
            )
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        serializer = TransactionSerializer(obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        serializer = TransactionSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        try:
            obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        serializer = TransactionSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            obj = Transaction.objects.get(pk=pk)
            obj.delete()
            return Response({"message": "Transaction deleted successfully"}, status=204)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

    def get_permissions(self):
        """
        Apply specific permissions for different actions.
        """
        permissions = super().get_permissions()

        if self.action == "destroy":
            permissions = [CanDeleteTransactionPermission()]

        return permissions


class PDFTransactionListAPIView(views.APIView):

    def get(self, request):
        # Create HTTP response with PDF content type
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="transaction_list.pdf"'

        # Create the PDF canvas object
        p = canvas.Canvas(response, pagesize=letter)

        # Add header logo (adjust path as per your static file setup)
        logo_path = os.path.join(
            settings.BASE_DIR, "static", "images", "logo.jpg"
        )  # Adjust path if necessary
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 40, 700, width=100, height=100)

        # Table header
        headers = [
            "Transaction ID",
            "Name",
            "Phone",
            "Email",
            "Amount",
            "Transaction Date",
        ]

        transactions = Transaction.objects.filter(status=Transaction.Status.APPROVED)

        x = 40
        y = 650
        row_height = 18
        col_widths = [80, 80, 100, 100, 80, 100]

        # Draw table header
        p.setFont("Helvetica-Bold", 10)
        for col_num, header in enumerate(headers):
            p.setFillColor(colors.white)
            p.rect(
                x + sum(col_widths[:col_num]),
                y,
                col_widths[col_num],
                row_height,
                fill=1,
                stroke=1,
            )
            p.setFillColor(colors.black)
            p.drawString(x + sum(col_widths[:col_num]) + 5, y + 5, header)
        y -= row_height

        p.setFont("Helvetica", 9)
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
                y = 750

        p.showPage()
        p.save()

        return response


class PDFTransactionAPIView(views.APIView):

    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)

        if transaction.status != Transaction.Status.APPROVED:
            return Response({"error": "Transaction not approved."}, status=400)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="transaction_{pk}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)

        logo_path = os.path.join(settings.BASE_DIR, "static", "images", "logo.jpg")
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 40, 700, width=100, height=100)

        p.setFont("Helvetica-Bold", 12)
        table_data = [
            ["Transaction ID", transaction.transaction_id],
            ["Name", transaction.name],
            ["Phone", transaction.phone],
            ["Email", transaction.email],
            ["Amount", str(transaction.amount)],
            ["Transaction Date", str(transaction.transaction_date)],
        ]

        x = 40
        y = 650
        row_height = 20
        col_widths = [230, 300]

        for row in table_data:
            p.setFont("Helvetica", 10)
            p.rect(x, y, col_widths[0], row_height, fill=0, stroke=1)
            p.rect(x + col_widths[0], y, col_widths[1], row_height, fill=0, stroke=1)

            p.drawString(x + 5, y + 5, row[0])
            p.drawString(x + col_widths[0] + 5, y + 5, row[1])
            y -= row_height

            if y < 100:
                p.showPage()
                y = 750

        p.showPage()
        p.save()

        return response
