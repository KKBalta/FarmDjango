# Generated by Django 5.1.3 on 2024-12-01 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Slaughter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slaughter',
            name='kdv',
            field=models.BooleanField(default=False),
        ),
    ]
