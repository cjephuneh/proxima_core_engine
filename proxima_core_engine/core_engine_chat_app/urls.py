from django.shortcuts import render

# Create your views here.
from django.urls import include, path, re_path

from core_engine_chat_app.views import (
    ChatView, ClientChatsView, 
    MessageView, TenantChatsView,
    VoiceNoteAPIView
)

app_name="core_engine_chat_app"

urlpatterns = [
    re_path(r'^api/chat/', include([
        # Signin
        re_path(r'^chat/$', ChatView.as_view(), name='core_chat_chat'),
        re_path(r'^voice/$', VoiceNoteAPIView.as_view(), name='core_chat_voice'),
        re_path(r'^clientschat/$', ClientChatsView.as_view(), name='core_chat_clientchats'),
        re_path(r'^message/$', MessageView.as_view(), name='core_chat_message'),
        re_path(r'^tenantchats/$', TenantChatsView.as_view(), name='core_chat_tenantchats'),

    ]))
]
