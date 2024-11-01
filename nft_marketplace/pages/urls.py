from django.urls import path, register_converter
from . import views


urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('about/', views.about_us, name='about'),
    path('nfts/collections/', views.collections, name='collections'),
    path('feedback/', views.feedback, name='feedback'),
    path('profile/', views.profile, name='profile'),
    path('nfts/collections/<str:collection_address>/', views.collections_items, name='collections_id'),
    path('nfts/<str:nft_address>/', views.nft_item, name='nft_id'),
    # path('nfts/collections/<str:collections_nft_address>/items', views.collections_nft_items, name='nft_id'),

    # path('post/<int:post_id>/', views.show_post, name='post'),
]

