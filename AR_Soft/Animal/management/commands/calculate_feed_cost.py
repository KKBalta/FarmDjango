from django.core.management.base import BaseCommand
from Animal.models import Animal
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Calculate feed cost for a specific animal or all animals."

    def add_arguments(self, parser):
        parser.add_argument('--eartag', type=str, help="Eartag of the animal to calculate feed cost for.")

    def handle(self, *args, **kwargs):
        eartag = kwargs.get('eartag')
        if eartag:
            try:
                animal = Animal.objects.get(eartag=eartag)
                self.calculate_and_print_feed_cost(animal)
            except Animal.DoesNotExist:
                self.stderr.write(f"Animal with eartag '{eartag}' does not exist.")
        else:
            animals = Animal.objects.all()
            for animal in animals:
                self.calculate_and_print_feed_cost(animal)

    def calculate_and_print_feed_cost(self, animal):
        start_date = animal.created_at
        end_date = now()
        feed_cost = animal.calculate_feed_cost(start_date, end_date)
        self.stdout.write(
            f"Feed cost for animal '{animal.eartag}' from {start_date} to {end_date}: {feed_cost}"
        )
