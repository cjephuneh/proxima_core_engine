# Generated by Django 4.1.7 on 2023-04-16 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_engine_community_app', '0004_alter_community_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='DateField',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='DateField',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='DateField',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='DateField',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
