# Generated by Django 5.1.3 on 2024-12-18 06:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weight', '0002_alter_weight_recorded_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
