from django.urls import path
from .views import accueil, recherche_article, profil, CustomLogoutView, UtilisateurCreationView, modifier_profil, \
    modifier_panier, modifier_article
from .views import voir_panier, ajouter_panier, supprimer_panier
from .views import CustomLoginView
from . import views
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
    path('mes_articles/', views.mes_articles, name='mes_articles'),
    path('modifier_article/<int:id>/', modifier_article, name='modifier_article'),
    path('articles/<int:article_id>/supprimer/', views.supprimer_article, name='supprimer_article'),
]