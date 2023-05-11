from django.urls import include, path, re_path

from .views import(
    AdminProfileRetrieveAPIView, AdminRetrieveUpdateAPIView, ClientProfileRetrieveAPIView,
    ClientRetrieveUpdateAPIView, EmployeeProfileRetrieveAPIView, EmployeeRetrieveUpdateAPIView,
)

app_name = 'core_engine_users_profile_app'


urlpatterns = [
    re_path(r'^api/userprofiles/', include([
        # Signin
        re_path(r'^adminprofiles/<int:admin_id>/$', AdminProfileRetrieveAPIView.as_view(), name='core_profile_adminprofiles'),
        re_path(r'^clientprofiles/<int:client_id>/$', ClientProfileRetrieveAPIView.as_view(), name='core_profile_clientprofiles'),
        re_path(r'^employeeprofiles/<int:employee_id>/$', EmployeeProfileRetrieveAPIView.as_view(), name='core_profile_employeeprofiles'),
        re_path(r'^admin/$', AdminRetrieveUpdateAPIView.as_view(), name='core_profile_admin'),
        re_path(r'^employee/$', EmployeeRetrieveUpdateAPIView.as_view(), name='core_profile_employee'),
        re_path(r'^client/$', ClientRetrieveUpdateAPIView.as_view(), name='core_profile_client'),

    ]))
]