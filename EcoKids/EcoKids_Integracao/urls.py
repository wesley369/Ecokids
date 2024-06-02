from django.urls import path
from . import views

app_name = 'EcoKids_Integracao'

urlpatterns = [
    path('', views.index, name='HomePage'),
    path('quem-somos/', views.QuemSomos, name='QuemSomos'), 
    path('login/', views.Login, name='Login'), 
    path('Personagem/', views.Personagem, name='Personagem'), 
    path('Card/', views.Card, name='Card'), 
    path('login2/', views.Login2, name='Login2'),
    path('signup/', views.signup, name='signup'),
    path('ToDoList/', views.ToDoList, name='ToDoList'),
    path('Mural/', views.Mural, name='Mural'),
    path('AdicionarComentario/', views.mural_comentario, name='AdicionarComentario'),
    path('logout/', views.logout, name='logout'),
    path('get_avatar_url/', views.get_avatar_url, name='get_avatar_url'),
    path('Ranking/', views.Ranking, name='Ranking'),
    path('marcar-tarefa-realizada/<int:tarefa_id>/', views.marcar_tarefa_realizada, name='marcar_tarefa_realizada'),
    path('api/get-ranking-data/', views.get_ranking_data, name='get_ranking_data'),
    path('get_tempo_restante/', views.get_tempo_restante, name='get_tempo_restante'),
    path('generate_nonce/', views.generate_nonce, name='generate_nonce'),
    path('Mural_Nonce/', views.Mural_Nonce, name='Mural_Nonce'),
    path('Card_Nonce/', views.Card_Nonce, name='Card_Nonce'),
    path('HomePage_Nonce/', views.HomePage_Nonce, name='HomePage_Nonce'),
    path('Personagem_Nonce/', views.Personagem_Nonce, name='Personagem_Nonce')
    # path('Login_Nonce/', views.Login_Nonce, name='Login_Nonce')
]