import pytest
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_users_app.models import Client
from core_engine_chat_app.models import (Chat, Message)

@pytest.fixture
def tenant():
    return Tenant.objects.create(tenant_name="Test Tenant")

@pytest.fixture
def client():
    return Client.objects.create(first_name="Test Client")

@pytest.fixture
def chat(tenant, client):
    return Chat.objects.create(tenant=tenant, chat_owner=client)

@pytest.mark.django_db
def test_create_chat(chat):
    assert chat.chat_id is not None
    assert chat.tenant is not None
    assert chat.chat_owner is not None

@pytest.mark.django_db
def test_create_chat_without_tenant(client):
    with pytest.raises(IntegrityError):
        Chat.objects.create(chat_owner=client)

@pytest.mark.django_db
def test_create_chat_without_client(tenant):
    with pytest.raises(IntegrityError):
        Chat.objects.create(tenant=tenant)

@pytest.mark.django_db
def test_chat_string_representation(chat):
    assert str(chat) == str(chat.chat_id)


@pytest.fixture
def message(chat):
    return Message.objects.create(chat_id=chat, text_content="Test message")

@pytest.mark.django_db
def test_create_message(message):
    assert message.message_id is not None
    assert message.chat_id is not None
    assert message.text_content == "Test message"
    assert message.sent_at is not None
    assert message.message_sender is not None
    assert message.channel is None
    assert message.topic is None

@pytest.mark.django_db
def test_create_message_with_voice_content(message):
    file = SimpleUploadedFile("test_voice_content.wav", b"file_content", content_type="audio/wav")
    message.voice_content = file
    message.save()
    assert message.voice_content is not None

@pytest.mark.django_db
def test_create_message_without_chat():
    with pytest.raises(IntegrityError):
        Message.objects.create(text_content="Test message")

@pytest.mark.django_db
def test_message_string_representation(message):
    assert str(message) == str(message.message_id)