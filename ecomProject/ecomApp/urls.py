from django.urls import path
from .views import accueil, recherche_article, profil, CustomLogoutView, UtilisateurCreationView, modifier_profil

from .views import CustomLoginView
urlpatterns = [
    path('', accueil, name='accueil'),
    path('recherche/', recherche_article, name='recherche'),
    path('profil/', profil, name='profil'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('inscription/', UtilisateurCreationView.as_view(), name='inscription'),
    path('accounts/profile/', profil, name='profile'),
    path('modifier_profil/', modifier_profil, name='modifier_profil'),
]