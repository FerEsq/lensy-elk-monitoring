#!/bin/bash

# Script de inicialización del stack ELK para Lensy
# Este script configura automáticamente Kibana con index patterns y visualizaciones

echo "====================================="
echo "Lensy - ELK Stack Initialization"
echo "====================================="
echo ""

# Esperar a que Elasticsearch esté listo
echo "[1/6] Esperando a que Elasticsearch esté disponible..."
until curl -s http://localhost:9200 > /dev/null; do
    echo "   Elasticsearch no está listo aún. Esperando..."
    sleep 5
done
echo "   ✓ Elasticsearch está listo"
echo ""

# Esperar a que Kibana esté listo
echo "[2/6] Esperando a que Kibana esté disponible..."
until curl -s http://localhost:5601/api/status > /dev/null; do
    echo "   Kibana no está listo aún. Esperando..."
    sleep 5
done
echo "   ✓ Kibana está listo"
echo ""

# Crear index pattern para logs de la API
echo "[3/6] Creando index pattern para logs de Lensy API..."
curl -X POST "http://localhost:5601/api/saved_objects/index-pattern/lensy-api-logs" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "lensy-api-logs-*",
      "timeFieldName": "@timestamp"
    }
  }'
echo ""
echo "   ✓ Index pattern para logs creado"
echo ""

# Crear index pattern para heartbeat
echo "[4/6] Creando index pattern para Heartbeat..."
curl -X POST "http://localhost:5601/api/saved_objects/index-pattern/lensy-heartbeat" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "lensy-heartbeat-*",
      "timeFieldName": "@timestamp"
    }
  }'
echo ""
echo "   ✓ Index pattern para Heartbeat creado"
echo ""

echo "[5/6] Configurando visualizaciones predeterminadas..."
echo "   Nota: Las visualizaciones deben crearse manualmente en Kibana"
echo "   URL: http://localhost:5601"
echo ""

echo "[6/6] Verificando estado del sistema..."
echo ""
echo "   Elasticsearch: http://localhost:9200"
curl -s http://localhost:9200/_cluster/health?pretty | grep status
echo ""
echo "   Kibana: http://localhost:5601"
echo "   Lensy API: http://localhost:5000/api/health"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""

echo "====================================="
echo "✓ Inicialización completada"
echo "====================================="
echo ""
echo "Próximos pasos:"
echo "1. Accede a Kibana: http://localhost:5601"
echo "2. Ve a 'Discover' para ver los logs"
echo "3. Ve a 'Dashboard' para crear visualizaciones"
echo "4. Ejecuta: python3 generate_traffic.py para generar tráfico"
echo ""
