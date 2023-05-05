import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User

# Ajout du chemin d'accès au répertoire contenant le fichier settings.py
sys.path.append(os.path.abspath('C:/Users/moukhtar/PycharmProjects/ecomProject/ecomProject'))

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomProject.settings')
django.setup()
from ecomProject.ecomApp.models import Article

# URL de la page de résultats de recherche d'Amazon avec des ordinateurs portables
url = "https://www.amazon.com/s?k=laptop&ref=nb_sb_noss_1"

# En-têtes HTTP pour simuler une requête à partir d'un navigateur web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Récupération de la page HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Recherche des éléments contenant les informations sur les ordinateurs portables
results = soup.find_all('div', {'data-component-type': 's-search-result'})

# Boucle sur les résultats pour extraire les informations pertinentes
for result in results:
    try:
        nom = result.find('h2', {'class': 'a-size-mini'}).text.strip()
    except:
        nom = 'N/A'
    try:
        marque = result.find('span', {'class': 'a-size-base-plus a-color-base'}).text.strip()
    except:
        marque = 'N/A'
    try:
        prix = Decimal(result.find('span', {'class': 'a-offscreen'}).text.replace('$', '').replace(',', '').strip())
    except:
        prix = Decimal('0.00')
    try:
        notation = Decimal(result.find('span', {'class': 'a-icon-alt'}).text.split(' ')[0])
    except:
        notation = Decimal('0.0')
    try:
        nombre_commentaires = int(result.find('span', {'class': 'a-size-base'}).text.replace(',', '').split(' ')[0])
    except:
        nombre_commentaires = 0

    # Création d'un utilisateur vendeur pour l'article
    vendeur = User.objects.get_or_create(username='vendeur')[0]

    # Création d'une instance d'article avec les informations extraites
    article = Article(
        nom=nom,
        titre=nom,
        description=f"{marque} - {nom}",
        prix=prix,
        quantite=1,
        image='path/to/my/image.png',
        categorie='Informatique',
        date_creation=datetime.now(),
        vendeur=vendeur,
        etat='Disponible',
    )

    # Enregistrement de l'article dans la base de données
    article.save()
