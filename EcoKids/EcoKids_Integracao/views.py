
import json
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import Usuario, Tarefa, Forum, Avatar
from .models import Usuario, Tarefa, Forum, Avatar, UsuarioTarefa
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models import Sum, Case, When, IntegerField
from django.templatetags.static import static
from datetime import timedelta


def get_avatar_url(request):
    user_avatar_url = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            usuario = Usuario.objects.get(id=user_id)
            
            if usuario.avatar_url:
                user_avatar_url = usuario.avatar_url
                print("A url do avatar é: " + user_avatar_url)
        except Usuario.DoesNotExist:
            pass
    
    return JsonResponse({'user_avatar_url': user_avatar_url})

def index(request):
    user_id = request.session.get('user_id')
    return render(request, 'EcoKids_Integracao/HomePage.html', {'user_id': user_id})


def QuemSomos(request):
    return render(request, 'EcoKids_Integracao/QuemSomos.html')

def Login(request):
    return render(request, 'EcoKids_Integracao/Login.html')

def obter_avatar_url_por_id(avatar_id):
    try:
        avatar = Avatar.objects.get(id=avatar_id)
        return avatar.url
    except Avatar.DoesNotExist:
        return None    
        
from django.urls import reverse

def Personagem(request):
    if request.method == 'POST':
        avatar_id = request.POST.get('avatar_id') 
        nome_personagem = request.POST.get('nome_personagem') 

        user_id = request.session.get('user_id')
        if user_id:
            try:
                usuario = Usuario.objects.get(id=user_id)
                usuario.personagem_selecionado = nome_personagem
                usuario.avatar_data_id = avatar_id
                avatar_url = obter_avatar_url_por_id(avatar_id)
                print("A url do avatar é: " + avatar_url)
                usuario.avatar_url = avatar_url  
                usuario.save()
                
                return JsonResponse({'avatar_url': avatar_url})

            except Usuario.DoesNotExist:
                pass

    # Definindo um cookie com a flag HttpOnly
    response = render(request, 'EcoKids_Integracao/Personagem.html')  # Substitua 'sua_pagina.html' pelo caminho da sua página
    response.set_cookie('cookie_name', 'cookie_value', httponly=True, samesite='Strict')
    return response

    return response

def Card(request):
    return render(request, 'EcoKids_Integracao/Card.html')

def ToDoList(request):
    user_id = request.session.get('user_id')
    tarefas = []

    todas_tarefas = Tarefa.objects.all()

    if user_id:
        usuario = get_object_or_404(Usuario, id=user_id)
        usuario_tarefas = UsuarioTarefa.objects.filter(usuario=usuario).select_related('tarefa')
        usuario_tarefas_dict = {ut.tarefa.id: ut.realizada for ut in usuario_tarefas}

        for tarefa in todas_tarefas:
            tarefas.append({
                'id': tarefa.id,
                'descricao': tarefa.descricao,
                'pontuacao': tarefa.pontuacao,
                'realizada': usuario_tarefas_dict.get(tarefa.id, False),
            })
    else:
        for tarefa in todas_tarefas:
            tarefas.append({
                'id': tarefa.id,
                'descricao': tarefa.descricao,
                'pontuacao': tarefa.pontuacao,
                'realizada': False, 
            })

    return render(request, 'EcoKids_Integracao/ToDoList.html', {'tarefas': tarefas})


def marcar_tarefa_realizada(request, tarefa_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id)
            usuario = get_object_or_404(Usuario, id=user_id)
            
            usuario_tarefa, created = UsuarioTarefa.objects.get_or_create(usuario=usuario, tarefa=tarefa)
            
            if not usuario_tarefa.realizada:
                usuario_tarefa.realizada = True
                usuario_tarefa.save()

                usuario.total_pontuacao += tarefa.pontuacao
                usuario.save()
            
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def Mural(request):
    response = HttpResponse('Conteúdo da resposta')
    response.set_cookie('cookie_name', 'cookie_value', httponly=True)

    return render(request, 'EcoKids_Integracao/Mural.html')

