from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UtilisateurCreationForm, ArticleForm
from .models import Article
from .models import Commande, Paiement
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from urllib.request import urlopen
from .models import Article
from django.http import request
from .models import Panier
from django.conf import settings
from django.http import JsonResponse
from django.views import View

stripe_api_key = settings.STRIPE_SECRET_KEY


def SuccessView(request):
    return render(request, 'succes.html')


def cancelView(request):
    return render(request, 'cancelled.html')


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            article_id = self.kwargs["pk"]
            article = Article.objects.get(id=article_id)
            intent = stripe.PaymentIntent.create(
                amount=article.prix,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "article_id": article.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        article_id = self.kwargs["pk"]
        article = get_object_or_404(Article, id=article_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': article.price,  # Assuming the price field is called "price"
                    'name': article.title,  # Assuming the title field is called "title"
                    'quantity': 1,  # Assuming a quantity of 1 for now
                },
            ],
            metadata={
                "article_id": article.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["article_id"]

        article = Article.objects.get(id=article_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered.",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        article_id = intent["metadata"]["article_id"]

        article = Article.objects.get(id=article_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered.",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)


def accueil(request):
    articles = Article.objects.all()[:]
    context = {'articles': articles,
               'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
               }

    return render(request, 'accueil.html', context)


#def recherche_article(request):
   # query = request.GET.get('q')
   # articles = None
   # if query:
     #   articles = Article.objects.filter(titre__icontains=query)
   # context = {'articles': articles, 'query': query}
   # return render(request, 'recherche_article.html', context)
def recherche_article(request):
    query = request.GET.get('q')  # Récupérer le terme de recherche depuis les paramètres de requête

    articles = Article.objects.all()  # Récupérer tous les articles

    if query:
        # Si un terme de recherche est spécifié, filtrer les articles en fonction du titre ou de la description
        articles = articles.filter(titre__icontains=query) | articles.filter(description__icontains=query) | articles.filter(prix__icontains=query)

    context = {
        'articles': articles,
        'query': query,
    }

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
def mes_articles(request):
    articles_vendus = Article.objects.filter(vendeur=request.user)

    context = {
        'articles_vendus': articles_vendus
    }

    return render(request, 'mes_articles.html', context)


@login_required
def modifier_article(request, id):
    article = get_object_or_404(Article, id=id, vendeur=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('mes_articles')
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'modifier_article.html', context)

#def article_detail(request, id):
   # article = get_object_or_404(Article, id=id, vendeur=request.user)
   # if request.method == 'POST':
    #    form = ArticleForm(request.POST, request.FILES, instance=article)
  #  else:
   #     form = ArticleForm(instance=article)
   # context = {'form': form}
   # return render(request, 'article_dettail.html', context)
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    context = {'article': article}
    return render(request, 'article_dettail.html', context)

@login_required
def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.vendeur = request.user
            article.save()
            return redirect('mes_articles')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'ajouter_article.html', context)


def my_view(request):
    article = Article.objects.first()
    if article.image:
        image_url = article.image.url
    else:
        image_url = None
    context = {'article': article, 'image_url': image_url}
    return render(request, 'my_template.html', context)


def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('mes_articles')
    context = {'article': article}
    return render(request, 'supprimer_article.html', context)


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
                user = form.save()
                update_session_auth_hash(request, user)  # mettre à jour la session de l'utilisateur
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


@login_required
def voir_panier(request):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    if not panier:
        panier = Panier.objects.create(utilisateur=request.user)
    return render(request, 'panier.html', {'panier': panier})


@login_required
def ajouter_panier(request, article_id):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    if not panier:
        panier = Panier.objects.create(utilisateur=request.user)
    article = Article.objects.get(id=article_id)
    panier.ajouter_article(article, 1)
    return redirect('voir_panier')


@login_required
def supprimer_panier(request, article_id):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    article = Article.objects.get(id=article_id)
    panier.supprimer_article(article)
    return redirect('voir_panier')


@login_required
def modifier_panier(request, article_id):
    panier = Panier.objects.filter(utilisateur=request.user).first()
    article = Article.objects.get(id=article_id)
    quantite = int(request.POST.get('quantite'))
    if quantite > 0:
        panier.ajouter_article(article, quantite)
    else:
        panier.supprimer_article(article)
    return redirect('voir_panier')
