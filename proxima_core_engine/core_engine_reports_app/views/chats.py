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
log = logging.getLogger(__name__)


    
class ChatsCsvFile(APIView):
    def get(self, request):

        tenant_id = self.request.query_params.get('tenant')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="chat_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Chat ID', 'Tenant', 'Guest Client', 'Chat Owner', 'Client Satisfaction'])

        chats = Chat.objects.filter(tenant_id=tenant_id)
        for chat in chats:
            writer.writerow([chat.chat_id, chat.tenant, chat.guest_client, chat.chat_owner, chat.client_satisfaction])

        return response


class ChatsPdfFile(APIView):
    def get(self, request):

        tenant_id = self.request.query_params.get('tenant')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="chat_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # messages = Message.objects.all()
        chats = Chat.objects.filter(tenant_id=tenant_id)
        data = []
        # for message in messages:
        #     data.append([message.message_id, message.chat_id, message.text_content, message.voice_content, message.sent_at, message.message_sender, message.escalated, message.channel, message.topic])

        for chat in chats:
            data.append([chat.chat_id, chat.tenant, chat.guest_client, chat.chat_owner, chat.client_satisfaction])

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

class MessagesCsvFile(APIView):
    def get(self, request):
        chat_id = self.request.query_params.get('chat_id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="message_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Message ID', 'Chat Id', 'Text Content', 'Voice Content', 'Sent at', 'Message Sender', 'Escalated', 'Channel', 'Topic'])

        messages = Message.objects.filter(chat_id=chat_id)
        for message in messages:
            writer.writerow([message.message_id, message.chat_id, message.text_content, message.voice_content, message.sent_at, message.message_sender, message.escalated, message.channel, message.topic])

        return response

class MessagesPdfFile(APIView):
    def get(self, request):

        chat_id = self.request.query_params.get('chat_id')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="message_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        messages = Message.objects.filter(chat_id=chat_id)
        data = []
        for message in messages:
            data.append([message.message_id, message.chat_id, message.text_content, message.voice_content, message.sent_at, message.message_sender, message.escalated, message.channel, message.topic])

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
