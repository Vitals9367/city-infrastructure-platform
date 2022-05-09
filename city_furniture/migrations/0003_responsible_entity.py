# Generated by Django 2.2.26 on 2022-02-14 14:26

import uuid

import django.db.models.deletion
import enumfields.fields
from django.db import migrations, models

import traffic_control.enums


class Migration(migrations.Migration):

    dependencies = [
        ('city_furniture', '0002_initial_colors'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponsibleEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('organization_level', enumfields.fields.EnumIntegerField(default=3, enum=traffic_control.enums.OrganizationLevel, verbose_name='Organization level')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='city_furniture.ResponsibleEntity', verbose_name='Parent Responsible Entity')),
            ],
            options={
                'verbose_name': 'Responsible Entity',
                'verbose_name_plural': 'Responsible Entities',
                'db_table': 'responsible_entity',
            },
        ),
        migrations.AddField(
            model_name='furnituresignpostplan',
            name='responsible_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='city_furniture.ResponsibleEntity', verbose_name='Responsible entity'),
        ),
        migrations.AddField(
            model_name='furnituresignpostreal',
            name='responsible_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='city_furniture.ResponsibleEntity', verbose_name='Responsible entity'),
        ),
    ]
