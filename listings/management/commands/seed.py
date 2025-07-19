from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Optional: clear existing data
        Listing.objects.all().delete()

        sample_titles = [
            "Cozy Cottage in the Mountains",
            "Modern Studio in Downtown",
            "Beachside Bungalow",
            "Luxury Villa with Pool",
            "Rustic Cabin Escape",
            "Charming Apartment in Paris",
            "Minimalist Loft in Berlin"
        ]

        locations = ["New York", "Paris", "Tokyo", "Berlin", "Casablanca", "Lisbon", "London"]

        for i in range(10):
            listing = Listing.objects.create(
                title=random.choice(sample_titles),
                description="This is a sample listing with auto-generated content.",
                location=random.choice(locations),
                price_per_night=random.randint(50, 500),
                max_guests=random.randint(1, 6),
                availability=True
            )
            self.stdout.write(self.style.SUCCESS(f"Created listing: {listing.title}"))

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed."))
