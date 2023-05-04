import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from urllib.request import urlopen
from .models import Article

def scrape_amazon_laptops(request):
    url = 'https://www.amazon.com/s?k=laptop&ref=nb_sb_noss_1'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for item in soup.find_all('div', {'class': 's-result-item'}):
        try:
            title = item.find('h2').text.strip()
            description = item.find('div', {'class': 'a-row a-size-base a-color-base'}).text.strip()
            price = item.find('span', {'class': 'a-offscreen'}).text.strip()
            image_url = item.find('img', {'class': 's-image'})['src']
            quantity = 10 # vous pouvez définir une valeur par défaut
            category = 'Laptops' # vous pouvez définir une valeur par défaut
            seller = request.user # vous devez définir le vendeur en fonction de votre application
            state = 'nouveau' # vous pouvez définir une valeur par défaut

            # enregistrer l'image localement et l'ajouter au modèle Article
            img_temp = urlopen(image_url)
            image_field = ContentFile(img_temp.read())
            image_name = image_url.split('/')[-1]
            article = Article(titre=title, description=description, prix=price, quantite=quantity,
                              image=image_name, categorie=category, vendeur=seller, etat=state)
            article.image.save(image_name, image_field, save=True)
            article.save()

            # afficher les valeurs des variables pour chaque élément traité
            print('Title:', title)
            print('Description:', description)
            print('Price:', price)
            print('Image URL:', image_url)
            print('Quantity:', quantity)
            print('Category:', category)
            print('Seller:', seller)
            print('State:', state)
        except:
            pass # ignorer les erreurs et continuer à traiter les autres éléments