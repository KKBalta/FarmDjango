# Generated by Django 5.1.3 on 2024-11-13 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farmer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
