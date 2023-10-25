from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Tache
from .serializers import TacheSerializer



from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes


class TacheListCreateView(APIView):
    def get_queryset(self):
        # Renvoyer le queryset des tâches de l'utilisateur actuel
        return Tache.objects.filter(utilisateur=self.request.user)

    def get(self, request, *args, **kwargs):
        taches = self.get_queryset()
        serializer = TacheSerializer(taches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'titre': request.data.get('titre'),
            'description': request.data.get('description'),
            'date_limite': request.data.get('date_limite'),
            'priorite': request.data.get('priorite'),
            'etiquettes': request.data.get('etiquettes'),
            'utilisateur': request.user.id
        }
        serializer = TacheSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TacheViewSet(viewsets.ModelViewSet):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer



@authentication_classes([SessionAuthentication])
class MaVueProtegee(APIView):
    def get(self, request):
        return Response()

