import json
import pytest
# import datetime
from datetime import timedelta
from datetime import datetime
from rest_framework import status
from django.urls import reverse
from core_engine_chat_app.models import Chat, Message
from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_users_app.models import Client as TestClient
from django.test import TestCase

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def tenant():
    return Tenant.objects.create(tenant_name="Test Tenant")

@pytest.fixture
def test_client():
    return TestClient.objects.create(first_name="Test Client")

@pytest.fixture
def chat(tenant, test_client):
    return Chat.objects.create(tenant=tenant, chat_owner=test_client)

@pytest.fixture
def message(chat, test_client):
    return Message.objects.create(chat_id=chat, chat_owner=test_client, escalated=True)


"""
Count all chats test
"""
@pytest.fixture
def count_chats_url():
    return reverse('analytics_urls:core_analytics_countchats')

@pytest.mark.django_db
def test_count_all_chats(api_client, count_chats_url, chat):
    response = api_client.get(count_chats_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert 'chat_count' in response_data

    chat_count = response_data['chat_count']
    assert chat_count == 1

@pytest.mark.django_db
def test_no_tenant_id(api_client, count_chats_url):
    response = api_client.get(count_chats_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'

"""
Count hourly chats
"""
@pytest.fixture
def count_hourly_chats_url():
    return reverse('analytics_urls:core_analytics_cumulativehourlychats')

@pytest.mark.django_db
def test_count_hourly_chats(api_client, count_hourly_chats_url, chat):
    response = api_client.get(count_hourly_chats_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_cumulative_hourly_chats_no_tenant_id(api_client, count_hourly_chats_url):
    response = api_client.get(count_hourly_chats_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
Cumullative Voice messages
"""
@pytest.fixture
def count_cumulative_voice_messages_url():
    return reverse('analytics_urls:core_analytics_cumulativevoicemessage')

@pytest.mark.django_db
def test_cumulative_voice_messages(api_client, count_cumulative_voice_messages_url, chat):
    response = api_client.get(count_cumulative_voice_messages_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_cumulative_voice_messages_no_tenant_id(api_client, count_cumulative_voice_messages_url):
    response = api_client.get(count_cumulative_voice_messages_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



"""
Hourly Chats
"""
@pytest.fixture
def last_hourly_chats_url():
    return reverse('analytics_urls:core_analytics_counthourlychats')

@pytest.mark.django_db
def test_last_hourly_chats(api_client, last_hourly_chats_url, chat):
    response = api_client.get(last_hourly_chats_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_last_hourly_chats_no_tenant_id(api_client, last_hourly_chats_url):
    response = api_client.get(last_hourly_chats_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'

"""
Average Voice Message Per Chat
"""
@pytest.fixture
def voice_messages_per_chat_url():
    return reverse('analytics_urls:core_analytics_averagevoicemessageperchat')

@pytest.mark.django_db
def test_voice_messages_per_chat(api_client, voice_messages_per_chat_url, chat):
    response = api_client.get(voice_messages_per_chat_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_voice_messages_per_chat_no_tenant_id(api_client, voice_messages_per_chat_url):
    response = api_client.get(voice_messages_per_chat_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
CountEscalated Issues
"""
@pytest.fixture
def count_escalated_issues_url():
    return reverse('analytics_urls:core_analytics_countescalatedissues')

@pytest.mark.django_db
def escalated_issues(api_client, count_escalated_issues_url, chat):
    response = api_client.get(count_escalated_issues_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def escalated_issues_no_tenant_id(api_client, count_escalated_issues_url):
    response = api_client.get(count_escalated_issues_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
Hourly Count Escalated Issues
"""
@pytest.fixture
def count_hourly_escalated_issues_url():
    return reverse('analytics_urls:core_analytics_hourlycountescalatedissues')

@pytest.mark.django_db
def hourly_escalated_issues(api_client, count_hourly_escalated_issues_url, chat):
    response = api_client.get(count_hourly_escalated_issues_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def tenant_escalated_issues_no_tenant_id(api_client, count_hourly_escalated_issues_url):
    response = api_client.get(count_hourly_escalated_issues_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



"""

UTILS
"""

"""
Communication Channels
"""
@pytest.fixture
def communication_channels_url():
    return reverse('analytics_urls:core_analytics_communicationchannels')

@pytest.mark.django_db
def test_communictation_channels(api_client, communication_channels_url, chat):
    response = api_client.get(communication_channels_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_ommunication_cahhenls_no_tenant_id(api_client, communication_channels_url):
    response = api_client.get(communication_channels_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
Engagement Frequency
"""
@pytest.fixture
def test_engagement_frequency_url():
    return reverse('analytics_urls:core_analytics_engagementfrequency')

@pytest.mark.django_db
def test_engagement_frequency(api_client, test_engagement_frequency_url, chat):
    response = api_client.get(test_engagement_frequency_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_engagement_frequency_no_tenant_id(api_client, test_engagement_frequency_url):
    response = api_client.get(test_engagement_frequency_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



"""
Least engaged topics
"""
@pytest.fixture
def least_engaged_topics_url():
    return reverse('analytics_urls:core_analytics_leasttopics')

@pytest.mark.django_db
def test_least_engaged_topics(api_client, least_engaged_topics_url, chat):
    response = api_client.get(least_engaged_topics_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_least_engaged_topics_no_tenant_id(api_client, least_engaged_topics_url):
    response = api_client.get(least_engaged_topics_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



"""
Hourly Count Escalated Issues
"""
@pytest.fixture
def hourly_average_response_time_url():
    return reverse('analytics_urls:core_analytics_hourlyaverageresponsetime')

@pytest.mark.django_db
def test_hourly_average_response_time(api_client, hourly_average_response_time_url, chat):
    response = api_client.get(hourly_average_response_time_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_hourly_average_response_time_no_tenant_id(api_client, hourly_average_response_time_url):
    response = api_client.get(hourly_average_response_time_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



"""
Client Hourly ClientSatisfaction
"""
@pytest.fixture
def client_hourly_satisfaction_url():
    return reverse('analytics_urls:core_analytics_hourly_clientsatisfaction')

@pytest.mark.django_db
def test_client_hourly_satisfaction(api_client, client_hourly_satisfaction_url, chat):
    response = api_client.get(client_hourly_satisfaction_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_client_hourly_satisfaction_no_tenant_id(api_client, client_hourly_satisfaction_url):
    response = api_client.get(client_hourly_satisfaction_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'

"""
Client Satisfaction
"""
@pytest.fixture
def client_satisfaction_url():
    return reverse('analytics_urls:core_analytics_clientsatisfaction')

# @pytest.mark.django_db
# def test_client_satisfaction(api_client, client_satisfaction_url, chat):
#     response = api_client.get(client_satisfaction_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
#     assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_client_satisfaction_no_tenant_id(api_client, client_satisfaction_url):
    response = api_client.get(client_satisfaction_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
MostPopularTopics
"""
@pytest.fixture
def count_most_popular_topics_url():
    return reverse('analytics_urls:core_analytics_populartopics')

@pytest.mark.django_db
def test_most_popular_topics(api_client, count_most_popular_topics_url, chat):
    response = api_client.get(count_most_popular_topics_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_most_popular_topics_no_tenant_id(api_client, count_most_popular_topics_url):
    response = api_client.get(count_most_popular_topics_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'