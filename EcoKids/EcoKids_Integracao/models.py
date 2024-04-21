# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome 
    
class Forum(models.Model):
    titulo = models.CharField(max_length=40)
    comentario = models.TextField(max_length=500)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    curtidas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo


class Tarefa(models.Model):
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  
    descricao = models.CharField(max_length=255, null=True) 
    # data_hora = models.DateTimeField(default=timezone.now)  
    pontuacao = models.IntegerField(default=0, null=True) 
    realizada = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"Tarefa de {self.usuario.username} - {self.descricao}"        

