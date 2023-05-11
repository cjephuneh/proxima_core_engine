import logging

from django.db import DatabaseError, IntegrityError

from core_engine_tenant_management_app.models import Product
from core_engine_tenant_management_app.models import Tenant

log = logging.getLogger(__name__)


### Retrieval methods
def get_tenant_products_from_id(product_id):
    product = None
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        log.warning("Tenant does not exist: %s", product_id)
    except Product.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Tenants found for Tenant ID: %s", product_id)
    except Exception:
        log.exception("Tenant lookup error for Tenant ID: %s", product_id)
    
    return product



### Save methods
def save_tenant_product(**kwargs):
    """
    Create or update course entry with product_id and tenant_name
    
    Return:
    product (None if fail)
    created
    """
    # if not product_id:
    #     return None, False
    
    try:
        tenant_id = kwargs.get('tenant_id')
        name = kwargs.get('name')
        description = kwargs.get('description')
        price = kwargs.get('price')

        product, created = Product.objects.get_or_create(
            # product_id=product_id,
            tenant_id=Tenant.objects.get(tenant_id=tenant_id),
            name=name,
            description=description,
            price=price
        )

        
        product.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Tenant Products save error: (tenant_id: %s, name: %s)",
            tenant_id, name
        )
        return None, False
    
    return product, created