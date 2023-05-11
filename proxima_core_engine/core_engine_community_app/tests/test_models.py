import pytest
from django.utils import timezone
from core_engine_tenant_users_app.models import Client
from django.core.exceptions import ObjectDoesNotExist
from core_engine_community_app.models import Community, Event, Rating, Issue, Thread, Comment
from core_engine_tenant_management_app.models import Tenant


from core_engine_tenant_users_app.models import Client
from core_engine_chat_app.models import (Chat, Message)

@pytest.fixture
def tenant():
    return Tenant.objects.create(tenant_name="Test Tenant")

@pytest.fixture
def client():
    return Client.objects.create(first_name="Test Client")


@pytest.fixture()
def community():
    tenant_id = Tenant.objects.create(tenant_name="Test Tenant")
    community_name = "Test Community"
    description = "A test community"
    community = Community.objects.create(tenant_id=tenant_id,
                                          community_name=community_name,
                                          description=description)
    return community

@pytest.fixture()
def client():
    username = "testuser"
    password = "testpassword"
    client = Client.objects.create(username=username, password=password)
    return client

@pytest.mark.django_db
def test_community_string_representation(community):
    assert str(community) == str(community.community_id)

@pytest.mark.django_db
def test_add_client_to_community(community):
    client = Client.objects.create(first_name="Test Client")
    event = community.add_client_to_community(client)
    assert community.members.filter(id=client.id).exists()
    assert community.event_set.filter(type="Join", client=client, timestamp=event.timestamp).exists()

@pytest.mark.django_db
def test_remove_client_from_community(community):
    client = Client.objects.create(first_name="Test Client")
    event = community.add_client_to_community(client)
    event2 = community.remove_client_from_community(client)
    assert not community.members.filter(id=client.id).exists()
    assert community.event_set.filter(type="Left", client=client, timestamp=event2.timestamp).exists()


@pytest.mark.django_db
def test_remove_client_from_non_existent_community(community, client):
    with pytest.raises(ObjectDoesNotExist):
        non_existent_community_id = community.community_id + 1
        non_existent_community = Community.objects.get(pk=non_existent_community_id)
        non_existent_community.remove_client_from_community(client)



@pytest.mark.django_db
def test_event_model():
    tenant = Tenant.objects.create(tenant_name="test tenant")
    client = Client.objects.create(email="test@test.com")
    community = Community.objects.create(
        community_name="test community",
        tenant_id=tenant,
        description="test description",
    )
    event = Event.objects.create(
        type="Join",
        client=client,
        timestamp=timezone.now(),
        community=community,
    )
    assert str(event) == f"{client} Join the {tenant} group"


@pytest.mark.django_db
def test_rating_model():
    tenant = Tenant.objects.create(tenant_name="test tenant")
    client = Client.objects.create(email="test@test.com")
    community = Community.objects.create(
        community_name="test community",
        tenant_id=tenant,
        description="test description",
    )
    rating = Rating.objects.create(
        community_id=community,
        client_id=client,
        rating=5,
    )
    assert str(rating) == str(rating.rating_id)


@pytest.mark.django_db
def test_issue_model():
    tenant = Tenant.objects.create(tenant_name="test tenant")
    client = Client.objects.create(email="test@test.com")
    community = Community.objects.create(
        community_name="test community",
        tenant_id=tenant,
        description="test description",
    )
    issue = Issue.objects.create(
        client_id=client,
        issue="test issue",
        community_id=community,
        description="test description",
    )
    assert str(issue) == str(issue.issue_id)


@pytest.mark.django_db
def test_thread_model():
    tenant = Tenant.objects.create(tenant_name="test tenant")
    client = Client.objects.create(email="test@test.com")
    community = Community.objects.create(
        community_name="test community",
        tenant_id=tenant,
        description="test description",
    )
    issue = Issue.objects.create(
        client_id=client,
        issue="test issue",
        community_id=community,
        description="test description",
    )
    thread = Thread.objects.create(issue=issue)
    assert str(thread) == str(thread.thread_id)


@pytest.mark.django_db
def test_comment_model(client):
    tenant = Tenant.objects.create(tenant_name="test tenant")
    community = Community.objects.create(
        community_name="test community",
        tenant_id=tenant,
        description="test description",
    )
    issue = Issue.objects.create(
        client_id=client,
        issue="test issue",
        community_id=community,
        description="test description",
    )
    thread = Thread.objects.create(issue=issue)
    comment = Comment.objects.create(
        thread=thread,
        client=client
    )
    comment.likes.add(client)
    comment.dislikes.add(client)
    assert comment.likes.filter(id=client.id).exists()
    assert comment.dislikes.filter(id=client.id).exists()

