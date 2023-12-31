# Generated by Django 4.1.7 on 2023-04-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_tenant_users_app', '0002_alter_admin_tenant_id'),
        ('core_engine_survey_app', '0005_alter_response_survey_id_alter_survey_survey_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='target_audience',
            field=models.ManyToManyField(blank=True, help_text='The target audience', null=True, to='core_engine_tenant_users_app.client'),
        ),
    ]
