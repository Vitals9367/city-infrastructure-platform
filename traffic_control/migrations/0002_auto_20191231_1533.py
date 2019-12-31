# Generated by Django 3.0.1 on 2019-12-31 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("traffic_control", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trafficsignplan",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_by_trafficsignplan_set",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="lifecycle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="traffic_control.Lifecycle",
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="traffic_control.TrafficSignPlan",
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="updated_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="updated_by_trafficsignplan_set",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
