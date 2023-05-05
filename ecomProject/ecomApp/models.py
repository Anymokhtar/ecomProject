from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Article(models.Model):
    nom = models.CharField(max_length=200, default='')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    quantite = models.IntegerField()
    image = models.ImageField(upload_to='articles')
    categorie = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)
    etat = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

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


class Panier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='LignePanier')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

    def ajouter_article(self, article, quantite):
        ligne_panier, created = LignePanier.objects.get_or_create(panier=self, article=article)
        if not created:
            ligne_panier.quantite += quantite
            ligne_panier.save()
        else:
            ligne_panier.quantite = quantite
            ligne_panier.save()
        self.maj_total()

    def supprimer_article(self, article):
        ligne_panier = LignePanier.objects.get(panier=self, article=article)
        ligne_panier.delete()
        self.maj_total()

    def maj_total(self):
        self.total = sum(ligne_panier.sous_total() for ligne_panier in self.lignes_panier.all())
        self.save()


class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='lignes_panier')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.article.titre}"

    def sous_total(self):
        return self.quantite * self.article.prix
