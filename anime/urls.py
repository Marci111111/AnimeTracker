from django.urls import path
from . import views

urlpatterns = [
    path('', views.anime_list, name='anime_list'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('generi/', views.genre_list, name='genre_list'),
    path('studi/', views.studio_list, name='studio_list'),
    path('mia-lista/', views.my_list, name='my_list'),
    path('aggiungi/<int:anime_id>/', views.add_to_list, name='add_to_list'),
    path('rimuovi/<int:anime_id>/', views.remove_from_list, name='remove_from_list'),
    path('recensione/<int:anime_id>/', views.add_review, name='add_review'),
    path('recensione/<int:anime_id>/elimina/', views.delete_review, name='delete_review'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
