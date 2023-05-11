# Generated by Django 4.1.7 on 2023-04-06 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_tenant_management_app', '0002_alter_tenant_tenant_id'),
        ('core_engine_tenant_users_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='tenant_id',
            field=models.ForeignKey(help_text='Display id of the tenant', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_management_app.tenant'),
        ),
    ]
