from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.producers.models import Producer
from apps.users.models import Product  # Product está em users
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Create demo users, producer and products for academic evaluation (no real data)."

    def handle(self, *args, **options):
        User = get_user_model()

        # Create admin
        admin_username = "demoadmin"
        admin_email = "demoadmin@example.com"
        admin_password = "demoadminpass"
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {admin_username} / {admin_password}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {admin_username} already exists, skipping."))

        # Create a consumer user
        if not User.objects.filter(username="alice").exists():
            alice = User.objects.create_user(username="alice", email="alice@example.com", password="alicepass")
            alice.first_name = "Alice"
            alice.user_type = "consumer"
            alice.is_active = True
            alice.save()
            self.stdout.write(self.style.SUCCESS("Created consumer user: alice / alicepass"))
        else:
            self.stdout.write(self.style.WARNING("User alice already exists, skipping."))

        # Create a producer user and producer profile
        if not User.objects.filter(username="bobfarm").exists():
            bob = User.objects.create_user(username="bobfarm", email="bob@example.com", password="bobpass")
            bob.first_name = "Bob"
            bob.user_type = "producer"
            bob.is_active = True
            bob.save()
            producer_obj, created = Producer.objects.get_or_create(user=bob, defaults={
                "name": "Bob's Farm",
                "description": "Produtos frescos e locais - demo",
                "location": "Demoville",
                "rating": 4.5,
                "active": True,
            })
            if created:
                self.stdout.write(self.style.SUCCESS("Created producer: Bob's Farm (user bobfarm / bobpass)"))
            else:
                self.stdout.write(self.style.WARNING("Producer for bobfarm already exists, skipping."))
        else:
            bob = User.objects.get(username="bobfarm")
            producer_obj = Producer.objects.filter(user=bob).first()

        # Create sample products
        demo_products = [
            {"name": "Maçã Gala", "price": 1.50, "category": "Frutas", "stock": 120},
            {"name": "Cenoura", "price": 0.80, "category": "Legumes", "stock": 200},
            {"name": "Alface", "price": 0.65, "category": "Verduras", "stock": 150},
            {"name": "Feijão", "price": 2.20, "category": "Grãos", "stock": 80},
        ]

        created_count = 0
        for p in demo_products:
            obj, created = Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "producer": producer_obj,
                    "description": f"Demo: {p['name']} do produtor {producer_obj.name}",
                    "price": p["price"],
                    "category": p["category"],
                    "unit": "kg",
                    "stock": p["stock"],
                    "available": True,
                    "is_organic": False,
                    "created_at": timezone.now(),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} demo products."))

        self.stdout.write(self.style.SUCCESS("Demo data creation complete. Use the credentials above to log in."))
