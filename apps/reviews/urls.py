from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Criar avaliações
    path('product/<uuid:product_id>/create/', views.create_product_review, name='create_product_uuid'),
    path('product/<int:product_id>/create/', views.create_product_review, name='create_product'),
    path('producer/<uuid:producer_id>/create/', views.create_producer_review, name='create_producer_uuid'),
    path('producer/<int:producer_id>/create/', views.create_producer_review, name='create_producer'),
    
    # Ver avaliações (públicas)
    path('product/<uuid:product_id>/', views.product_reviews, name='product_list_uuid'),
    path('product/<int:product_id>/', views.product_reviews, name='product_list'),
    path('producer/<uuid:producer_id>/', views.producer_reviews, name='producer_list_uuid'),
    path('producer/<int:producer_id>/', views.producer_reviews, name='producer_list'),
    
    # Minhas avaliações
    path('my-reviews/', views.my_reviews, name='my_reviews'),
]
