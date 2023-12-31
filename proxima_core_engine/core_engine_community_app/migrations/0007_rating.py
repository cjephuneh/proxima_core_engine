# Generated by Django 4.1.7 on 2023-04-17 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_tenant_users_app', '0002_alter_admin_tenant_id'),
        ('core_engine_community_app', '0006_rename_datefield_comment_date_time_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('date_time_created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating_id', models.AutoField(help_text='The tenant community rating ID.', primary_key=True, serialize=False)),
                ('community_id', models.CharField(blank=True, help_text='Display name of the community', max_length=255, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('client_id', models.ForeignKey(help_text='Display name of the client', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_users_app.client')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
    ]
