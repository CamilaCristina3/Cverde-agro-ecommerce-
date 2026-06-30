"""
Management command: seed_demo_data
Popula a base de dados COVERDE com dados de demonstração.

Uso:
    python manage.py seed_demo_data

Seguro: usa get_or_create / update_or_create, não apaga dados existentes.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from apps.users.models import Category, Producer, Product, CustomerProfile

User = get_user_model()

# ---------------------------------------------------------------------------
# Dados de configuração
# ---------------------------------------------------------------------------

PRODUCER_PASSWORD = "Produtor12345"
CLIENT_PASSWORD = "Cliente12345"

PRODUCERS_DATA = [
    {
        "email": "produtor1@coverde.pt",
        "first_name": "António",
        "last_name": "Ferreira",
        "company_name": "Quinta Verde do Mondego",
        "location": "Coimbra",
        "nif": "501234567",
        "description": "Quinta familiar com 30 anos de experiência em produção de frutas e legumes biológicos nas margens do Rio Mondego.",
    },
    {
        "email": "produtor2@coverde.pt",
        "first_name": "Maria",
        "last_name": "Santos",
        "company_name": "Horta Bio Coimbra",
        "location": "Coimbra",
        "nif": "502345678",
        "description": "Produção 100% biológica certificada de hortícolas e ervas aromáticas no coração de Coimbra.",
    },
    {
        "email": "produtor3@coverde.pt",
        "first_name": "João",
        "last_name": "Oliveira",
        "company_name": "Frutas da Serra",
        "location": "Lousã",
        "nif": "503456789",
        "description": "Produtores de frutas de montanha da Serra da Lousã: maçãs, peras e frutos silvestres de excelência.",
    },
    {
        "email": "produtor4@coverde.pt",
        "first_name": "Ana",
        "last_name": "Costa",
        "company_name": "Campos do Centro",
        "location": "Condeixa-a-Nova",
        "nif": "504567890",
        "description": "Exploração agrícola de grande produção de cereais, leguminosas e hortícolas da região de Condeixa.",
    },
    {
        "email": "produtor5@coverde.pt",
        "first_name": "Carlos",
        "last_name": "Rodrigues",
        "company_name": "Aromas da Terra",
        "location": "Mealhada",
        "nif": "505678901",
        "description": "Especialistas em ervas aromáticas, azeites e produtos tradicionais da Mealhada com certificação de produção integrada.",
    },
]

CLIENTS_DATA = [
    {"email": "cliente1@coverde.pt", "first_name": "Sofia", "last_name": "Mendes"},
    {"email": "cliente2@coverde.pt", "first_name": "Pedro", "last_name": "Carvalho"},
    {"email": "cliente3@coverde.pt", "first_name": "Beatriz", "last_name": "Lopes"},
    {"email": "cliente4@coverde.pt", "first_name": "Rui", "last_name": "Figueiredo"},
    {"email": "cliente5@coverde.pt", "first_name": "Inês", "last_name": "Teixeira"},
]

CATEGORIES_DATA = [
    {"name": "Frutas",            "slug": "frutas",            "icon": "fa-apple-alt",  "ordering": 1},
    {"name": "Legumes",           "slug": "legumes",           "icon": "fa-carrot",     "ordering": 2},
    {"name": "Verduras",          "slug": "verduras",          "icon": "fa-leaf",       "ordering": 3},
    {"name": "Hortícolas",        "slug": "horticolas",        "icon": "fa-seedling",   "ordering": 4},
    {"name": "Biológicos",        "slug": "biologicos",        "icon": "fa-spa",        "ordering": 5},
    {"name": "Cereais e Grãos",   "slug": "cereais-e-graos",   "icon": "fa-wheat-awn",  "ordering": 6},
    {"name": "Azeite",            "slug": "azeite",            "icon": "fa-oil-can",    "ordering": 7},
    {"name": "Ervas Aromáticas",  "slug": "ervas-aromaticas",  "icon": "fa-mortar-pestle", "ordering": 8},
]

# (nome, slug, categoria_slug, produtor_email, preço, stock, unit, is_featured, certification, image_file)
PRODUCTS_DATA = [
    # Frutas
    ("Maçã",          "maca",          "frutas",          "produtor3@coverde.pt", "1.50", 200, "kg",   True,  "tradicional", "Maçã.png"),
    ("Pêra",          "pera",          "frutas",          "produtor3@coverde.pt", "1.80", 180, "kg",   True,  "tradicional", "Pêra.webp"),
    ("Laranja",       "laranja",       "frutas",          "produtor1@coverde.pt", "1.20", 300, "kg",   True,  "",            "Laranja.webp"),
    ("Limão",         "limao",         "frutas",          "produtor1@coverde.pt", "1.00", 250, "kg",   False, "",            "Limão.webp"),
    ("Manga",         "manga",         "frutas",          "produtor1@coverde.pt", "3.50", 100, "un",   True,  "",            "Manga.webp"),
    ("Banana",        "banana",        "frutas",          "produtor1@coverde.pt", "1.40", 150, "kg",   False, "",            None),
    ("Morango Bio",   "morango-bio",   "biologicos",      "produtor2@coverde.pt", "4.50", 80,  "pct",  True,  "biologico",   "Morango Bio.webp"),
    ("Abacate",       "abacate",       "frutas",          "produtor1@coverde.pt", "2.80", 120, "un",   True,  "",            "Abacate.webp"),
    # Legumes
    ("Tomate",        "tomate",        "legumes",         "produtor2@coverde.pt", "2.00", 200, "kg",   True,  "biologico",   None),
    ("Cenoura",       "cenoura",       "legumes",         "produtor4@coverde.pt", "0.90", 350, "kg",   False, "",            "Cenouras Bio.png"),
    ("Batata",        "batata",        "legumes",         "produtor4@coverde.pt", "0.80", 500, "kg",   False, "",            None),
    ("Cebola",        "cebola",        "legumes",         "produtor4@coverde.pt", "0.70", 400, "kg",   False, "",            None),
    ("Pepino",        "pepino",        "legumes",         "produtor2@coverde.pt", "1.20", 180, "un",   False, "",            "Pepino.webp"),
    ("Pimentão",      "pimentao",      "legumes",         "produtor2@coverde.pt", "2.50", 120, "un",   False, "",            "Pimentão.png"),
    ("Abóbora",       "abobora",       "legumes",         "produtor4@coverde.pt", "1.80", 90,  "un",   False, "",            "Abóbora.webp"),
    ("Milho Verde",   "milho-verde",   "legumes",         "produtor4@coverde.pt", "0.60", 200, "un",   False, "",            "Milho Verde.jpg"),
    # Verduras
    ("Alface",        "alface",        "verduras",        "produtor2@coverde.pt", "1.00", 200, "un",   False, "biologico",   "Alface.png"),
    ("Couve",         "couve",         "verduras",        "produtor2@coverde.pt", "1.20", 180, "un",   False, "",            "Couve_Tronchuda.png"),
    ("Espinafre",     "espinafre",     "verduras",        "produtor2@coverde.pt", "2.00", 150, "maco", False, "biologico",   "Espinafre Frescos.jpg"),
    # Hortícolas
    ("Feijão",        "feijao",        "horticolas",      "produtor4@coverde.pt", "2.50", 160, "kg",   False, "",            None),
    ("Grão-de-bico",  "grao-de-bico",  "cereais-e-graos", "produtor4@coverde.pt", "3.00", 130, "kg",   False, "",            None),
    # Cereais e Grãos
    ("Milho Seco",    "milho-seco",    "cereais-e-graos", "produtor4@coverde.pt", "1.50", 200, "kg",   False, "",            None),
    # Azeite
    ("Azeite",        "azeite",        "azeite",          "produtor5@coverde.pt", "8.50", 60,  "l",    True,  "dop",         "Azeite.webp"),
    # Ervas Aromáticas
    ("Salsa",         "salsa",         "ervas-aromaticas","produtor5@coverde.pt", "0.80", 200, "maco", False, "",            None),
    ("Coentros",      "coentros",      "ervas-aromaticas","produtor5@coverde.pt", "0.80", 200, "maco", False, "",            None),
]


class Command(BaseCommand):
    help = "Popula a base de dados com dados de demonstração para o COVERDE"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== COVERDE — Seed de Dados de Demonstração ===\n"))

        cats_created   = self._seed_categories()
        prod_users_created, producers_created = self._seed_producers()
        clients_created = self._seed_clients()
        products_created = self._seed_products()

        self.stdout.write(self.style.SUCCESS("\n=== Resumo ==="))
        self.stdout.write(f"  Categorias criadas/actualizadas : {Category.objects.count()}")
        self.stdout.write(f"  Produtores criados/actualizados : {Producer.objects.count()}")
        self.stdout.write(f"  Clientes criados                : {clients_created}")
        self.stdout.write(f"  Produtos criados/actualizados   : {Product.objects.count()}")
        self.stdout.write(self.style.SUCCESS("\nDone.\n"))

    # ------------------------------------------------------------------
    def _seed_categories(self):
        self.stdout.write("\n[1/4] Categorias…")
        count = 0
        for data in CATEGORIES_DATA:
            obj, created = Category.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "icon": data["icon"],
                    "ordering": data["ordering"],
                    "is_active": True,
                },
            )
            label = "criada" if created else "já existe"
            self.stdout.write(f"    {obj.name} — {label}")
            count += 1
        return count

    # ------------------------------------------------------------------
    def _seed_producers(self):
        self.stdout.write("\n[2/4] Produtores…")
        users_created = 0
        producers_created = 0

        for data in PRODUCERS_DATA:
            # Utilizador
            user, u_created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "user_type": "producer",
                    "is_active": True,
                    "is_verified": True,
                },
            )
            if u_created:
                user.set_password(PRODUCER_PASSWORD)
                user.save()
                users_created += 1

            # Producer
            producer, p_created = Producer.objects.update_or_create(
                user=user,
                defaults={
                    "name": data["company_name"],
                    "description": data["description"],
                    "location": data["location"],
                    "nif": data["nif"],
                    "status": Producer.Status.APPROVED,
                    "is_verified": True,
                    "is_active": True,
                    "verified_at": timezone.now(),
                },
            )
            label = "criado" if p_created else "já existe"
            self.stdout.write(f"    {producer.name} ({user.email}) — {label}")
            if p_created:
                producers_created += 1

        return users_created, producers_created

    # ------------------------------------------------------------------
    def _seed_clients(self):
        self.stdout.write("\n[3/4] Clientes…")
        count = 0
        for data in CLIENTS_DATA:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "user_type": "consumer",
                    "is_active": True,
                    "is_verified": True,
                },
            )
            if created:
                user.set_password(CLIENT_PASSWORD)
                user.save()
                count += 1

            # CustomerProfile
            CustomerProfile.objects.get_or_create(user=user)
            label = "criado" if created else "já existe"
            self.stdout.write(f"    {user.email} — {label}")

        return count

    # ------------------------------------------------------------------
    def _seed_products(self):
        self.stdout.write("\n[4/4] Produtos…")
        count = 0
        media_products_dir = os.path.join("media", "products")

        for (name, slug, cat_slug, prod_email, price, stock, unit,
             is_featured, certification, image_file) in PRODUCTS_DATA:

            try:
                category = Category.objects.get(slug=cat_slug)
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"    Categoria '{cat_slug}' não encontrada, produto '{name}' ignorado."))
                continue

            try:
                producer_user = User.objects.get(email=prod_email)
                producer = Producer.objects.get(user=producer_user)
            except (User.DoesNotExist, Producer.DoesNotExist):
                self.stdout.write(self.style.WARNING(f"    Produtor '{prod_email}' não encontrado, produto '{name}' ignorado."))
                continue

            # Resolver imagem
            image_path = None
            if image_file:
                full_path = os.path.join(media_products_dir, image_file)
                if os.path.exists(full_path):
                    image_path = os.path.join("products", image_file)

            defaults = {
                "name": name,
                "description": f"{name} fresco da {producer.name}, produzido em {producer.location}. Qualidade garantida.",
                "category": category,
                "producer": producer,
                "price": price,
                "stock": stock,
                "unit": unit,
                "is_featured": is_featured,
                "is_active": True,
                "status": "active",
                "certification": certification,
            }
            if image_path:
                defaults["main_image"] = image_path

            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )
            label = "criado" if created else "actualizado"
            img_label = f" [{image_file}]" if image_path else " [sem imagem]"
            self.stdout.write(f"    {product.name} ({category.name}){img_label} — {label}")
            count += 1

        return count
