# views.py
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseNotAllowed
from .models import Usuario, Tarefa
from django.utils import timezone
from django.http import JsonResponse
from .models import Forum
from django.core.serializers import serialize
from datetime import date

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

def ToDoList(request):
    tarefas = Tarefa.objects.all() 
    return render(request, 'EcoKids_Integracao/ToDoList.html', {'tarefas': tarefas})

def Mural(request):
    return render(request, 'Ecokids_Integracao/Mural.html')

def Login2(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email').strip() 
        password = data.get('password').strip()
        
        print("Email recebido (antes da consulta):", email)

        try:
            print("Consultando usuário com email:", email)
     
            user = Usuario.objects.get(email=email)
            
            if user and user.senha == password:
                print("Usuário encontrado:", user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                print("Usuário não encontrado ou senha incorreta.")
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except Usuario.DoesNotExist:
            print("Usuário não encontrado.")
            return JsonResponse({'message': 'User does not exist'}, status=401)
        except Exception as e:
            print("Erro:", e)
            return JsonResponse({'message': 'An error occurred'}, status=500)
    else:
        print("Solicitação não permitida.")
        return HttpResponseBadRequest('Method not allowed')

def signup(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        print(nome)
        print(email)
        print(senha)


        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        novo_usuario.save()


        return JsonResponse({'message': 'Usuário cadastrado com sucesso', 'success': True})
    else:
        return JsonResponse({'message': 'Método não permitido'}, status=405)

def mural_comentario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titulo = data.get('titulo')
        comentario = data.get('comentario')
        # usuario = request.user
        data_hora = timezone.now()

        novo_comentario = Forum(titulo=titulo, comentario=comentario, data_hora=data_hora)
        novo_comentario.save()

        return JsonResponse({'message': 'Comentário adicionado com sucesso'}, status=200)
    else:
        comentarios = Forum.objects.order_by('-data_hora')[:10]

        # Criar uma lista de dicionários contendo apenas os campos relevantes
        comentarios_dict = [
            {'titulo': comentario.titulo, 'comentario': comentario.comentario, 'data_hora': str(comentario.data_hora)}
            for comentario in comentarios
        ]

        # Enviar os comentários como resposta
        return JsonResponse(comentarios_dict, safe=False)


# def lista_tarefas(request):
#     tarefas = Tarefa.objects.filter(data_hora__date=date.today())

#     return render(request, 'EcoKids_Integracao/ToDoList.html', {'tarefas': tarefas})



# def lista_tarefas(request):
#     tarefas = Tarefa.objects.all()
#     return render(request, 'EcoKids_Integracao/ToDoList.html', {'tarefas': tarefas})    