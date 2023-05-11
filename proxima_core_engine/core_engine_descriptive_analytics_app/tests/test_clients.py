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
from core_engine_users_profile_app.models import ClientProfile
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

@pytest.fixture
def clientprofile(chat, test_client):
    return  ClientProfile.objects.create(client=test_client,
        profile_photo="test_client.jpg",
        country="USA",
        county="Los Angeles",
        city="Los Angeles",
        postal_code="90001")


"""
Clients Average Age
"""
@pytest.fixture
def clients_average_age_url():
    return reverse('analytics_urls:core_analytics_clientsaverageage')

@pytest.mark.django_db
def test_clients_average_age(api_client, clients_average_age_url, chat):
    response = api_client.get(clients_average_age_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_clients_average_age_no_tenant_id(api_client, clients_average_age_url):
    response = api_client.get(clients_average_age_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'

"""
City Distribution
"""
@pytest.fixture
def city_distribution_url():
    return reverse('analytics_urls:core_analytics_clientcitydistribution')

@pytest.mark.django_db
def test_city_distribution(api_client, city_distribution_url, chat):
    response = api_client.get(city_distribution_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_city_distribution_no_tenant_id(api_client, city_distribution_url):
    response = api_client.get(city_distribution_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
Country Distribution
"""
@pytest.fixture
def country_distribution_url():
    return reverse('analytics_urls:core_analytics_countrydistribution')

@pytest.mark.django_db
def test_country_distribution(api_client, country_distribution_url, chat):
    response = api_client.get(country_distribution_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_country_distribution_no_tenant_id(api_client, country_distribution_url):
    response = api_client.get(country_distribution_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
Gender Distribution
"""
@pytest.fixture
def gender_distribution_url():
    return reverse('analytics_urls:core_analytics_genderdistribution')

@pytest.mark.django_db
def test_gender_distribution(api_client, gender_distribution_url, chat):
    response = api_client.get(gender_distribution_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_gender_distribution_no_tenant_id(api_client, gender_distribution_url):
    response = api_client.get(gender_distribution_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'


"""
State Distribution
"""
@pytest.fixture
def state_distribution_url():
    return reverse('analytics_urls:core_analytics_statedistribution')

@pytest.mark.django_db
def test_state_distribution_url(api_client, state_distribution_url, chat):
    response = api_client.get(state_distribution_url, {'tenant': chat.tenant.tenant_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_state_distribution_url_no_tenant_id(api_client, state_distribution_url):
    response = api_client.get(state_distribution_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No tenant provided'



