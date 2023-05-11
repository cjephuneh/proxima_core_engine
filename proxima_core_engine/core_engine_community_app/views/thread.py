import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_community_app.models import Thread
from core_engine_community_app.serializers import ThreadSerializer
from core_engine_community_app.utils import save_issue_thread
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class ThreadView(APIView):
    """
    Threads API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Threads matching query.

        Params:
        thread_id
        issue
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'thread_id': 'thread_id',
            'issue': 'issue',
        }
        filters = get_filter_from_params(params, allowed_params)

        thread_query = Thread.objects.select_related('issue').filter(**filters)
        thread_set = ThreadSerializer(thread_query, many=True)
        return Response(thread_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a thread to the database.

        Params:
        thread_id
        issue
        """
        thread, created = save_issue_thread(**request.data)
        if not thread:
            return Response(status=400)
        
        thread_info = ThreadSerializer(thread)
        if created:
            return Response(thread_info.data, status=201)
        else:
            return Response(thread_info.data, status=200)


