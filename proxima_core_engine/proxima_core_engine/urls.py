import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import include, path
from django.urls import re_path as url
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

openapi_info = openapi.Info(
    title="Proxima Core Engine API",
    default_version="v1.5",
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
    url=settings.SWAGGER_ROOT_URL,
    permission_classes=(permissions.AllowAny,),
)


app_name = "proxima_core_engine"

urlpatterns = [
    url(
        r"^healthz/$",
        TemplateView.as_view(template_name="healthz.html"),
        name="healthz",
    ),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path('admin/', admin.site.urls),
    path("", include(("core_engine_auth_app.urls", "core_engine_auth_app"), namespace="auth_urls")),
    path("", include(("core_engine_chat_app.urls", "core_engine_chat_app"), namespace="chat_urls")),
    path("", include(("core_engine_community_app.urls", "core_engine_community_app"), namespace="community_urls")),
    path("", include(("core_engine_survey_app.urls", "core_engine_survey_app"), namespace="survey_urls")), 
    path("", include(("core_engine_users_profile_app.urls", "core_engine_users_profile_app"), namespace="profiles_urls")), 
    path("", include("core_engine_descriptive_analytics_app.urls", namespace="analytics_urls")),
    # path("", include("core_engine_payments_app.urls", namespace="payments_urls")),
    path("", include("core_engine_reports_app.urls", namespace="reports_urls")),
    # path("api/", include("core_engine_subscriptions_app.urls", namespace="subscriptions_urls")),
    path("", include(("core_engine_tenant_management_app.urls", "core_engine_tenant_management_app"), namespace="tenant_urls")),
    path('auth/', include('dj_rest_auth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
