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


# from django.http import HttpResponse
# from rest_framework.views import APIView
# from tablib import Dataset
# from io import BytesIO
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas

# from core_engine_community_app.models import Issue, Comment, Thread

from io import BytesIO

from reportlab.pdfgen import canvas

from rest_framework.views import APIView
from rest_framework.response import Response

import csv
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from rest_framework.views import APIView
from core_engine_community_app.models import Issue, Comment, Thread


from core_engine_reports_app.tasks import generate_csv_issues, generate_pdf_issues
log = logging.getLogger(__name__)

"""
Trigger tasks
"""
class InitiateCsvIssueGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_csv_issues.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)

class InitiatePdfIssueGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_pdf_issues.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)  


"""
Get results from tasks
"""

class RetrievePdfIssueGeneration(APIView):


    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200) 
    
class RetrieveCsvIssueGeneration(APIView):

    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200)
    

class GenerateIssueCsvView(APIView):
    """
    BillingDetails API View
    """

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Issue.csv'

        Issue = ChatbotChat.objects.all()

        # Create a CSV writer
        writer = csv.writer(response)

        # Add column headings to CSV file
        writer.writerow(['client','chat_means','user_query','chatbot_response','escalated','client_satisfaction','topic','time'])


        # Loop through and output
        for chat in Issue:
            writer.writerow([chat.client, chat.chat_means, chat.user_query, chat.chatbot_response, chat.escalated, chat.client_satisfaction, chat.topic,chat.time])
        

        return response


class GenerateIssuePdfView(APIView):
    """
    BillingDetailss API View
    """

    def get(self, request, format=None):
        # designate our model
        Issue = ChatbotChat.objects.all()
        # Create a BysteStream Buffer
        buf = io.BytesIO()
        # Create a canavas
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        # Create a text object
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        # Add lines of text
        lines = [
        ]

        for chat in Issue:
            lines.append(chat.client)
            lines.append(chat.chat_means)
            lines.append(chat.user_query)
            lines.append(chat.chatbot_response)
            lines.append(chat.escalated)
            lines.append(chat.client_satisfaction)
            lines.append(chat.topic)
            lines.append(chat.time)
            lines.append(" ")

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='Issue.pdf')
    


# class GenerateFilesView(APIView):

#     def get(self, request):
#         # Query the models to get the data for the files
#         issues = Issue.objects.all()
#         comments = Comment.objects.all()
#         threads = Thread.objects.all()

#         # Generate CSV file
#         issue_dataset = Dataset()
#         issue_dataset.headers = ('Issue ID', 'Client ID', 'Issue', 'Community ID', 'Description', 'Solved')
#         for issue in issues:
#             issue_dataset.append((issue.issue_id, issue.client_id, issue.issue, issue.community_id, issue.description, issue.solved))

#         comment_dataset = Dataset()
#         comment_dataset.headers = ('Comment ID', 'Thread', 'Client', 'Issue', 'Likes', 'Dislikes')
#         for comment in comments:
#             comment_dataset.append((comment.comment_id, comment.thread, comment.client, comment.issue, comment.likes.count(), comment.dislikes.count()))

#         thread_dataset = Dataset()
#         thread_dataset.headers = ('Thread ID', 'Issue')
#         for thread in threads:
#             thread_dataset.append((thread.thread_id, thread.issue))

#         csv_data = {
#             'issues.csv': issue_dataset.export('csv'),
#             'comments.csv': comment_dataset.export('csv'),
#             'threads.csv': thread_dataset.export('csv')
#         }

#         # Generate PDF file
#         buffer = BytesIO()
#         pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

#         # Add the table of Issues
#         styles = getSampleStyleSheet()
#         table_style = [('GRID', (0, 0), (-1, -1), 1, colors.black)]
#         issue_table_data = [[("Issue ID"), ("Client ID"), ("Issue"),
#                              ("Community ID"), ("Description"), ("Solved")]]
#         for issue in issues:
#             issue_table_data.append([issue.issue_id, issue.client_id, issue.issue, issue.community_id, issue.description, issue.solved])
#         issue_table = Table(issue_table_data, style=table_style)
#         issue_table.wrapOn(pdf_canvas, inch, inch)
#         issue_table.drawOn(pdf_canvas, *coord(1.5, 10.2, mm))

