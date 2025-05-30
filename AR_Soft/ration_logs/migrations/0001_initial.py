# Generated by Django 5.1.3 on 2024-12-28 12:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ration_components', '0009_delete_rationcomponentchange'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=50)),
                ('old_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('new_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_logs', to='ration_components.rationcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='RationTableComponentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50)),
                ('old_quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('new_quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('table_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='ration_components.rationtablecomponent')),
            ],
        ),
        migrations.CreateModel(
            name='RationTableLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ration_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='ration_components.rationtable')),
            ],
        ),
    ]
