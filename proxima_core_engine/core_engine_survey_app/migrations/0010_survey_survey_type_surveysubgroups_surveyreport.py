# Generated by Django 4.1.7 on 2023-05-01 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_tenant_users_app', '0002_alter_admin_tenant_id'),
        ('core_engine_survey_app', '0009_alter_response_survey_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='survey_type',
            field=models.CharField(blank=True, choices=[('open_ended', 'open_ended'), ('close_ended', 'close_ended')], help_text='The survey type', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='SurveySubGroups',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('date_time_created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('survey_subgroups_id', models.AutoField(help_text='The survey report id', primary_key=True, serialize=False)),
                ('subgroup_name', models.CharField(help_text='The survey subgroup name', max_length=255)),
                ('subgroup_description', models.CharField(help_text='The survey subgroup description', max_length=255)),
                ('subgroup_clients', models.ManyToManyField(blank=True, help_text='The subgroup clients', to='core_engine_tenant_users_app.client')),
                ('survey_id', models.ForeignKey(help_text='Display name of the survey', on_delete=django.db.models.deletion.CASCADE, to='core_engine_survey_app.survey')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyReport',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('date_time_created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('survey_report_id', models.AutoField(help_text='The survey report id', primary_key=True, serialize=False)),
                ('conclusion', models.TextField(help_text='The survey subgroup name')),
                ('survey_success', models.BooleanField(default=False, help_text='The survey success')),
                ('survey_id', models.ForeignKey(help_text='Display name of the survey', on_delete=django.db.models.deletion.CASCADE, to='core_engine_survey_app.survey')),
                ('survey_reporter', models.ForeignKey(help_text='Employee who made the survey review', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_users_app.employee')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
    ]
