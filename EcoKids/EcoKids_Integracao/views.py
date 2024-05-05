import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Usuario, Tarefa, Forum, Avatar
from django.utils import timezone
from django.contrib.auth.hashers import make_password


def get_avatar_url(request):
    user_avatar_url = None
    
    # Verifica se o usuário está logado com base no ID do usuário armazenado na sessão
    user_id = request.session.get('user_id')
    if user_id:
        try:
            # Recupera o usuário com base no ID da sessão
            usuario = Usuario.objects.get(id=user_id)
            
            # Verifica se o usuário possui um avatar
            if usuario.avatar_url:
                user_avatar_url = usuario.avatar_url
                print("A url do avatar é: " + user_avatar_url)
        except Usuario.DoesNotExist:
            pass
    
    # Retorna a URL do avatar como uma resposta JSON
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
        # Se o avatar com o ID especificado não existir, retorne um URL padrão ou None
        return None    
        
from django.urls import reverse

def Personagem(request):
    if request.method == 'POST':
        # Recebendo os dados do formulário
        avatar_id = request.POST.get('avatar_id')  # Recebendo o ID do avatar selecionado
        nome_personagem = request.POST.get('nome_personagem')  # Recebendo o nome do personagem

        # Verificando se o usuário está logado com base no ID do usuário armazenado na sessão
        user_id = request.session.get('user_id')
        if user_id:
            try:
                usuario = Usuario.objects.get(id=user_id)
                # Salvando o personagem selecionado e o ID do avatar para o usuário logado
                usuario.personagem_selecionado = nome_personagem
                usuario.avatar_data_id = avatar_id
                avatar_url = obter_avatar_url_por_id(avatar_id)
                print("A url do avatar é: " + avatar_url)
                usuario.avatar_url = avatar_url  # Salva a URL da imagem no usuário
                usuario.save()
                
                # Retorna a URL do avatar como uma resposta JSON
                return JsonResponse({'avatar_url': avatar_url})

            except Usuario.DoesNotExist:
                pass

    # Se for uma solicitação GET, simplesmente renderizar o template
    return render(request, 'EcoKids_Integracao/Personagem.html')

def Card(request):
    return render(request, 'EcoKids_Integracao/Card.html')

def ToDoList(request):
    tarefas = Tarefa.objects.all() 
    return render(request, 'EcoKids_Integracao/ToDoList.html', {'tarefas': tarefas})

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
                request.session['user_id'] = user.id  # Armazena o ID do usuário na sessão
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

        # Após salvar o usuário, podemos armazenar seu ID na sessão
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
    # Lógica para remover os dados de autenticação da sessão
    if 'user_id' in request.session:
        del request.session['user_id']  # Removendo o ID do usuário da sessão
    
    # Defina a URL do avatar padrão
    default_avatar_url = 'img/avatar-rafael.png'
    print("Logout: " + default_avatar_url)
    # Retorna a URL do avatar padrão como uma resposta JSON
    return JsonResponse({'user_avatar_url': default_avatar_url})





