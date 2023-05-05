from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Article


class UtilisateurCreationForm(UserCreationForm):
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

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur.email = self.cleaned_data['email']

        if commit:
            utilisateur.save()

        return utilisateur


class ArticleForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Article
        fields = ['nom', 'description', 'prix', 'photo']
        labels = {
            'nom': 'Nom de l\'article',
            'description': 'Description',
            'prix': 'Prix',
            'photo': 'Photo de l\'article'
        }
        error_messages = {
            'nom': {'required': 'Le nom de l\'article est requis.'},
            'description': {'required': 'La description de l\'article est requise.'},
            'prix': {'required': 'Le prix de l\'article est requis.'},
            'photo': {'required': 'Une photo de l\'article est requise.'},
        }

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix <= 0:
            raise forms.ValidationError('Le prix doit être supérieur à zéro.')
        return prix
