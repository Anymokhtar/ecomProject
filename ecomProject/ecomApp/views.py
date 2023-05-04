from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .models import Commande, Paiement
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from .forms import UtilisateurCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from urllib.request import urlopen
from .models import Article
from django.http import request

from .scrape_amazon_laptops import scrape_amazon_laptops


def scrape_laptops_view(request):
    # appeler la fonction de scraping et enregistrer les données dans la base de données
    scrape_amazon_laptops(request)

    # afficher une réponse de confirmation
    return render(request, 'confirmation.html',
                  {'message': 'Les laptops ont été scrape avec succès à partir d\'Amazon.'})


def accueil(request):
    articles = Article.objects.all()[:4]
    context = {'articles': articles}
    return render(request, 'accueil.html', context)


def recherche_article(request):
    query = request.GET.get('q')
    articles = None
    if query:
        articles = Article.objects.filter(titre__icontains=query)
    context = {'articles': articles, 'query': query}
    return render(request, 'recherche_article.html', context)


# Vue de connexion personnalisée
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


# Vue de déconnexion personnalisée
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accueil')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 302:
            return redirect(self.next_page)
        return response


# Vue pour créer un compte
class UtilisateurCreationView(CreateView):
    model = User
    form_class = UtilisateurCreationForm
    template_name = 'registration/inscription.html'
    success_url = reverse_lazy('login')


@login_required
def profil(request):
    commandes = Commande.objects.filter(utilisateur=request.user)
    paiements = Paiement.objects.filter(utilisateur=request.user)
    context = {'commandes': commandes, 'paiements': paiements}
    return render(request, 'profil.html', context)


@login_required
def modifier_profil(request):
    user = request.user
    if request.method == 'POST':
        if 'change_username' in request.POST:
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Le nom d\'utilisateur a été modifié avec succès.')
                return redirect('profil')
        elif 'change_email' in request.POST:
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'L\'adresse email a été modifiée avec succès.')
                return redirect('profil')
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Le mot de passe a été modifié avec succès.')
                return redirect('profil')
        elif 'delete_account' in request.POST:
            user.delete()
            messages.success(request, 'Votre compte a été supprimé avec succès.')
            return redirect('home')
    else:
        form_username = UserChangeForm(instance=user)
        form_email = UserChangeForm(instance=user)
        form_password = PasswordChangeForm(user=user)
    context = {'form_username': form_username, 'form_email': form_email, 'form_password': form_password}
    return render(request, 'modifier_profil.html', context)
