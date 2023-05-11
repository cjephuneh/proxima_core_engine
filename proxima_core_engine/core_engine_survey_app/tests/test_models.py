import pytest
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_users_app.models import Client
from core_engine_utils_app.models import MetaDataBase
from core_engine_survey_app.models import Survey, Response


@pytest.fixture
def tenant(db):
    tenant = Tenant.objects.create(tenant_name="Test Tenant")
    yield tenant
    tenant.delete()


@pytest.fixture
def client(db, tenant):
    client = Client.objects.create(email="testclient@example.com")
    yield client
    client.delete()


@pytest.fixture
def survey_data():
    return {
        "survey_topic": "Test Topic",
        "survey_description": "Test Description",
        "survey_context": "Test Context",
        "survey_questions": {"Question 1": "Answer 1", "Question 2": "Answer 2"},
    }


@pytest.fixture
def response_data():
    return {"survey_response": {"Question 1": "Answer 1", "Question 2": "Answer 2"}}

@pytest.mark.django_db
def test_survey_creation(tenant, survey_data):
    survey = Survey.objects.create(tenant_id=tenant, **survey_data)
    assert isinstance(survey, MetaDataBase)
    assert str(survey) == str(survey.survey_id)
    assert survey.survey_topic == survey_data["survey_topic"]
    assert survey.survey_description == survey_data["survey_description"]
    assert survey.survey_context == survey_data["survey_context"]
    assert survey.survey_questions == survey_data["survey_questions"]
    assert survey.target_audience.count() == 0

@pytest.mark.django_db
def test_response_creation(tenant, client, survey_data, response_data):
    survey = Survey.objects.create(tenant_id=tenant, **survey_data)
    response = Response.objects.create(survey_id=survey, client=client, **response_data)
    assert isinstance(response, MetaDataBase)
    assert str(response) == str(response.response_id)
    assert response.survey_id == survey
    assert response.client == client
    assert response.survey_response == response_data["survey_response"]

@pytest.mark.django_db
def test_survey_str_method(tenant, survey_data):
    survey = Survey.objects.create(tenant_id=tenant, **survey_data)
    assert str(survey) == str(survey.survey_id)

@pytest.mark.django_db
def test_response_str_method(tenant, client, survey_data, response_data):
    survey = Survey.objects.create(tenant_id=tenant, **survey_data)
    response = Response.objects.create(survey_id=survey, client=client, **response_data)
    assert str(response) == str(response.response_id)

@pytest.mark.django_db
def test_survey_creation_without_tenant_raises_integrity_error(survey_data):
    with pytest.raises(IntegrityError):
        Survey.objects.create(**survey_data)

# @pytest.mark.django_db
# def test_survey_creation_with_invalid_topic_length_raises_validation_error(tenant):
#     with pytest.raises(ValidationError):
#         Survey.objects.create(tenant_id=tenant, survey_topic="x" * 256)


# @pytest.mark.django_db
# def test_survey_creation_with_invalid_description_length_raises_validation_error(tenant):
#     with pytest.raises(ValidationError):
#         Survey.objects.create(tenant_id=tenant, survey_description="x" * 21)

# @pytest.mark.django_db
# def test_survey_creation_with_invalid_context_length_raises_validation_error(tenant):
#     with pytest.raises(ValidationError):
#         Survey.objects.create(tenant_id=tenant, survey_context="x" * 21)

# @pytest.mark.django_db
# def test_response_creation_without_survey_id_raises_integrity_error(client, response_data):
#     with pytest.raises(IntegrityError):
#         Response.objects.create(client=client, **response_data)


# def test_response_creation_without_client_raises_integrity_error(survey_data, response_data):
#     survey = Survey.objects.create(**survey_data)
#     with pytest.raises
