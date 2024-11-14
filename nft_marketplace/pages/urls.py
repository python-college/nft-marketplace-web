from django.urls import path, register_converter
from . import views


urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('about/', views.about_us, name='about'),
    path('nfts/collections/', views.collections, name='collections'),
    path('feedback/', views.feedback, name='feedback'),
    path('profile/<str:address>/', views.profile, name='profile'),
    path('nfts/collections/<str:collection_address>/', views.collections_items, name='collections_id'),
    path('nfts/collections/<str:collection_address>/<str:nft_item_address>/', views.nft_item, name='nft_id'),
    path('nfts/create/nft_collection', views.mint_collection, name='mint_collection'),
    path('nfts/create/nft_collection/<str:collection_address>/nft', views.mint_nft, name='mint_nft'),
]

