from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_chat_app.models import Message, Chat


from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from core_engine_chat_app.models import Message, Chat

class LeastEngagedTopics(APIView):

    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all chats for the given tenant
        chats = Chat.objects.filter(tenant_id=tenant_id)

        # Group messages by topic and count the number of messages for each topic
        topics = Message.objects.filter(chat_id__in=chats) \
                                .values('topic') \
                                .annotate(topic_count=Count('topic')) \
                                .order_by('topic_count')

        # Get the topic(s) with the least number of messages
        least_engaged_topics = []
        min_topic_count = topics.first()['topic_count'] if topics else 0
        for topic in topics:
            if topic['topic_count'] == min_topic_count:
                least_engaged_topics.append(topic['topic'])
            else:
                break

        return Response({'least_engaged_topics': least_engaged_topics}, status=status.HTTP_200_OK)
