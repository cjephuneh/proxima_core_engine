from django.contrib import admin

from core_engine_survey_app.models import (
    Survey, Response, SurveyReport, SurveySubGroups

)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_id', 'tenant_id', 'survey_topic', 'survey_description')
    # raw_id_fields = ('survey_id', 'tenant_id')
    # autocomplete_fields = ('skills',)

    search_fields = ('survey_id',)
    


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('response_id', 'survey_id', 'client', 'survey_response')
    # raw_id_fields = ('response_id', 'survey_id')

    search_fields = ('response_id',)

@admin.register(SurveyReport)
class SurveyReportAdmin(admin.ModelAdmin):
    list_display = ('survey_report_id', 'survey_id', 'conclusion', 'survey_success', 'survey_reporter')
    # raw_id_fields = ('survey_id', 'tenant_id')
    # autocomplete_fields = ('skills',)

    search_fields = ('survey_report_id',)
    


@admin.register(SurveySubGroups)
class SurveySubGroupsAdmin(admin.ModelAdmin):
    list_display = ('survey_subgroups_id', 'survey_id', 'subgroup_name', 'subgroup_description')
    # raw_id_fields = ('response_id', 'survey_id')

    search_fields = ('survey_subgroups_id',)
