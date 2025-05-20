from django.contrib import admin
from .models import *

models = [
    Marka, ModelAdi, Makine, MakineTakip, IsTanimi,
    KanunMaddeleri, KanunDosyalari,
    Il, Ilce, Planlamalar, IsinAdi,
    Yatirim
]

for model in models:
    admin.site.register(model)
