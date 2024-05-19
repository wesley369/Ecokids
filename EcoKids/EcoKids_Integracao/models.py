# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    personagem_selecionado = models.CharField(max_length=100, blank=True, null=True)
    avatar_data_id = models.CharField(max_length=100, blank=True, null=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    total_pontuacao = models.IntegerField(default=0) 

    def __str__(self):
        return self.nome  

class Forum(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=40)
    comentario = models.TextField(max_length=500)
    data_hora = models.DateTimeField(auto_now_add=True)
    curtidas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

class Tarefa(models.Model):
    descricao = models.CharField(max_length=255, null=True)
    pontuacao = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"Tarefa - {self.descricao}"

class UsuarioTarefa(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    realizada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.nome} - {self.tarefa.descricao}"      

class Avatar(models.Model):
    nome = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
