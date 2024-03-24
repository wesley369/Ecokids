from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'EcoKids_Integracao/HomePage.html')


def QuemSomos(request):
    return render(request, 'EcoKids_Integracao/QuemSomos.html')    

def Login(request):
    return render(request, 'EcoKids_Integracao/Login.html')    

def Personagem(request):
    return render(request, 'EcoKids_Integracao/Personagem.html')  

def Card(request):
    return render(request, 'EcoKids_Integracao/Card.html')         