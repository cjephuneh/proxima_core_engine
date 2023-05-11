from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.db.models import F
from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework import status
from core_engine_community_app.models import Community, Event

class CommunityGrowthRate(APIView):

    def get(self, request):

        community = request.query_params.get('community')
        # try:
        #     community = Community.objects.get(community_id=community_id)
        # except Community.DoesNotExist:
        #     return HttpResponse({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not community:
            return JsonResponse({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the latest event for the community
        latest_event = Event.objects.filter(community=community).order_by('-timestamp').first()

        if latest_event:
            # Calculate the time difference between the current time and the latest event time
            time_diff = datetime.now() - latest_event.timestamp
            # Get the total number of members in the community before the latest event
            prev_members_count = latest_event.community.members.count() - 1
            # Get the current number of members in the community
            current_members_count = community.members.count() - 1
            # Calculate the percentage growth rate
            growth_rate = ((current_members_count - prev_members_count) / prev_members_count) * 100
            # Return the growth rate as a JSON response
            return HttpResponse(f"Community growth rate: {Decimal(growth_rate).quantize(Decimal('.01'))}%", content_type='application/json', status=status.HTTP_200_OK)
        else:
            # Return 0% growth rate if there are no events in the community
            return HttpResponse("Community growth rate: 0%", content_type='application/json', status=status.HTTP_200_OK)
