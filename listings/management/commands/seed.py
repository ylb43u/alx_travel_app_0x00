from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample users, listings, bookings, and reviews."

    def handle(self, *args, **kwargs):
        # Clear old data (optional but helpful for development)
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.all().delete()

        # Create Users
        users = []
        for i in range(3):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123'
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS("✅ Created sample users."))

        # Create Listings
        listings = []
        for i in range(5):
            listing = Listing.objects.create(
                title=f"Sample Listing {i}",
                description="A nice place to stay.",
                location=random.choice(['New York', 'Paris', 'Tokyo', 'Berlin']),
                price_per_night=random.randint(50, 200),
                host=random.choice(users)
            )
            listings.append(listing)

        self.stdout.write(self.style.SUCCESS("🏡 Created sample listings."))

        # Create Bookings
        bookings = []
        for i in range(5):
            listing = random.choice(listings)
            guest = random.choice([u for u in users if u != listing.host])
            check_in = timezone.now().date() + timedelta(days=random.randint(1, 10))
            check_out = check_in + timedelta(days=random.randint(2, 5))
            total_price = (check_out - check_in).days * listing.price_per_night

            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price
            )
            bookings.append(booking)

        self.stdout.write(self.style.SUCCESS("📅 Created sample bookings."))

        # Create Reviews
        for booking in bookings:
            Review.objects.create(
                listing=booking.listing,
                guest=booking.guest,
                rating=random.randint(3, 5),
                comment="Great stay!",
            )

        self.stdout.write(self.style.SUCCESS("🌟 Created sample reviews."))
        self.stdout.write(self.style.SUCCESS("✅ Seeding completed successfully!"))
