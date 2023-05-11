import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_community_app.models import Issue
from core_engine_community_app.serializers import IssueSerializer
from core_engine_community_app.utils import save_community_issue
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class IssueView(APIView):
    """
    Communitys API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Communitys matching query.

        Params:
        issue_id
        community_id
        client_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'issue_id': 'issue_id',
            'community_id': 'community_id',
            'client_id': 'client_id'
        }
        filters = get_filter_from_params(params, allowed_params)

        issue_query = Issue.objects.select_related('community_id').filter(**filters)
        issue_set = IssueSerializer(issue_query, many=True)
        return Response(issue_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a issue to the database.

        Params:
        issue_id
        community_id
        """
        issue, created = save_community_issue(**request.data)
        if not issue:
            return Response(status=400)
        
        issue_info = IssueSerializer(issue)
        if created:
            return Response(issue_info.data, status=201)
        else:
            return Response(issue_info.data, status=200)

