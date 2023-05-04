from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    quantite = models.IntegerField()
    image = models.ImageField(upload_to='articles')
    categorie = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)
    etat = models.CharField(max_length=200)


class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)
    adresse_livraison = models.CharField(max_length=200)
    mode_paiement = models.CharField(max_length=200)
    statut = models.CharField(max_length=200)


class Paiement(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    mode_paiement = models.CharField(max_length=200)
    date_paiement = models.DateTimeField(auto_now_add=True)
