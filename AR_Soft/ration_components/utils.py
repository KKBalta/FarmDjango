from ration_components.models import RationTable

def create_default_ration_table():
    # Check if the default ration table exists
    if not RationTable.objects.filter(name="Base Ration").exists():
        RationTable.objects.create(
            name="Base Ration",
            description="This is the default base ration table for all new animals. Clients can customize it."
        )
        print("Default ration table created.")
    else:
        print("Default ration table already exists.")
