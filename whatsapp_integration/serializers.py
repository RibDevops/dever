from rest_framework import serializers
from .models import WhatsAppInstance, MensagemWhatsApp

class WhatsAppInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppInstance
        fields = ['id', 'nome_instancia', 'numero_telefone', 
                 'status', 'qr_code', 'created_at']
        read_only_fields = ['id', 'qr_code', 'created_at']

class MensagemWhatsAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensagemWhatsApp
        fields = ['id', 'instance', 'numero_destino', 
                 'mensagem', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']