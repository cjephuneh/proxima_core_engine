from django.shortcuts import render

# Create your views here.
from django.urls import include, path, re_path

from core_engine_survey_app.views import (
    SurveyView, ResponseView, SurveyReportView, SurveySubGroupsView
)

app_name="core_engine_survey_app"

urlpatterns = [
    re_path(r'^api/survey/', include([
        # Signin
        re_path(r'^survey/$', SurveyView.as_view(), name='core_survey_crud'),
        re_path(r'^response/$', ResponseView.as_view(), name='core_survey_response'),
        re_path(r'^surveyreportview/$', SurveyReportView.as_view(), name='core_survey_surveyreportview'),
        re_path(r'^surveysubgroup/$', SurveySubGroupsView.as_view(), name='core_survey_surveysubgroup'),

    ]))
]