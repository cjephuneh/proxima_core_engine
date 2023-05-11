Usage
=====


# Tenant


### Params
* `context` 

### Notes
* Create a tenant

### Example
#### Request
```
/api/tenantmanagement/tenant
```

#### Response
```
{
    "tenant_id": 1,
    "tenant_name": "Proxima",
    "industry": "Software"
}
```

### Params
* `context` 

### Notes
* Create tenant products
* Retrieve tenant products

### Example
#### Request
```
/api/tenantmanagement/product
```

#### Response
```
{
    "product_id": 1,
    "tenant_id": null,
    "name": "Virtual agents",
    "description": "Virtual customer service agents",
    "price": "500"
}
```

### Params
* `context` 

### Notes
* Retrieve tenant address

### Example
#### Request
```
/api/analtenantmanagementytics/address
```

#### Response
```
{
    "address_id": 1,
    "city": "Nairobi",
    "country": "Kenya",
    "community_id": null,
    "postal_code": "100 Nairobi",
    "state": "Nairobi",
    "payment_number": "0793681840"
}
```

### Params
* `context` 

### Notes
* Retrieve tenant metadata

### Example
#### Request
```
/api/tenantmanagement/metadata
```

#### Response
```

```



