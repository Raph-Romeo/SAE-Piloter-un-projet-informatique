from django.db import models


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


from django.db import models
from django.contrib.auth.models import User

PRIORITE_CHOICES = [
    ('Basse', 'Basse'),
    ('Moyenne', 'Moyenne'),
    ('Haute', 'Haute'),
]


class Tache(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_limite = models.DateField()
    priorite = models.CharField(max_length=10)
    etiquettes = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


# class Tache(models.Model):
# id = models.AutoField(primary_key=True)
#  titre = models.CharField(max_length=100)
#  description = models.TextField()
#  date_creation = models.DateTimeField(auto_now_add=True)
#  date_limite = models.DateTimeField()
#  priorite = models.CharField(max_length=20)
#  etiquettes = models.CharField(max_length=100)
# utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

# def __str__(self):
#     return self.titre


class SousTache(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    accomplie = models.BooleanField(default=False)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Affectation(models.Model):
    id = models.AutoField(primary_key=True)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.utilisateur} -> {self.tache}'
