from django.urls import path
from .views import accueil, recherche_article, profil, CustomLogoutView, UtilisateurCreationView, modifier_profil, \
    modifier_panier
from .views import voir_panier, ajouter_panier, supprimer_panier
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
    path('panier/', voir_panier, name='voir_panier'),
    path('ajouter_panier/<int:article_id>/', ajouter_panier, name='ajouter_panier'),
    path('supprimer_panier/<int:article_id>/', supprimer_panier, name='supprimer_panier'),
    path('modifier_panier/<int:article_id>/', modifier_panier, name='modifier_panier'),
]