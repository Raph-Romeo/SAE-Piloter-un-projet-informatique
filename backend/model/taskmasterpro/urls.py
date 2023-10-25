from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import TacheViewSet
from .views import TacheListCreateView
from rest_framework.authtoken.views import obtain_auth_token
# router = DefaultRouter()
# router.register(r'taches', TacheViewSet)


from django.urls import path
from .views import MaVueProtegee

from .views import *

from django.contrib.auth.decorators import login_required





urlpatterns = [

    path('/login/', login_required(MaVueProtegee.as_view()), name='login'),
    # path('taches/', views.liste_taches),
    # path('ajouter_tache/', views.ajouter_tache, name='ajouter_tache'),
    # path('api/taches/', views.TacheListCreateView.as_view(), name='tache-list-create'),
    # path('api/taches/<int:pk>/', views.TacheRetrieveUpdateDestroyView.as_view(), name='tache-retrieve-update-destroy'),
    path('/api', TacheListCreateView.as_view()),
    # path('api/token/', obtain_auth_token, name='api_token'),
    path('/ma_vue_protegee', MaVueProtegee.as_view(), name='ma_vue_protegee'),
    # Définissez d'autres URL ici
    # ... d'autres URLs pour mettre à jour, supprimer des tâches, etc.
]
# urlpatterns += router.urls





