# Generated by Django 4.1.7 on 2023-04-24 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantite', models.IntegerField()),
                ('image', models.ImageField(upload_to='articles')),
                ('categorie', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('etat', models.CharField(max_length=200)),
                ('vendeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse_livraison', models.CharField(max_length=200)),
                ('mode_paiement', models.CharField(max_length=200)),
                ('statut', models.CharField(max_length=200)),
                ('articles', models.ManyToManyField(to='ecomApp.article')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=8)),
                ('mode_paiement', models.CharField(max_length=200)),
                ('date_paiement', models.DateTimeField(auto_now_add=True)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomApp.commande')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
