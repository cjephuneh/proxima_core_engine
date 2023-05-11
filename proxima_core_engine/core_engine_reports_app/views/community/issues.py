from core_engine_chat_app.models import Chat, Message
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
import io
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv
# from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import uuid
import logging
from celery.result import AsyncResult
import csv
from io import BytesIO
from django.http import HttpResponse
from django.views.generic import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from core_engine_community_app.models import Issue
from core_engine_reports_app.tasks import generate_csv_chats, generate_pdf_chats
log = logging.getLogger(__name__)


    
class IssuesCsvFile(APIView):
    def get(self, request):

        community_id = self.request.query_params.get('community_id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="issue_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Issue ID', 'Client ID', 'Issue', 'Community ID', 'Description', 'Solved'])

        issues = Issue.objects.filter(community_id=community_id)
        for issue in issues:
            writer.writerow([issue.issue_id, issue.client_id, issue.issue, issue.community_id, issue.description, issue.solved])

        return response


class IssuesPdfFile(APIView):
    def get(self, request):

        community_id = self.request.query_params.get('community_id')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="issues_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        issues = Issue.objects.filter(community_id=community_id)
        data = []
        for issue in issues:
            data.append([issue.issue_id, issue.client_id, issue.issue, issue.community_id, issue.description, issue.solved])

        # Create the table
        if data:
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ]))

            elements.append(table)
            # Write the PDF to the buffer
            doc.build(elements)
            response.write(buffer.getvalue())
            buffer.close()

        else:
            response.write(buffer.getvalue())
            buffer.close()


        return response

