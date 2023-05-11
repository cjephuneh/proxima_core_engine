# Generated by Django 4.1.7 on 2023-04-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_id', models.AutoField(help_text='The lilling details id ID UUID', primary_key=True, serialize=False)),
                ('survey_response', models.JSONField(help_text='The survey response')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('survey_id', models.AutoField(help_text='The lilling details id ID UUID', primary_key=True, serialize=False)),
                ('survey_topic', models.CharField(help_text='The survey topic', max_length=20)),
                ('survey_description', models.CharField(help_text='The survey description', max_length=20)),
                ('survey_context', models.CharField(help_text='The survey context', max_length=20)),
                ('survey_questions', models.JSONField(help_text='The survey questions')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
    ]
