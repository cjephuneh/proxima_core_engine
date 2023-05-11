import pytest
from django.db import IntegrityError
from core_engine_tenant_management_app.models import Tenant, Product, Metadata, Address


@pytest.fixture
def sample_tenant():
    return Tenant.objects.create(tenant_name="Sample Company", industry="IT")


@pytest.fixture
def sample_product(sample_tenant):
    return Product.objects.create(tenant_id=sample_tenant, name="Sample Product", description="Sample Description",
                                   price="10.00")


@pytest.fixture
def sample_metadata(sample_tenant):
    return Metadata.objects.create(tenant_id={"tenant_name": "Sample Company", "industry": "IT"})


@pytest.fixture
def sample_address(sample_tenant):
    return Address.objects.create(tenant_id=sample_tenant, billing_details_id="123", city="Sample City",
                                   country="Sample Country", postal_code="12345", state="Sample State",
                                   payment_number="1234567890")

@pytest.mark.django_db
def test_tenant_model(sample_tenant):
    assert sample_tenant.tenant_id is not None
    assert sample_tenant.tenant_name == "Sample Company"
    assert sample_tenant.industry == "IT"


@pytest.mark.django_db
def test_product_model(sample_product):
    assert sample_product.product_id is not None
    assert sample_product.tenant_id is not None
    assert sample_product.name == "Sample Product"
    assert sample_product.description == "Sample Description"
    assert sample_product.price == "10.00"

@pytest.mark.django_db
def test_metadata_model(sample_metadata):
    assert sample_metadata.metadata_id is not None
    assert sample_metadata.tenant_id == {"tenant_name": "Sample Company", "industry": "IT"}

@pytest.mark.django_db
def test_address_model(sample_address):
    assert sample_address.address_id is not None
    assert sample_address.tenant_id is not None
    assert sample_address.billing_details_id == "123"
    assert sample_address.city == "Sample City"
    assert sample_address.country == "Sample Country"
    assert sample_address.postal_code == "12345"
    assert sample_address.state == "Sample State"
    assert sample_address.payment_number == "1234567890"

@pytest.mark.django_db
def test_product_tenant_fk_constraint(sample_tenant):
    with pytest.raises(IntegrityError):
        Product.objects.create(tenant_id=None, name="Sample Product", description="Sample Description",
                                price="10.00")

@pytest.mark.django_db
def test_address_tenant_fk_constraint(sample_tenant):
    with pytest.raises(IntegrityError):
        Address.objects.create(tenant_id=None, billing_details_id="123", city="Sample City",
                                country="Sample Country", postal_code="12345", state="Sample State",
                                payment_number="1234567890")


