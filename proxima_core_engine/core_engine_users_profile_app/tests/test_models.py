import pytest
from core_engine_tenant_users_app.models import  Admin, Client, Employee
from django.core.exceptions import ValidationError
from core_engine_users_profile_app.models import AdminProfile, ClientProfile, EmployeeProfile
from core_engine_tenant_management_app.models import Tenant

@pytest.mark.django_db
def test_admin_profile_creation():
    tenant = Tenant.objects.create(tenant_name="Test Tenant")
    admin = Admin.objects.create(
        username="test_admin",
        email="test_admin@example.com",
        first_name="Test",
        last_name="Admin",
        phonenumber="1234567890",
        gender="Male",
        DOB="2000-01-01",
        user_type="admin",
        tenant_id=tenant
    )
    AdminProfile.objects.create(
        admin=admin,
        profile_photo="test_admin.jpg",
        country="USA",
        county="Los Angeles",
        city="Los Angeles",
        postal_code="90001"
    )
    assert AdminProfile.objects.count() == 1

@pytest.mark.django_db
def test_client_profile_creation():
    client = Client.objects.create(
        username="test_client",
        email="test_client@example.com",
        first_name="Test",
        last_name="Client",
        phonenumber="1234567890",
        gender="Male",
        DOB="2000-01-01",
        user_type="client"
    )
    ClientProfile.objects.create(
        client=client,
        profile_photo="test_client.jpg",
        country="USA",
        county="Los Angeles",
        city="Los Angeles",
        postal_code="90001"
    )
    assert ClientProfile.objects.count() == 1

@pytest.mark.django_db
def test_employee_profile_creation():
    tenant = Tenant.objects.create(tenant_name="Test Tenant")
    employee = Employee.objects.create(
        username="test_employee",
        email="test_employee@example.com",
        first_name="Test",
        last_name="Employee",
        phonenumber="1234567890",
        gender="Male",
        DOB="2000-01-01",
        user_type="employee",
        tenant_id=tenant
    )
    EmployeeProfile.objects.create(
        employee=employee,
        profile_photo="test_employee.jpg",
        country="USA",
        county="Los Angeles",
        city="Los Angeles",
        postal_code="90001"
    )
    assert EmployeeProfile.objects.count() == 1



