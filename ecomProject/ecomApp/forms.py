from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Article


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation des labels
        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['email'].label = 'Adresse email'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmation du mot de passe'



class ArticleForm(forms.ModelForm):
    '''Formulaire de création/modification d'un article'''

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Article
        fields = ['titre', 'description', 'prix', 'quantite', 'categorie', 'image', 'etat']
        labels = {
            'titre': 'Titre de l\'article',
            'description': 'Description',
            'prix': 'Prix',
            'quantite': 'Quantité',
            'categorie': 'Catégorie',
            'image': 'Photo de l\'article',
            'etat': 'État'
        }
        error_messages = {
            'titre': {'required': 'Le titre de l\'article est requis.'},
            'description': {'required': 'La description de l\'article est requise.'},
            'prix': {'required': 'Le prix de l\'article est requis.'},
            'quantite': {'required': 'La quantité de l\'article est requise.'},
            'categorie': {'required': 'La catégorie de l\'article est requise.'},
            'etat': {'required': 'L\'état de l\'article est requis.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
