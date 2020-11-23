# Generated by Django 2.2.16 on 2020-11-23 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="layer",
            options={
                "ordering": ("is_basemap", "order"),
                "verbose_name": "Layer",
                "verbose_name_plural": "Layers",
            },
        ),
        migrations.AlterField(
            model_name="layer",
            name="identifier",
            field=models.CharField(max_length=200, verbose_name="Identifier"),
        ),
        migrations.AlterField(
            model_name="layer",
            name="is_basemap",
            field=models.BooleanField(default=False, verbose_name="Is basemap"),
        ),
        migrations.AlterField(
            model_name="layer",
            name="order",
            field=models.IntegerField(default=1, verbose_name="Order"),
        ),
    ]
