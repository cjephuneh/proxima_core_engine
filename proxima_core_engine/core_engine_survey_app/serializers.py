import logging
from rest_framework import serializers

from core_engine_survey_app.models import (
    Response, Survey, SurveySubGroups, SurveyReport

)

from core_engine_tenant_users_app.models import (
    Client
)

# Response serializers

# survey target audience serializer
class TargetAudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB']

class SurveySerializer(serializers.ModelSerializer):
    # tenant_id = serializers.CharField(
    #     source='core_engine_tenant_management_app.tenant', default=None
    # )
    target_audience = TargetAudienceSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('survey_id', 'tenant_id', 'survey_topic', 'survey_description',
                  'survey_context', 'survey_questions', 'target_audience', 'survey_type', 'start_day', 'end_day')
        # read_only_fields = fields


# Survey serializers

class ResponseSerializer(serializers.ModelSerializer):

    # survey_id = serializers.CharField(
    #     source='core_engine_survey_app.survey', default=None
    # )
    # client = serializers.CharField(
    #     source='core_engine_tenant_users_app.client', default=None
    # )
    client = TargetAudienceSerializer(many=False)
    class Meta:
        model = Response
        fields = ('response_id', 'survey_id', 'client', 'survey_response')
        # read_only_fields = ('position',)


class SurveySubGroupsSerializer(serializers.ModelSerializer):
    survey_id = serializers.CharField(
        source='core_engine_survey_app.survey', default=None
    )

    class Meta:
        model = SurveySubGroups
        fields = ('survey_subgroups_id', 'survey_id', 'subgroup_name', 'subgroup_description')
        # read_only_fields = fields


# Survey serializers

class SurveyReportSerializer(serializers.ModelSerializer):

    # survey_id = serializers.CharField(
    #     source='core_engine_survey_app.survey', default=None
    # )
    # survey_reporter = serializers.CharField(
    #     source='core_engine_tenant_users_app.employee', default=None
    # )
    class Meta:
        model = SurveyReport
        fields = ('survey_report_id', 'survey_id', 'conclusion', 'survey_success', 'survey_reporter')