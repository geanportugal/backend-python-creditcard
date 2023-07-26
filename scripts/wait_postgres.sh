#!/bin/bash

# Nome do container Docker PostgreSQL
CONTAINER_NAME="postgres"

# Tempo de espera entre as tentativas (em segundos)
TEMPO_ESPERA=5

echo "Aguardando o container $CONTAINER_NAME estar pronto para aceitar conexões..."

# Loop para verificar a conexão
while true; do
  # Tenta conectar ao PostgreSQL usando o utilitário pg_isready
  if docker exec $CONTAINER_NAME pg_isready -q; then
    echo "O container $CONTAINER_NAME está pronto para aceitar conexões!"
    break
  fi

  # Aguarda um curto período de tempo antes de tentar novamente
  sleep $TEMPO_ESPERA
done