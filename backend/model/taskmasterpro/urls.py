from django.urls import path
from .import views

urlpatterns = [
    path('/bonjour',views.page_vide)
]