import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Usuario, Tarefa, Forum, Avatar, UsuarioTarefa
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models import Sum, Case, When, IntegerField
from django.templatetags.static import static


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
    return render(request, 'EcoKids_Integracao/HomePage.html')

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

    return render(request, 'EcoKids_Integracao/Personagem.html')

def Card(request):
    return render(request, 'EcoKids_Integracao/Card.html')

def ToDoList(request):
    tarefas = Tarefa.objects.all()
    context = {
        'tarefas': tarefas
    }
    return render(request, 'EcoKids_Integracao/ToDoList.html', context)

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
    return render(request, 'EcoKids_Integracao/Mural.html')

def Login2(request):
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
            "avatar_url": static(usuario.avatar_url)  # Ajusta a URL do avatar
        }
        for usuario in usuarios
    ]
    return JsonResponse(data, safe=False)