# Generated by Django 4.1.7 on 2023-04-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_community_app', '0010_remove_comment_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_description',
            field=models.TextField(blank=True, help_text='Description of the comment', null=True),
        ),
    ]
