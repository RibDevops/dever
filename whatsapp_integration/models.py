from django.db import models
from django.contrib.auth.models import User

class WhatsAppInstance(models.Model):
    STATUS_CHOICES = [
        ('creating', 'Criando'),
        ('qr_ready', 'Aguardando QR Code'),
        ('connected', 'Conectado'),
        ('disconnected', 'Desconectado'),
        ('error', 'Erro'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_instancia = models.CharField(max_length=100, unique=True)
    numero_telefone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='creating')
    qr_code = models.TextField(blank=True, null=True)  # Armazenar QR code em base64
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome_instancia} - {self.status}"

class MensagemWhatsApp(models.Model):
    instance = models.ForeignKey(WhatsAppInstance, on_delete=models.CASCADE)
    numero_destino = models.CharField(max_length=20)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=20, default='text')
    status = models.CharField(max_length=20, default='enviado')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.instance.nome_instancia} - {self.numero_destino}"
    
from django.db import models

class RegistroEnvio(models.Model):
    # O SQLite do Django cuidará disso
    celular = models.CharField(max_length=20)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.celular} - {self.data_envio}"
