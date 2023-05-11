from django.urls import include, path, re_path

from core_engine_auth_app.views.signin import LoginAPIView
from core_engine_reports_app.views import (
   ChatsPdfFile, ChatsCsvFile, MessagesPdfFile, MessagesCsvFile,
    SurveyCsvFile, SurveyPdfFile, IssuesCsvFile, IssuesPdfFile,
    ThreadsPdfFile, ThreadsCsvFile, SurveyResponsesPdfFile, surveyResponsesCsvFile
    )

app_name="core_engine_reports_app"

urlpatterns = [
    re_path(r'^api/reports/', include([
        # Signin

        re_path(r'^chatspdf/$', ChatsPdfFile.as_view(), name='core_reports_chatspdf'),
        re_path(r'^chatscsv/$', ChatsCsvFile.as_view(), name='core_reports_chatscsv'), 
        re_path(r'^messagespdf/$', MessagesPdfFile.as_view(), name='core_reports_messagespdf'),
        re_path(r'^messagescsv/$', MessagesCsvFile.as_view(), name='core_reports_messagescsv'), 
        re_path(r'^surveycsv/$', SurveyCsvFile.as_view(), name='core_reports_surveycsv'),
        re_path(r'^surveypdf/$', SurveyPdfFile.as_view(), name='core_reports_surveypdf'), 
        re_path(r'^issuescsv/$', IssuesCsvFile.as_view(), name='core_reports_issuescsv'),
        re_path(r'^issuespdf/$', IssuesPdfFile.as_view(), name='core_reports_issuespdf'), 
        re_path(r'^threadpdf/$', ThreadsPdfFile.as_view(), name='core_reports_threadpdf'),
        re_path(r'^threadscsv/$', ThreadsCsvFile.as_view(), name='core_reports_threadscsv'),    
        re_path(r'^surveyresponsespdf/$', SurveyResponsesPdfFile.as_view(), name='core_reports_surveyresponsespdf'),
        re_path(r'^surveyresponsescsv/$', surveyResponsesCsvFile.as_view(), name='core_reports_surveyresponsescsv'), 
    ]))
]