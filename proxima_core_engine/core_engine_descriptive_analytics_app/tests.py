from django.test import TestCase

# Create your tests here.
import json
from django.urls import reverse
from rest_framework import status

def test_count_all_chats(client):
    tenant_id = 1
    url = reverse('count_all_chats') + f'?tenant={tenant_id}'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {'count': 3}


from django.urls import reverse
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_cumulative_count_all_hourly_chats(client, create_tenant, create_chat):
    url = reverse('cumulative_count_all_hourly_chats')
    tenant_id = str(create_tenant().id)

    # Test case 1: Missing tenant ID
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test case 2: Valid request
    response = client.get(f"{url}?tenant={tenant_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 24

    for item in data:
        assert isinstance(item, dict)


import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_cumulative_voice_messages():
    # create some test data
    tenant = Tenant.objects.create(name='Test Tenant')
    chat = Chat.objects.create(tenant=tenant, chat_owner=client)
    Message.objects.create(chat_id=chat, text_content='Test message', voice_content=b'Test voice note')
    
    # send a GET request to the view
    client = APIClient()
    url = reverse('cumulative-voice-messages')
    response = client.get(url, {'tenant': tenant.pk})
    
    # assert that the response is as expected
    assert response.status_code == 200
    assert response.json() == {'total_voice_size': 13}  # size of test voice note is 13 bytes

from django.urls import reverse
from rest_framework import status

def test_count_all_hourly_chats(api_client, create_chat):
    tenant_id = create_chat.tenant.id
    url = reverse('count_hourly_chats')

    # Test case when tenant is not provided
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test case when there are no chats for the given tenant
    response = api_client.get(url, {'tenant': tenant_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'total_chats_last_hour': 0}

    # Test case when there are chats for the given tenant
    create_chat(date_time_created_at=timezone.now() - timezone.timedelta(minutes=30))
    response = api_client.get(url, {'tenant': tenant_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'total_chats_last_hour': 1}

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_average_voice_message_per_chat():
    # Create a tenant and some chats with voice messages
    tenant = Tenant.objects.create(name='Test Tenant')
    chat1 = Chat.objects.create(tenant=tenant, chat_owner_id=1)
    chat2 = Chat.objects.create(tenant=tenant, chat_owner_id=2)
    Message.objects.create(chat_id=chat1, voice_content='voice1.mp3')
    Message.objects.create(chat_id=chat1, voice_content='voice2.mp3')
    Message.objects.create(chat_id=chat2, voice_content='voice3.mp3')

    # Test the view
    url = reverse('average-voice-messages-per-chat')
    client = APIClient()
    response = client.get(url, {'tenant': tenant.id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'average_voice_messages_per_chat': 1.5}

    # Test with a tenant that has no voice messages
    tenant2 = Tenant.objects.create(name='Test Tenant 2')
    response = client.get(url, {'tenant': tenant2.id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'average_voice_messages_per_chat': None}

    # Test without the 'tenant' query parameter
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'error': 'Missing query parameter: tenant'}



"""
Community
"""
import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_average_comments_per_thread():
    # Create some test data
    community = Community.objects.create(name='Test Community')
    tenant = Tenant.objects.create(name='Test Tenant')
    issue = Issue.objects.create(community=community, tenant=tenant)
    thread1 = Thread.objects.create(issue=issue)
    thread2 = Thread.objects.create(issue=issue)
    Comment.objects.create(thread=thread1)
    Comment.objects.create(thread=thread1)
    Comment.objects.create(thread=thread2)

    # Make a GET request to the view
    client = APIClient()
    url = reverse('average-comments-per-thread')
    params = {'community': community.id, 'tenant': tenant.id}
    response = client.get(url, params)

    # Check that the response has the expected status code and data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'avg_comments_per_thread': 1.5}


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CommentsUserRelationTestCase(APITestCase):
    def test_unique_comment_count(self):
        thread = Thread.objects.create(issue=Issue.objects.create(client_id=1))
        Comment.objects.create(thread=thread, client_id=1)
        Comment.objects.create(thread=thread, client_id=2)
        Comment.objects.create(thread=thread, client_id=1)
        url = reverse('comments-user-relation')
        response = self.client.get(url, {'thread_id': thread.thread_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 2})



from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class CommunityGrowthRateTest(TestCase):

    def setUp(self):
        self.community = Community.objects.create(community_name='Test Community')
        self.client1 = Client.objects.create(username='user1', email='user1@example.com')
        self.client2 = Client.objects.create(username='user2', email='user2@example.com')
        self.community.members.add(self.client1, self.client2)
        self.event1 = Event.objects.create(type='Join', description='user1 joined the community', client=self.client1, community=self.community)
        self.event2 = Event.objects.create(type='Join', description='user2 joined the community', client=self.client2, community=self.community)

    def test_community_growth_rate(self):
        url = reverse('community_growth_rate')
        response = self.client.get(url, {'community_id': self.community.community_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'Community growth rate: 100.00%')


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CommunityMembersTestCase(APITestCase):

    def test_community_members(self):
        community = Community.objects.create(community_name='Test Community')
        client1 = Client.objects.create(name='Client 1')
        client2 = Client.objects.create(name='Client 2')
        community.members.add(client1, client2)

        url = reverse('community-members')
        response = self.client.get(url, {'community': community.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'community': 'Test Community', 'member_count': 2})

    def test_community_members_invalid_id(self):
        url = reverse('community-members')
        response = self.client.get(url, {'community': 'invalid_id'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_community_members_missing_id(self):
        url = reverse('community-members')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Community ID is required.'})


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

def test_community_rating(api_client):
    url = reverse('community-rating')
    response = api_client.get(url, {'community': 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'count': 3.5}

def test_community_rating_invalid_community(api_client):
    url = reverse('community-rating')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'error': 'community ID is required'}


import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CumulativeCommentsTestCase(APITestCase):

    def test_cumulative_comments(self):
        # Create a community and some threads/comments
        # ...

        # Make a GET request to the CumulativeComments view
        url = reverse('cumulative-comments')
        response = self.client.get(url, {'community': community_id})

        # Check that the response is valid
        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.json()
        assert response.json()['count'] == expected_count


import json
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from core_engine_community_app.models import Thread, Comment

class UniqueCommentsTestCase(TestCase):
    def setUp(self):
        # Create some test data
        self.thread = Thread.objects.create(...)
        self.client = Client.objects.create(...)
        self.issue = Issue.objects.create(...)
        self.comment1 = Comment.objects.create(client=self.client, thread=self.thread, issue=self.issue, metadata={"text": "Comment 1"})
        self.comment2 = Comment.objects.create(client=self.client, thread=self.thread, issue=self.issue, metadata={"text": "Comment 2"})

    def test_unique_comments(self):
        # Test that we get unique comments for a given client and community
        client_id = self.client.id
        community_id = self.issue.community_id.id
        client = APIClient()
        response = client.get(reverse('unique-comments') + f'?community={community_id}&client={client_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1) # Expecting one unique comment
        self.assertEqual(data[0]['fields']['metadata']['text'], 'Comment 1')


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CumulativeIssuesTests(APITestCase):
    
    def setUp(self):
        self.community1 = Community.objects.create(
            community_name='Community 1',
            tenant_id=1
        )
        self.community2 = Community.objects.create(
            community_name='Community 2',
            tenant_id=2
        )
        self.issue1 = Issue.objects.create(
            client_id=1,
            issue='Issue 1',
            community_id=self.community1.id
        )
        self.issue2 = Issue.objects.create(
            client_id=2,
            issue='Issue 2',
            community_id=self.community1.id
        )
        self.issue3 = Issue.objects.create(
            client_id=3,
            issue='Issue 3',
            community_id=self.community2.id
        )
    
    def test_get_cumulative_issues_success(self):
        url = reverse('cumulative-issues')
        response = self.client.get(url, {'community': self.community1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 2})
        
    def test_get_cumulative_issues_missing_community(self):
        url = reverse('cumulative-issues')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Community ID is required.'})


from django.urls import reverse
from rest_framework.test import APITestCase

class IssueUserRelationTest(APITestCase):
    def test_get_unique_issues(self):
        community = Community.objects.create(community_name='Test Community')
        client1 = Client.objects.create(name='Client 1')
        client2 = Client.objects.create(name='Client 2')
        issue1 = Issue.objects.create(client_id=client1, issue='Test Issue 1',
                                      community_id=community)
        issue2 = Issue.objects.create(client_id=client2, issue='Test Issue 2',
                                      community_id=community)
        issue3 = Issue.objects.create(client_id=client1, issue='Test Issue 3',
                                      community_id=community)
        
        url = reverse('issue_user_relation')
        response = self.client.get(url, {'community': community.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
