from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


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