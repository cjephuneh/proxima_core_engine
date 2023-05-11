from django.http import JsonResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from core_engine_chat_app.models import Message, Chat

class CountEscalatedIssues(APIView):
    """
    A view to count the number of escalated messages for a given tenant.
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Message.objects.filter(escalated=True, chat_id__tenant_id=tenant)
        count = queryset.aggregate(count=Count('message_id'))['count']
        response_data = {"count": count}

        return JsonResponse(response_data, status=status.HTTP_200_OK)
