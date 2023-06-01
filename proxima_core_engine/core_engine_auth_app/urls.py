from django.urls import include, path, re_path

from core_engine_auth_app.views import (
    LoginAPIView, AdminAPIView, AnonymousUserView, ClientAPIView, EmployeeAPIView,
    ChangePasswordView, ForgotPasswordView, ActivateUserView, ResendActivationLinkView, ResetPasswordView
)
app_name="core_engine_auth_app"


urlpatterns = [

    re_path(r'^api/auth/', include([
        # Signin
        re_path(r'^signin/$', LoginAPIView.as_view(), name='core_auth_signin'),
        re_path(r'^admin/$', AdminAPIView.as_view(), name='core_auth_admin'),
        re_path(r'^anonymoususer/$', AnonymousUserView.as_view(), name='core_auth_anonymoususer'),
        re_path(r'^client/$', ClientAPIView.as_view(), name='core_auth_client'),
        re_path(r'^employee/$', EmployeeAPIView.as_view(), name='core_auth_employee'),
        re_path(r'^changepassword/$', ChangePasswordView.as_view(), name='core_auth_changepassword'),
        re_path(r'^forgotpassword/$', ForgotPasswordView.as_view(), name='core_auth_forgotpassword'),
        re_path(r'^activateuser/$', ActivateUserView.as_view(), name='core_auth_activate_user'),
        re_path(r'^resendactivationlink/$', ResendActivationLinkView.as_view(), name='core_auth_resend_activation_link'),
        re_path(r'^activate_user/<str:uid>/<str:token>/<str:activation_key>/$', ActivateUserView.as_view(), name="core_auth_activate_user"),
        re_path(r'reset_password/<str:uid>/<str:token>/$', ResetPasswordView.as_view(), name="core_auth_reset0-password"),
    ]))
    
]