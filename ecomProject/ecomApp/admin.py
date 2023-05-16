from django.contrib import admin

from .models import Article
from .models import Commande
from .models import Paiement
from .models import *

# aresmouk
# 123456789
admin.site.register(Article)
admin.site.register(Commande)
admin.site.register(Paiement)
admin.site.register(Panier)
admin.site.register(LignePanier)
