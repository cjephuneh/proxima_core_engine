# Generated by Django 4.1.7 on 2023-04-05 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_engine_tenant_users_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_photo', models.ImageField(upload_to='')),
                ('country', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('employee', models.OneToOneField(help_text='Display name of the employee', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_users_app.employee')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_photo', models.ImageField(upload_to='')),
                ('country', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('client', models.OneToOneField(help_text='Display name of the client', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_users_app.client')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_photo', models.ImageField(upload_to='')),
                ('country', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('admin', models.OneToOneField(help_text='Display name of the admin', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_users_app.admin')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
    ]