def Login2(request):
    # Definindo um cookie com a flag HttpOnly
    response = HttpResponse('Conteúdo da resposta')
    response.set_cookie('cookie_name', 'cookie_value', httponly=True)

    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email').strip() 
        password = data.get('password').strip()

        try:
            user = Usuario.objects.get(email=email)
            if user.senha == password:
                request.session['user_id'] = user.id  
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'An error occurred'}, status=500)
    else:
        return HttpResponseBadRequest('Method not allowed')

def signup(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        novo_usuario.save()

        request.session['user_id'] = novo_usuario.id

        return JsonResponse({'message': 'Usuário cadastrado com sucesso', 'success': True})
    else:
        return JsonResponse({'message': 'Método não permitido'}, status=405)



def mural_comentario(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            data = json.loads(request.body)
            titulo = data.get('titulo')
            comentario = data.get('comentario')
            data_hora = timezone.now()

            novo_comentario = Forum(usuario_id=user_id, titulo=titulo, comentario=comentario, data_hora=data_hora)
            novo_comentario.save()

            return JsonResponse({'message': 'Comentário adicionado com sucesso'}, status=200)
        else:
            return HttpResponseBadRequest('Unauthorized')
    else:
        comentarios = Forum.objects.order_by('-data_hora')[:10]
        comentarios_dict = [
            {'titulo': comentario.titulo, 'comentario': comentario.comentario, 'data_hora': str(comentario.data_hora)}
            for comentario in comentarios
        ]
        return JsonResponse(comentarios_dict, safe=False)


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  
    
    default_avatar_url = 'img/avatar-rafael.png'
    default_avatar_url = 'img/avatar-default.jpg'
    print("Logout: " + default_avatar_url)
    return JsonResponse({'user_avatar_url': default_avatar_url})


def Ranking(request):
    return render(request, 'EcoKids_Integracao/Ranking.html')



def get_ranking_data(request):
    usuarios = Usuario.objects.all().order_by('-total_pontuacao')
    data = [
        {
            "nome": usuario.nome,
            "total_pontuacao": usuario.total_pontuacao,
            "avatar_url": static(usuario.avatar_url)
        }
        for usuario in usuarios
    ]
    return JsonResponse(data, safe=False)

def verificar_atualizacao_tarefas():
    agora = timezone.now()
    tarefas = Tarefa.objects.all()
    for tarefa in tarefas:
        if (agora - tarefa.ultima_atualizacao).total_seconds() > 86400:  # 24 horas
            tarefa.ultima_atualizacao = agora
            tarefa.save()
            UsuarioTarefa.objects.filter(tarefa=tarefa).update(realizada=False)    

def get_tempo_restante(request):
    ultima_atualizacao = Tarefa.objects.latest('ultima_atualizacao').ultima_atualizacao
    agora = timezone.now()
    tempo_restante = timedelta(days=1) - (agora - ultima_atualizacao)

    if tempo_restante.total_seconds() < 0:
        tempo_restante = timedelta(seconds=0)

    return JsonResponse({'tempo_restante': int(tempo_restante.total_seconds())})            




# views.py

from django.shortcuts import render

def generate_nonce():
    import os
    import base64
    return base64.b64encode(os.urandom(16)).decode()

def Mural_Nonce(request):
    nonce = generate_nonce()
    context = {'nonce': nonce}
    return render(request, 'Mural.html', context)

def Card_Nonce(request):
    nonce = generate_nonce()
    context = {'nonce': nonce}
    return render(request, 'Card.html', context)

def HomePage_Nonce(request):
    nonce = generate_nonce()
    context = {'nonce': nonce}
    return render(request, 'HomePage.html', context)

def Personagem_Nonce(request):
    nonce = generate_nonce()
    context = {'nonce': nonce}
    return render(request, 'Personagem.html', context)

# def Login_Nonce(request):
#     nonce = generate_nonce()
#     context = {'nonce': nonce}
#     return render(request, 'Login.html', context)

# def minha_view(request):
#     # Seu código para processar a requisição...

#     # Definindo um cookie com a flag HttpOnly
#     response = HttpResponse('Conteúdo da resposta')
#     response.set_cookie('cookie_name', 'cookie_value', httponly=True)

#     return response