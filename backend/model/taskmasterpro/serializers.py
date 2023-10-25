#from rest_framework import serializers
#from .models import Utilisateur

#class UtilisateurSerializer(serializers.ModelSerializer):
 #   class Meta:
    #    model = Utilisateur
 #       fields = '__all__'


from rest_framework import serializers
from .models import Tache

class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = ['titre', 'description', 'date_limite', 'priorite', 'etiquettes']
