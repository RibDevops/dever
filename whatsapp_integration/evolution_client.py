import requests
import json
from django.conf import settings

class EvolutionAPIClient:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API['BASE_URL']
        self.api_key = settings.EVOLUTION_API['API_KEY']
        self.headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def criar_instancia(self, instance_name):
        """Cria uma nova instância do WhatsApp"""
        url = f"{self.base_url}/instance/create"
        payload = {
            "instanceName": instance_name,
            "qrcode": True
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def obter_qrcode(self, instance_name):
        """Obtém o QR Code para conexão do WhatsApp"""
        url = f"{self.base_url}/instance/connect/{instance_name}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def enviar_texto(self, instance_name, numero, mensagem):
        """Envia uma mensagem de texto"""
        url = f"{self.base_url}/message/sendText/{instance_name}"
        payload = {
            "number": numero,
            "text": mensagem
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def verificar_conexao(self, instance_name):
        """Verifica o status da conexão"""
        url = f"{self.base_url}/instance/connectionState/{instance_name}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def logout(self, instance_name):
        """Desconecta uma instância"""
        url = f"{self.base_url}/instance/logout/{instance_name}"
        response = requests.delete(url, headers=self.headers)
        return response.json()