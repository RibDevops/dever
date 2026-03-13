#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8080"
API_KEY="123456"

echo -e "${BLUE}=== TESTANDO EVOLUTION API ===${NC}\n"

# Teste 1: Verificar se API está respondendo
echo -e "${YELLOW}Teste 1: Verificando saúde da API...${NC}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)
if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ API está respondendo (HTTP $RESPONSE)${NC}"
else
    echo -e "${RED}❌ API não respondeu corretamente (HTTP $RESPONSE)${NC}"
fi

# Teste 2: Verificar autenticação
echo -e "\n${YELLOW}Teste 2: Verificando autenticação...${NC}"
RESPONSE=$(curl -s -H "apikey: $API_KEY" $API_URL)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Autenticação funcionando${NC}"
    echo -e "${BLUE}Resposta: $RESPONSE${NC}"
else
    echo -e "${RED}❌ Erro na autenticação${NC}"
fi

# Teste 3: Criar uma instância
echo -e "\n${YELLOW}Teste 3: Criando instância de teste...${NC}"
INSTANCE_NAME="teste_$(date +%s)"
RESPONSE=$(curl -s -X POST \
    -H "apikey: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"instanceName\": \"$INSTANCE_NAME\", \"qrcode\": true}" \
    "$API_URL/instance/create")

if [[ $RESPONSE == *"success"* ]] || [[ $RESPONSE == *"instance"* ]]; then
    echo -e "${GREEN}✅ Instância criada com sucesso: $INSTANCE_NAME${NC}"
    echo -e "${BLUE}Resposta: $RESPONSE${NC}"
else
    echo -e "${RED}❌ Erro ao criar instância${NC}"
    echo -e "${RED}Resposta: $RESPONSE${NC}"
fi

# Teste 4: Listar instâncias
echo -e "\n${YELLOW}Teste 4: Listando instâncias...${NC}"
RESPONSE=$(curl -s -H "apikey: $API_KEY" "$API_URL/instance/fetchInstances")
echo -e "${BLUE}Instâncias: $RESPONSE${NC}"

# Teste 5: Verificar se a instância foi criada
echo -e "\n${YELLOW}Teste 5: Verificando status da instância...${NC}"
RESPONSE=$(curl -s -H "apikey: $API_KEY" "$API_URL/instance/connectionState/$INSTANCE_NAME")
echo -e "${BLUE}Status: $RESPONSE${NC}"

echo -e "\n${GREEN}=== TESTES CONCLUÍDOS ===${NC}"
echo -e "${BLUE}Para ver os logs em tempo real: docker-compose logs -f evolution-api${NC}"
echo -e "${BLUE}Para acessar a API: http://localhost:8080${NC}"
echo -e "${BLUE}API Key: $API_KEY${NC}"