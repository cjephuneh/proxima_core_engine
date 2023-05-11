from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_community_app.models import Comment


class CommentsUserRelation(APIView):

    def get(self, request):

        thread_id = self.request.query_params.get('thread')

        if not thread_id:
            return JsonResponse({'error': 'No Thread provided'}, status=status.HTTP_400_BAD_REQUEST)

        unique_comment_count = Comment.objects.filter(thread_id=thread_id).values('client').distinct().count()
        return JsonResponse({'count': unique_comment_count}, status=status.HTTP_200_OK)

