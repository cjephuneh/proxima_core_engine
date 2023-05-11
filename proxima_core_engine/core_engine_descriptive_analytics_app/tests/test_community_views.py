import json
import pytest
# import datetime
from datetime import timedelta
from datetime import datetime
from rest_framework import status
from django.urls import reverse
from core_engine_chat_app.models import Chat
from core_engine_tenant_management_app.models import Tenant
from core_engine_community_app.models import Community, Issue, Thread, Comment
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
def community(tenant):
    return Community.objects.create(tenant_id=tenant)

@pytest.fixture
def test_client():
    return TestClient.objects.create(first_name="Test Client")

@pytest.fixture
def issue(test_client, community):
    return Issue.objects.create(community_id=community, client_id=test_client)

@pytest.fixture
def thread(issue, test_client):
    return Thread.objects.create(issue=issue)


@pytest.fixture
def comments(thread, test_client):
    return Comment.objects.create(thread=thread, client=test_client)


"""
Count Comments per thread
"""
@pytest.fixture
def count_comments_url():
    return reverse('analytics_urls:core_analytics_averagecomments')

@pytest.mark.django_db
def test_comments_per_thread(api_client, count_comments_url, community):
    response = api_client.get(count_comments_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_comments_per_thread_no_tenant_id(api_client, count_comments_url):
    response = api_client.get(count_comments_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'



"""
Comments User Relation
"""
@pytest.fixture
def count_comments_user_relation_url():
    return reverse('analytics_urls:core_analytics_commentsuserrelation')

@pytest.mark.django_db
def test_comments_user_relationthread(api_client, count_comments_user_relation_url, thread):
    response = api_client.get(count_comments_user_relation_url, {'thread': thread.thread_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_comments_user_relationthread_no_tenant_id(api_client, count_comments_user_relation_url):
    response = api_client.get(count_comments_user_relation_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Thread provided'


"""
Community Growth Rate
"""
@pytest.fixture
def count_community_growth_rate_url():
    return reverse('analytics_urls:core_analytics_communitygrowthrate')

@pytest.mark.django_db
def test_community_growth_rate(api_client, count_community_growth_rate_url, community):
    response = api_client.get(count_community_growth_rate_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_community_growth_rate_no_tenant_id(api_client, count_community_growth_rate_url):
    response = api_client.get(count_community_growth_rate_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'

"""
Community Members
"""
@pytest.fixture
def count_community_members_url():
    return reverse('analytics_urls:core_analytics_communitymembers')

@pytest.mark.django_db
def test_community_members(api_client, count_community_members_url, community):
    response = api_client.get(count_community_members_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_community_members_no_community_id(api_client, count_community_members_url):
    response = api_client.get(count_community_members_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'

"""
Community Rating
"""
@pytest.fixture
def community_rating_url():
    return reverse('analytics_urls:core_analytics_communityrating')

@pytest.mark.django_db
def test_community_rating(api_client, community_rating_url, community):
    response = api_client.get(community_rating_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_community_rating_no_community_id(api_client, community_rating_url):
    response = api_client.get(community_rating_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'

"""
Cumulative Comments
"""
@pytest.fixture
def count_cumulative_comments_url():
    return reverse('analytics_urls:core_analytics_cumulativecomments')

@pytest.mark.django_db
def test_cumulative_comments(api_client, count_cumulative_comments_url, community):
    response = api_client.get(count_cumulative_comments_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_cumulative_comments_no_community_id(api_client, count_cumulative_comments_url):
    response = api_client.get(count_cumulative_comments_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'


"""
Issue User Relation
"""
@pytest.fixture
def issue_user_relation_url():
    return reverse('analytics_urls:core_analytics_issueuserrelation')

@pytest.mark.django_db
def test_issue_user_relation(api_client, issue_user_relation_url, community):
    response = api_client.get(issue_user_relation_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_issue_user_relation_no_community_id(api_client, issue_user_relation_url):
    response = api_client.get(issue_user_relation_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'


"""
Cumulative Issues
"""
@pytest.fixture
def cumulative_issues_url():
    return reverse('analytics_urls:core_analytics_averagecomments')

@pytest.mark.django_db
def test_cumulative_issues(api_client, count_comments_url, community):
    response = api_client.get(count_comments_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_cumulative_issues_no_community_id(api_client, count_comments_url):
    response = api_client.get(count_comments_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'


"""
Unique Comments
"""
@pytest.fixture
def unique_comments_url():
    return reverse('analytics_urls:core_analytics_uniquecomments')

@pytest.mark.django_db
def test_unique_comments(api_client, unique_comments_url, community):
    response = api_client.get(unique_comments_url, {'community': community.community_id}) # Use pk instead of object
    assert response.status_code == status.HTTP_200_OK

    # response_data = json.loads(response.content)
    # assert 'chat_count' in response_data

    # chat_count = response_data['chat_count']
    # assert chat_count == 1

@pytest.mark.django_db
def test_unique_comments_no_community_id(api_client, unique_comments_url):
    response = api_client.get(unique_comments_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = json.loads(response.content)
    assert 'error' in response_data
    assert response_data['error'] == 'No Community provided'