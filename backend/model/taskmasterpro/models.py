from django.db import models
# models.py
from django.db import models

class VotreModele(models.Model):
    champ_1 = models.CharField(max_length=100)
    champ_2 = models.IntegerField()