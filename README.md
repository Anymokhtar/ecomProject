Ce projet est développé en utilisant le framework web Django, la bibliothèque de scraping BeautifulSoup et le système de gestion de base de données MySQL.

Le site web permet aux utilisateurs de créer des comptes, de publier des articles à vendre, de rechercher des articles à acheter, d'ajouter des articles à leur panier et de passer des commandes.
Le projet contient les modèles suivants :
Le modèle Utilisateur stocke les informations sur les utilisateurs, y compris leur nom, adresse e-mail, mot de passe et rôle.
Le modèle Article stocke les informations sur les articles à vendre, y compris leur nom, leur description, leur prix et leur propriétaire.
Le modèle Commande stocke les informations sur les commandes passées par les utilisateurs, y compris la date de la commande, l'utilisateur qui a passé la commande et l'article acheté.
Le modèle Paiement stocke les informations sur les paiements effectués par les utilisateurs, y compris la date du paiement, l'utilisateur qui a effectué le paiement et le montant payé.
Vues :

La page d'accueil affiche les articles les plus récents publiés sur le site.
Les pages de recherche permettent aux utilisateurs de rechercher des articles en fonction de différents critères tels que le nom de l'article, la description et le prix.
Les pages de profil utilisateur affichent les informations de profil de l'utilisateur, y compris les articles qu'il a publiés et les commandes qu'il a passées.
Les pages de gestion de compte permettent aux utilisateurs de modifier leurs informations de profil et de supprimer leur compte.
Les pages de paiement permettent aux utilisateurs de payer pour leurs achats en ligne en utilisant un système de paiement tiers.
Templates :

Les templates sont utilisés pour afficher les données stockées dans les modèles et renvoyer une réponse HTML.
Le système de templates de Django est utilisé pour faciliter la gestion et la personnalisation des mises en page.
Authentification et autorisation :

Django fournit un système d'authentification intégré qui permet aux utilisateurs de créer un compte, de se connecter et de se déconnecter en toute sécurité.
Le système d'autorisation est utilisé pour limiter l'accès aux pages en fonction du rôle de l'utilisateur. Par exemple, les utilisateurs non connectés ne peuvent pas accéder aux pages de gestion de compte et les utilisateurs normaux ne peuvent pas modifier les articles d'autres utilisateurs.
Système de paiement :

Le système de paiement est intégré à l'aide d'une bibliothèque tierce telle que Stripe ou PayPal.
Les utilisateurs peuvent payer pour leurs achats en ligne en utilisant leur carte de crédit ou leur compte PayPal.
Panier :

Le système de panier permet aux utilisateurs d'ajouter des articles à leur panier avant de passer à la caisse.
Les informations sur le panier sont stockées dans la session de l'utilisateur.
Web scraping :

Le script de web scraping utilise la bibliothèque BeautifulSoup pour extraire les informations sur les articles à vendre à partir d'autres sites web.
Les informations sont ensuite importées dans la base de données du site web.
Recherche :
Les utilisateurs peuvent rechercher des articles en fonction de différents critères tels que le nom de l'article, la description et le prix.
Les résultats de la recherche sont affichés sous forme de liste.
Publication d'articles :
Les utilisateurs peuvent publier des articles à vendre en remplissant un formulaire.
Les informations sur les articles sont stockées dans la base de données, y compris le nom de l'article, la description, le prix et le propriétaire.
Les utilisateurs peuvent modifier et supprimer les articles qu'ils ont publiés.
Achat d'articles :
Les utilisateurs peuvent ajouter des articles à leur panier avant de passer à la caisse.
Les informations sur le panier sont stockées dans la session de l'utilisateur.
Les utilisateurs peuvent payer pour leurs achats en ligne en utilisant un système de paiement tiers tel que Stripe.
Les informations sur les commandes et les paiements sont stockées dans la base de données.
Technologies utilisées :

Django pour le développement web.
MySQL pour la base de données.
BeautifulSoup pour le web scraping.
Stripe pour le système de paiement.

