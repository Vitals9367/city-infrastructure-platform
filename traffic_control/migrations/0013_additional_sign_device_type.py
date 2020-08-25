# Generated by Django 2.2.14 on 2020-07-06 10:06

import django.db.models.deletion
from django.db import migrations, models

import traffic_control.models.common


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_control", "0012_sign_relations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionalsigncontentplan",
            name="device_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(
                        ("target_model", None),
                        (
                            "target_model",
                            traffic_control.models.common.DeviceTypeTargetModel(
                                "additional_sign"
                            ),
                        ),
                        _connector="OR",
                    )
                ),
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="traffic_control.TrafficControlDeviceType",
                verbose_name="Device type",
            ),
        ),
        migrations.AlterField(
            model_name="additionalsigncontentreal",
            name="device_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(
                        ("target_model", None),
                        (
                            "target_model",
                            traffic_control.models.common.DeviceTypeTargetModel(
                                "additional_sign"
                            ),
                        ),
                        _connector="OR",
                    )
                ),
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="traffic_control.TrafficControlDeviceType",
                verbose_name="Device type",
            ),
        ),
    ]
