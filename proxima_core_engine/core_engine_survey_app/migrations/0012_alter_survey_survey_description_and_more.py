# Generated by Django 4.2.1 on 2023-06-07 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_engine_tenant_users_app", "0002_alter_admin_tenant_id"),
        ("core_engine_survey_app", "0011_survey_end_day_survey_start_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="survey_description",
            field=models.CharField(help_text="The survey description", max_length=200),
        ),
        migrations.AlterField(
            model_name="survey",
            name="target_audience",
            field=models.ManyToManyField(
                blank=True,
                help_text="The target audience/who to share with",
                to="core_engine_tenant_users_app.client",
            ),
        ),
    ]