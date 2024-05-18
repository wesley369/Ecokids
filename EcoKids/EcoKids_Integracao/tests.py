from django.test import TestCase
from .models import Usuario as UsuarioModel, Forum, Tarefa, Avatar

# Testes para o modelo Usuario
class TesteModeloUsuario(TestCase):
    # Configuração dos dados de teste antes da execução dos testes
    @classmethod
    def setUpTestData(cls):
        # Criando um usuário de teste para ser usado nos testes
        UsuarioModel.objects.create(nome='Teste', email='teste@exemplo.com', senha='senha')

    # Teste para verificar se o rótulo do campo 'nome' está correto
    def test_label_nome(self):
        # Obtém o usuário de teste
        usuario = UsuarioModel.objects.get(email='teste@exemplo.com')
        # Obtém o rótulo do campo 'nome' do modelo Usuario
        nome_campo = usuario._meta.get_field('nome').verbose_name
        # Verifica se o rótulo do campo 'nome' é 'nome'
        self.assertEqual(nome_campo, 'nome')

    # Teste para verificar se a restrição de email único está funcionando corretamente
    def test_email_unico(self):
        # Tenta criar um novo usuário com o mesmo email
        usuario = UsuarioModel(nome='Teste2', email='teste@exemplo.com', senha='senha')
        # Verifica se uma exceção é levantada
        with self.assertRaises(Exception):
            usuario.save()

    # Teste para verificar a representação em string do usuário
    def test_str(self):
        # Obtém o usuário de teste
        usuario = UsuarioModel.objects.get(email='teste@exemplo.com')
        # Verifica se a representação em string do usuário é seu nome
        self.assertEqual(str(usuario), usuario.nome)

    # Teste para verificar se o campo 'personagem_selecionado' é nulo por padrão
    def test_personagem_selecionado_padrao(self):
        # Obtém o usuário de teste
        usuario = UsuarioModel.objects.get(email='teste@exemplo.com')
        # Verifica se o campo 'personagem_selecionado' é None
        self.assertIsNone(usuario.personagem_selecionado)

# Testes para o modelo Forum
class TesteModeloForum(TestCase):
    # Configuração dos dados de teste antes da execução dos testes
    @classmethod
    def setUpTestData(cls):
        # Criando um usuário de teste para ser usado na criação de um fórum
        usuario = UsuarioModel.objects.create(nome='Teste', email='teste@exemplo.com', senha='senha')
        # Criando um fórum de teste associado ao usuário de teste
        Forum.objects.create(usuario=usuario, titulo='Título', comentario='Comentário')

    # Teste para verificar a representação em string do fórum
    def test_str(self):
        # Obtém o fórum de teste
        forum = Forum.objects.get(titulo='Título')
        # Verifica se a representação em string do fórum é seu título
        self.assertEqual(str(forum), forum.titulo)

    # Teste para verificar se o campo 'curtidas' é 0 por padrão
    def test_curtidas_padrao(self):
        # Obtém o fórum de teste
        forum = Forum.objects.get(titulo='Título')
        # Verifica se o número de curtidas do fórum é 0
        self.assertEqual(forum.curtidas, 0)

# Testes para o modelo Avatar
class TesteModeloAvatar(TestCase):
    # Configuração dos dados de teste antes da execução dos testes
    @classmethod
    def setUpTestData(cls):
        # Criando um avatar de teste
        Avatar.objects.create(nome='Avatar1', url='http://exemplo.com/avatar1')

    # Teste para verificar a representação em string do avatar
    def test_str(self):
        # Obtém o avatar de teste
        avatar = Avatar.objects.get(nome='Avatar1')
        # Verifica se a representação em string do avatar é seu nome
        self.assertEqual(str(avatar), avatar.nome)

    # Teste para verificar se o campo 'url' do modelo Avatar tem o comprimento máximo correto
    def test_comprimento_maximo_url(self):
        # Obtém o avatar de teste
        avatar = Avatar.objects.get(nome='Avatar1')
        # Obtém o comprimento máximo do campo 'url' do modelo Avatar
        comprimento_maximo = avatar._meta.get_field('url').max_length
        # Verifica se o comprimento máximo do campo 'url' é 255
        self.assertEqual(comprimento_maximo, 255)
