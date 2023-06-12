from django.urls import include, path, re_path

from core_engine_social_intergtaions.views import (
    WhatsAppIntergration, FaceBookIntergration, InstagramIntergration
)

app_name="core_engine_social_intergtaions"


urlpatterns = [
    re_path(r'^api/socialintergrations/', include([
        # Signin
        re_path(r'^whatsappintergration/$', WhatsAppIntergration.as_view(), name='core__engine_whatsapp_intergration'),
        re_path(r'^facebookintergration/$', FaceBookIntergration.as_view(), name='core__engine_facebook_intergration'),
        re_path(r'^instagramintergration/$', InstagramIntergration.as_view(), name='core__engine_intergration_intergration'),

    ]))
]