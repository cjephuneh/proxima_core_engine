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

from core_engine_reports_app.tasks import generate_csv_chats, generate_pdf_chats
from core_engine_survey_app.models import Survey, Response as ResponseModel

log = logging.getLogger(__name__)


    
class SurveyCsvFile(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant_id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="survey_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Survey ID', 'Tenant', 'Survey Topic', 'Survey Description', 'Survey Context', 'Survey Questions', 'Target Audience', 'Survey Type', 'Start Day', 'End Day'])

        surveys = Survey.objects.filter(tenant_id=tenant_id)
        for survey in surveys:
            writer.writerow([survey.survey_id, survey.tenant_id, survey.survey_topic, survey.survey_description, survey.survey_context, survey.survey_questions, survey.target_audience, survey.survey_type, survey.start_day, survey.end_day])

        return response


class SurveyPdfFile(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant_id')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="message_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        surveys = Survey.objects.filter(tenant_id=tenant_id)
        data = []
        for survey in surveys:
            data.append([survey.survey_id, survey.tenant_id, survey.survey_topic, survey.survey_description, survey.survey_context, survey.survey_questions, survey.target_audience, survey.survey_type, survey.start_day, survey.end_day])

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

class surveyResponsesCsvFile(APIView):
    def get(self, request):
        survey_id = self.request.query_params.get('survey_id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="chat_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Response ID', 'Survey', 'Client', 'Chat Owner', 'Response'])

        surveys = ResponseModel.objects.filter(survey_id=survey_id)
        for survey in surveys:
            writer.writerow([survey.response_id, survey.survey_id, survey.client, survey.survey_response])

        return response

class SurveyResponsesPdfFile(APIView):
    def get(self, request):
        survey_id = self.request.query_params.get('survey_id')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="message_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        surveys = ResponseModel.objects.filter(survey_id=survey_id)
        data = []
        for survey in surveys:
            data.append([survey.response_id, survey.survey_id, survey.client, survey.survey_response])

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
