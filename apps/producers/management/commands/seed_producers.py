from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import Producer


class Command(BaseCommand):
    help = "Cria (ou atualiza) 6 contas de produtores de demonstração."

    producers_data = [
        {
            "username": "quinta_do_sol",
            "email": "contato@quintadosol.pt",
            "password": "producer123",
            "first_name": "João",
            "last_name": "Silva",
            "producer_name": "Quinta do Sol",
            "description": "Agricultura familiar sustentável há mais de 30 anos. Produzimos frutas e legumes frescos com métodos tradicionais.",
            "location": "Sintra, Portugal",
            "rating": 4.8,
            "is_active": True,
        },
        {
            "username": "horta_da_vila",
            "email": "contato@hortadavila.pt",
            "password": "producer123",
            "first_name": "Maria",
            "last_name": "Santos",
            "producer_name": "Horta da Vila",
            "description": "Produtos frescos colhidos diariamente. Compromisso com a qualidade e o sabor autêntico.",
            "location": "Cascais, Portugal",
            "rating": 4.6,
            "is_active": True,
        },
        {
            "username": "fazenda_verde",
            "email": "contato@fazendaverde.pt",
            "password": "producer123",
            "first_name": "António",
            "last_name": "Ferreira",
            "producer_name": "Fazenda Verde",
            "description": "Certificação biológica desde 2010. Produtos 100% orgânicos e sustentáveis.",
            "location": "Óbidos, Portugal",
            "rating": 4.9,
            "is_active": True,
        },
        {
            "username": "pomar_do_oeste",
            "email": "contato@pomardoeste.pt",
            "password": "producer123",
            "first_name": "Ricardo",
            "last_name": "Almeida",
            "producer_name": "Pomar do Oeste",
            "description": "Especialistas em frutas de qualidade. Maçãs, peras e morangos cultivados com paixão.",
            "location": "Alcobaça, Portugal",
            "rating": 5.0,
            "is_active": True,
        },
        {
            "username": "quinta_bio_coimbra",
            "email": "contato@quintabio.pt",
            "password": "producer123",
            "first_name": "Teresa",
            "last_name": "Costa",
            "producer_name": "Quinta Bio Coimbra",
            "description": "Produtos biológicos certificados. Agricultura regenerativa e respeito pelo meio ambiente.",
            "location": "Coimbra, Portugal",
            "rating": 4.7,
            "is_active": True,
        },
        {
            "username": "hortas_do_ave",
            "email": "contato@hortasdoave.pt",
            "password": "producer123",
            "first_name": "Manuel",
            "last_name": "Rodrigues",
            "producer_name": "Hortas do Ave",
            "description": "Legumes e verduras frescas. Tradição familiar e qualidade garantida.",
            "location": "Vila Nova de Famalicão, Portugal",
            "rating": 4.5,
            "is_active": True,
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        created_users = 0
        created_producers = 0

        for data in self.producers_data:
            user, user_created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_active": bool(data.get("is_active", True)),
                },
            )

            if user_created:
                created_users += 1

            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.is_active = bool(data.get("is_active", True))
            user.user_type = "producer"

            if user_created or not user.has_usable_password():
                user.set_password(data["password"])

            user.save()

            producer, producer_created = Producer.objects.get_or_create(
                user=user,
                defaults={
                    "name": data["producer_name"],
                    "description": data["description"],
                    "location": data["location"],
                    "rating": data["rating"],
                    "is_active": bool(data.get("is_active", True)),
                    "is_verified": True,
                },
            )

            if producer_created:
                created_producers += 1

            producer.name = data["producer_name"]
            producer.description = data["description"]
            producer.location = data["location"]
            producer.rating = data["rating"]
            producer.is_active = bool(data.get("is_active", True))
            producer.is_verified = True
            producer.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Produtor pronto: {producer.name} (user={user.username})"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"🎉 Concluído. Users criados: {created_users}. Produtores criados: {created_producers}."))
