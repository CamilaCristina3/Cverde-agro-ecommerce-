#!/usr/bin/env python
"""
Script para adicionar imagens de placeholder às categorias de produtos.
Usa picsum.photos como serviço de imagens placeholder.
"""

import os
import sys
import django
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cverde.settings')
django.setup()

from apps.users.models import Category
from django.core.files.base import ContentFile

# Cores para cada categoria (RGB)
CATEGORY_COLORS = {
    'frutas': (220, 53, 69),           # Vermelho
    'legumes': (40, 167, 69),          # Verde
    'verduras': (53, 126, 52),         # Verde escuro
    'orgânicos': (75, 192, 75),        # Verde claro
    'grãos': (200, 140, 80),           # Marrom
    'hortaliças': (107, 174, 35),      # Verde amarelado
    'vinho': (139, 35, 69),            # Vinho/Roxo
    'azeite': (184, 134, 11),          # Ouro
    'queijo e laticínios': (238, 214, 175),  # Bege
    'mel e apicultura': (255, 193, 7),      # Amarelo/Ouro
}

def create_placeholder_image(category_name, color):
    """Cria uma imagem de placeholder com o nome da categoria."""
    # Criar imagem com cor de fundo
    img = Image.new('RGB', (400, 300), color=color)
    draw = ImageDraw.Draw(img)
    
    # Adicionar texto
    text = category_name
    text_bbox = draw.textbbox((0, 0), text, font=None)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255))
    
    # Converter para bytes
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=85)
    img_io.seek(0)
    
    return img_io

def add_images_to_categories():
    """Adiciona imagens às categorias."""
    categories = Category.objects.filter(image='')
    
    for category in categories:
        try:
            slug_lower = category.slug.lower()
            
            # Encontrar a cor correspondente
            color = None
            for key, col in CATEGORY_COLORS.items():
                if key in slug_lower:
                    color = col
                    break
            
            if color is None:
                color = (46, 125, 50)  # Verde padrão
            
            # Criar imagem
            print(f"🎨 Gerando imagem para: {category.name}")
            img_io = create_placeholder_image(category.name, color)
            
            # Salvar no modelo
            filename = f"{category.slug}_image.jpg"
            category.image.save(filename, ContentFile(img_io.read()), save=True)
            
            print(f"✅ Imagem adicionada a: {category.name}")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar imagem a {category.name}: {str(e)}")
    
    print(f"\n✨ Pronto! Adicionadas imagens a {len(list(categories))} categorias.")

if __name__ == '__main__':
    print("Adicionando imagens às categorias...\n")
    add_images_to_categories()
