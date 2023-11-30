# Generated by Django 4.2.1 on 2023-06-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_engine_community_app", "0011_comment_comment_description"),
        ("core_engine_tenant_users_app", "0002_alter_admin_tenant_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="favorites",
            field=models.ManyToManyField(to="core_engine_community_app.community"),
        ),
    ]