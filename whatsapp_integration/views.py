from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import WhatsAppInstance, MensagemWhatsApp
from .serializers import WhatsAppInstanceSerializer, MensagemWhatsAppSerializer
from .evolution_client import EvolutionAPIClient
import json

client = EvolutionAPIClient()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_instancia(request):
    """Endpoint para criar nova instância WhatsApp"""
    nome_instancia = request.data.get('nome_instancia')
    
    if not nome_instancia:
        return Response(
            {'erro': 'Nome da instância é obrigatório'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Criar no banco de dados
    instancia = WhatsAppInstance.objects.create(
        user=request.user,
        nome_instancia=nome_instancia
    )
    
    # Criar na Evolution API
    try:
        resultado = client.criar_instancia(nome_instancia)
        
        # Obter QR Code
        qrcode = client.obter_qrcode(nome_instancia)
        instancia.qr_code = qrcode.get('qrcode', {}).get('base64')
        instancia.status = 'qr_ready'
        instancia.save()
        
        serializer = WhatsAppInstanceSerializer(instancia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        instancia.status = 'error'
        instancia.save()
        return Response(
            {'erro': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_mensagem(request):
    """Endpoint para enviar mensagem WhatsApp"""
    instance_id = request.data.get('instance_id')
    numero = request.data.get('numero')
    mensagem = request.data.get('mensagem')
    
    if not all([instance_id, numero, mensagem]):
        return Response(
            {'erro': 'instance_id, numero e mensagem são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    instancia = get_object_or_404(WhatsAppInstance, 
                                  id=instance_id, 
                                  user=request.user)
    
    try:
        resultado = client.enviar_texto(instancia.nome_instancia, 
                                       numero, mensagem)
        
        # Registrar no banco
        msg = MensagemWhatsApp.objects.create(
            instance=instancia,
            numero_destino=numero,
            mensagem=mensagem
        )
        
        serializer = MensagemWhatsAppSerializer(msg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'erro': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_instancias(request):
    """Lista todas as instâncias do usuário"""
    instancias = WhatsAppInstance.objects.filter(user=request.user)
    serializer = WhatsAppInstanceSerializer(instancias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def status_instancia(request, instance_id):
    """Verifica status de uma instância"""
    instancia = get_object_or_404(WhatsAppInstance, 
                                  id=instance_id, 
                                  user=request.user)
    
    try:
        status_api = client.verificar_conexao(instancia.nome_instancia)
        instancia.status = status_api.get('state', 'disconnected').lower()
        instancia.save()
        
        return Response({
            'instance_id': instance_id,
            'status': instancia.status,
            'detalhes': status_api
        })
        
    except Exception as e:
        return Response(
            {'erro': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
import requests
import json

def enviar_whatsapp(numero, texto):
    url = "http://localhost:8080/message/sendText/meuzap" # 'meuzap' é o nome da instancia
    
    payload = {
        "number": numero, # Ex: 5511999999999
        "options": {
            "delay": 1200,
            "presence": "composing"
        },
        "textMessage": {
            "text": texto
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "apikey": "123456"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Exemplo de uso em uma View:
# enviar_whatsapp("5511988887777", "Olá! Teste de integração Django.")

import requests
import json
from .models import MensagemWhatsApp

def disparar_mensagem(numero, texto):
    # 1. Configurações da Evolution API
    url = "http://localhost:8080/message/sendText/meuzap"
    headers = {
        "Content-Type": "application/json",
        "apikey": "123456" # A mesma que você definiu no Docker
    }
    payload = {
        "number": numero,
        "textMessage": {"text": texto}
    }

    try:
        # 2. Tenta enviar para a API
        response = requests.post(url, json=payload, headers=headers)
        status_res = response.json()

        # 3. Salva no seu db.sqlite3
        MensagemWhatsApp.objects.create(
            numero=numero,
            conteudo=texto,
            status_api=status_res
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar: {e}")
        return False