#         # Add the table of Comments
#         comment_table_data = [[("Comment ID"), ("Thread"), ("Client"),
#                                ("Issue"), ("Likes"), ("Dislikes")]]
#         for comment in comments:
#             comment_table_data.append([comment.comment_id, comment.thread, comment.client, comment.issue, comment.likes.count(), comment.dislikes.count()])
#         comment_table = Table(comment_table_data, style=table_style)
#         comment_table.wrapOn(pdf_canvas, inch, inch)
#         comment_table.drawOn(pdf_canvas, *coord(1.5, 8.2, mm))

#         # Add the table of Threads
#         thread_table_data = [[("Thread ID"), ("Issue")]]
#         for thread in threads:
#             thread_table_data.append([thread.thread_id, thread.issue])
#         thread_table = Table(thread_table_data, style=table_style)
#         thread_table.wrapOn(pdf_canvas, inch, inch)
#         thread




# class GenerateFilesView(APIView):
#     def get(self, request, format=None):
#         issues = Issue.objects.all()

#         # Generate CSV file
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="issues.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['Issue ID', 'Client ID', 'Issue', 'Community ID', 'Description', 'Solved'])
#         for issue in issues:
#             writer.writerow([issue.issue_id, issue.client_id.client_id, issue.issue, issue.community_id.community_id,
#                              issue.description, issue.solved])

#         # Generate PDF file
#         template_path = 'issue_template.html'
#         context = {'issues': issues}
#         response_pdf = HttpResponse(content_type='application/pdf')
#         response_pdf['Content-Disposition'] = 'attachment; filename="issues.pdf"'
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response_pdf)
#         if pisa_status.err:
#             return HttpResponse('An error occurred while generating the PDF file')
#         return response





class GenerateFilesView(APIView):
    def get(self, request):
        # Get all issues and their comments
        issues = Issue.objects.all().prefetch_related('comment_set')
        
        # Create a response object for CSV file
        response_csv = HttpResponse(content_type='text/csv')
        response_csv['Content-Disposition'] = 'attachment; filename="issues.csv"'
        
        # Create a CSV writer object
        writer = csv.writer(response_csv)
        
        # Write header row
        writer.writerow(['Issue ID', 'Client ID', 'Issue', 'Community ID', 'Description', 'Solved', 'Comment ID', 'Thread ID', 'Likes', 'Dislikes'])
        
        # Write data rows
        for issue in issues:
            for comment in issue.comment_set.all():
                likes = ', '.join(str(c) for c in comment.likes.all())
                dislikes = ', '.join(str(c) for c in comment.dislikes.all())
                writer.writerow([issue.issue_id, issue.client_id.client_id, issue.issue, issue.community_id.community_id, issue.description, issue.solved, comment.comment_id, comment.thread_id, likes, dislikes])
        
        # Create a response object for PDF file
        response_pdf = HttpResponse(content_type='application/pdf')
        response_pdf['Content-Disposition'] = 'attachment; filename="issues.pdf"'
        
        # Create a PDF object
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        
        # Write PDF content
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 750, "Issues and Comments Report")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 700, "Issue ID\tClient ID\tIssue\tCommunity ID\tDescription\tSolved\tComment ID\tThread ID\tLikes\tDislikes")
        y = 680
        for issue in issues:
            for comment in issue.comment_set.all():
                likes = ', '.join(str(c) for c in comment.likes.all())
                dislikes = ', '.join(str(c) for c in comment.dislikes.all())
                data = f"{issue.issue_id}\t{issue.client_id.client_id}\t{issue.issue}\t{issue.community_id.community_id}\t{issue.description}\t{issue.solved}\t{comment.comment_id}\t{comment.thread_id}\t{likes}\t{dislikes}"
                pdf.drawString(100, y, data)
                y -= 20
        
        # Save PDF object
        pdf.save()
        
        # Set buffer position to beginning
        buffer.seek(0)
        
        # Write buffer content to PDF response
        response_pdf.write(buffer.getvalue())
        
        return response_csv
        
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

