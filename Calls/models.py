from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Setor e Posto Graduações
# Setor e Posto Graduações são modelos que representam as seções e postos de graduação dos usuários do sistema.
class Setor(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome


class Posto_grad(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome


# User é um modelo que estende o modelo AbstractUser do Django, adicionando campos específicos para o sistema de chamados.
# Ele inclui campos para o nome de guerra, setor e posto graduação do usuário.
class User(AbstractUser):
    nome_de_guerra = models.CharField(max_length=50, null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='usuarios', null=True, blank=True)
    posto_grad = models.ForeignKey(Posto_grad, on_delete=models.SET_NULL, related_name='usuarios', null=True, blank=True)


# StatusChamado e PrioridadeChamado são modelos que representam o status e a prioridade dos chamados.
# Eles são usados para categorizar os chamados e facilitar a gestão dos mesmos.
class StatusChamado(models.Model):
    status = models.CharField(max_length=50)
    data_status = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
    
class PrioridadeChamado(models.Model):
    prioridade = models.CharField(max_length=50)


    def __str__(self):
        return self.prioridade
    
class CategoriaChamado(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria
    
    
# Chamado é um modelo que representa um chamado no sistema.
# Ele inclui campos para o título, descrição, status, prioridade, categotia, data de criação e atualização, e o usuário que criou o chamado.
class Chamado(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.ForeignKey(StatusChamado, on_delete=models.SET_NULL, related_name='chamados', null=True, blank=True)
    prioridade = models.ForeignKey(PrioridadeChamado, on_delete=models.SET_NULL, related_name='chamados', null=True, blank=True)
    categoriaChamado = models.ForeignKey(CategoriaChamado, on_delete=models.SET_NULL, related_name='chamados', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chamados')

    def __str__(self):
        return self.titulo
    
    def mensagens_nao_visualizadas(self, usuario_atual):
        return self.mensagens_chamado.filter(
            visualizado=False
        ).exclude(usuario=usuario_atual)
    

# MensagemChamado é um modelo que representa uma mensagem enviada em um chamado.
# Ele inclui campos para o chamado relacionado, o usuário que enviou a mensagem, o conteúdo da mensagem e a data de envio.
class MensagemChamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='mensagens_chamado')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_usuario')
    mensagem = models.TextField()
    imagem = models.ImageField(upload_to='mensagens/', null=True, blank=True)
    video = models.FileField(upload_to='mensagens/', null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.chamado.titulo} - {self.data_envio}"