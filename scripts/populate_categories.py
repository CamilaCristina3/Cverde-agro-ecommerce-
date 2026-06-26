#!/usr/bin/env python
"""
Script para popular categorias de produtos no banco de dados.
Cria categorias com nomes, descrições e ícones FontAwesome.
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cverde.settings')
django.setup()

from apps.users.models import Category
from django.utils.text import slugify

# Categorias para criar (nome, descrição, ícone FontAwesome)
CATEGORIES_DATA = [
    {
        'name': 'Frutas',
        'description': 'Frutas frescas e sazonais diretamente do produtor',
        'icon': 'apple-alt',
    },
    {
        'name': 'Legumes',
        'description': 'Legumes e hortaliças locais de qualidade premium',
        'icon': 'carrot',
    },
    {
        'name': 'Verduras',
        'description': 'Folhas verdes e saladas cultivadas biologicamente',
        'icon': 'leaf',
    },
    {
        'name': 'Orgânicos',
        'description': 'Produtos certificados biológicos sem pesticidas',
        'icon': 'leaf-heart',
    },
    {
        'name': 'Grãos',
        'description': 'Cereais, leguminosas e sementes integrais',
        'icon': 'sheaf-wheat',
    },
    {
        'name': 'Hortaliças',
        'description': 'Vegetais frescos para cozinha portuguesa',
        'icon': 'seedling',
    },
    {
        'name': 'Vinho',
        'description': 'Vinhos portugueses de qualidade',
        'icon': 'wine-glass-alt',
    },
    {
        'name': 'Azeite',
        'description': 'Azeite virgem extra de produtores locais',
        'icon': 'bottle-droplet',
    },
    {
        'name': 'Queijo e Laticínios',
        'description': 'Produtos lácteos frescos e artesanais',
        'icon': 'cheese',
    },
    {
        'name': 'Mel e Apicultura',
        'description': 'Mel puro, pólen e produtos de abelha',
        'icon': 'jar',
    },
]

def populate_categories():
    """Cria categorias no banco de dados."""
    created_count = 0
    updated_count = 0

    for cat_data in CATEGORIES_DATA:
        slug = slugify(cat_data['name'])
        
        category, created = Category.objects.update_or_create(
            slug=slug,
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'is_active': True,
                'ordering': CATEGORIES_DATA.index(cat_data),
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Criada: {category.name}")
        else:
            updated_count += 1
            print(f"🔄 Atualizada: {category.name}")

    print(f"\n📊 Resumo:")
    print(f"   ✅ Categorias criadas: {created_count}")
    print(f"   🔄 Categorias atualizadas: {updated_count}")
    print(f"   📈 Total de categorias: {Category.objects.count()}")

if __name__ == '__main__':
    print("Populando categorias de produtos...")
    populate_categories()
    print("\n✨ Pronto!")
