# Generated by Django 4.1.7 on 2023-04-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_chat_app', '0005_rename_datefield_chat_date_time_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='escalated',
            field=models.BooleanField(blank=True, default=False, help_text='Say whether a client escalated a chat to a human agent.', null=True),
        ),
    ]
