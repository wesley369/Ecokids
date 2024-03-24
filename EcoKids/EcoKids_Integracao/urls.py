from django.urls import path
from . import views

app_name = 'EcoKids_Integracao'

urlpatterns = [
    path('', views.index, name='HomePage'),
    path('quem-somos/', views.QuemSomos, name='QuemSomos'), 
    path('login/', views.Login, name='Login'), 
    path('Personagem/', views.Personagem, name='Personagem'), 
    path('Card/', views.Card, name='Card'), 
]