from core_engine_reports_app.tasks import generate_csv_thread, generate_pdf_thread
log = logging.getLogger(__name__)

"""
Trigger tasks
"""
class InitiateCsvThreadsGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_csv_thread.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)

class InitiatePdfThreadsGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_pdf_thread.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)  


"""
Get results from tasks
"""

class RetrievePdfThreadsGeneration(APIView):


    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200) 
    
class RetrieveCsvThreadsGeneration(APIView):

    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200)
    

class GenerateThreadsCsvView(APIView):
    """
    BillingDetails API View
    """

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Threads.csv'

        Threads = ChatbotChat.objects.all()

        # Create a CSV writer
        writer = csv.writer(response)

        # Add column headings to CSV file
        writer.writerow(['client','chat_means','user_query','chatbot_response','escalated','client_satisfaction','topic','time'])


        # Loop through and output
        for chat in Threads:
            writer.writerow([chat.client, chat.chat_means, chat.user_query, chat.chatbot_response, chat.escalated, chat.client_satisfaction, chat.topic,chat.time])
        

        return response


class GenerateThreadsPdfView(APIView):
    """
    BillingDetailss API View
    """

    def get(self, request, format=None):
        # designate our model
        Threads = ChatbotChat.objects.all()
        # Create a BysteStream Buffer
        buf = io.BytesIO()
        # Create a canavas
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        # Create a text object
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        # Add lines of text
        lines = [
        ]

        for chat in Threads:
            lines.append(chat.client)
            lines.append(chat.chat_means)
            lines.append(chat.user_query)
            lines.append(chat.chatbot_response)
            lines.append(chat.escalated)
            lines.append(chat.client_satisfaction)
            lines.append(chat.topic)
            lines.append(chat.time)
            lines.append(" ")

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='Threads.pdf')
    
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

"""
Trigger tasks
"""
class InitiateCsvChatsGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_csv_chats.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)

class InitiatePdfChatsGeneration(APIView):


    def post(self, request, format=None):

        task_type = request.data.get("type")
        task = generate_pdf_chats.delay(int(task_type))
         
        return Response({"task_id": task.id}, status=202)  


"""
Get results from tasks
"""

class RetrievePdfChatsGeneration(APIView):


    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200) 
    
class RetrieveCsvChatsGeneration(APIView):

    def post(self, request, format=None):

        task_id = request.data.get("task_id")
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }         
        return Response(result, status=200)
    

class GenerateChatsCsvView(APIView):
    """
    BillingDetails API View
    """

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=chats.csv'

        chats = ChatbotChat.objects.all()

        # Create a CSV writer
        writer = csv.writer(response)

        # Add column headings to CSV file
        writer.writerow(['client','chat_means','user_query','chatbot_response','escalated','client_satisfaction','topic','time'])


        # Loop through and output
        for chat in chats:
            writer.writerow([chat.client, chat.chat_means, chat.user_query, chat.chatbot_response, chat.escalated, chat.client_satisfaction, chat.topic,chat.time])
        

        return response


class GenerateChatsPdfView(APIView):
    """
    BillingDetailss API View
    """

    def get(self, request, format=None):
        # designate our model
        chats = ChatbotChat.objects.all()
        # Create a BysteStream Buffer
        buf = io.BytesIO()
        # Create a canavas
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        # Create a text object
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        # Add lines of text
        lines = [
        ]

        for chat in chats:
            lines.append(chat.client)
            lines.append(chat.chat_means)
            lines.append(chat.user_query)
            lines.append(chat.chatbot_response)
            lines.append(chat.escalated)
            lines.append(chat.client_satisfaction)
            lines.append(chat.topic)
            lines.append(chat.time)
            lines.append(" ")

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='chats.pdf')
    


class ChatDataExportView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="chat_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Chat ID', 'Tenant', 'Guest Client', 'Chat Owner', 'Client Satisfaction'])

        chats = Chat.objects.all()
        for chat in chats:
            writer.writerow([chat.chat_id, chat.tenant, chat.guest_client, chat.chat_owner, chat.client_satisfaction])

        return response


class MessageDataExportView(View):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="message_data.pdf"'

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        messages = Message.objects.all()
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
