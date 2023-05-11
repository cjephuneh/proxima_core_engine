from django.contrib import admin

from core_engine_tenant_users_app.models import (
Admin, AnonymousUser, Client, Employee
)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    # raw_id_fields = ('tenant_id', )
    # autocomplete_fields = ('skills',)

    search_fields = ('first_name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    # raw_id_fields = ('tenant_id', )
    # autocomplete_fields = ('skills',)

    search_fields = ('first_name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tenant_id')
    raw_id_fields = ('tenant_id', )
    # autocomplete_fields = ('skills',)

    search_fields = ('tenant_id',)


@admin.register(AnonymousUser)
class AnonymousUserAdmin(admin.ModelAdmin):
    list_display = ('contact', )
    # raw_id_fields = ('tenant_id', )
    # autocomplete_fields = ('skills',)

    search_fields = ('contact',)


