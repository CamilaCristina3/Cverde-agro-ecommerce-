from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Criar avaliações
    path('product/<int:product_id>/create/', views.create_product_review, name='create_product'),
    path('producer/<int:producer_id>/create/', views.create_producer_review, name='create_producer'),
    
    # Ver avaliações (públicas)
    path('product/<int:product_id>/', views.product_reviews, name='product_list'),
    path('producer/<int:producer_id>/', views.producer_reviews, name='producer_list'),
    
    # Minhas avaliações
    path('my-reviews/', views.my_reviews, name='my_reviews'),
]
