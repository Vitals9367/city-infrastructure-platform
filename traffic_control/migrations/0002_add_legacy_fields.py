# Generated by Django 2.2.10 on 2020-02-25 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_control", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trafficsigncode",
            name="legacy_code",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Legacy code"
            ),
        ),
        migrations.AddField(
            model_name="trafficsigncode",
            name="legacy_description",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Legacy description"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="mount_type_fi",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Mount (fi)"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="source_id",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Source id"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignplan",
            name="source_name",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Source name"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignreal",
            name="legacy_code",
            field=models.CharField(
                blank=True,
                max_length=32,
                null=True,
                verbose_name="Legacy Traffic Sign Code",
            ),
        ),
        migrations.AddField(
            model_name="trafficsignreal",
            name="mount_type_fi",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Mount (fi)"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignreal",
            name="scanned_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Scanned at"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignreal",
            name="source_id",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Source id"
            ),
        ),
        migrations.AddField(
            model_name="trafficsignreal",
            name="source_name",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Source name"
            ),
        ),
        migrations.AlterField(
            model_name="trafficsignplan",
            name="mount_type",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Mount"
            ),
        ),
        migrations.AlterField(
            model_name="trafficsignreal",
            name="code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="traffic_control.TrafficSignCode",
                verbose_name="Traffic Sign Code",
            ),
        ),
        migrations.AlterField(
            model_name="trafficsignreal",
            name="height",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                max_digits=20,
                null=True,
                verbose_name="Height",
            ),
        ),
        migrations.AlterField(
            model_name="trafficsignreal",
            name="mount_type",
            field=models.CharField(
                blank=True, max_length=254, null=True, verbose_name="Mount"
            ),
        ),
    ]
