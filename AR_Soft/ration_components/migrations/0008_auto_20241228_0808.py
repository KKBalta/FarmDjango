from django.db import migrations


def create_base_ration(apps, schema_editor):
    # Get the RationTable model
    RationTable = apps.get_model('ration_components', 'RationTable')

    # Check if the default ration table exists
    if not RationTable.objects.filter(name="Base Ration").exists():
        # Create the default ration table
        RationTable.objects.create(
            name="Base Ration",
            description="This is the default base ration table for all new animals."
        )


class Migration(migrations.Migration):
    dependencies = [
        ('ration_components', '0007_alter_rationcomponentchange_ration_table_component_id'),  # Keep the existing dependency
    ]

    operations = [
        migrations.RunPython(create_base_ration),  # Add the custom logic to create the Base Ration
    ]
