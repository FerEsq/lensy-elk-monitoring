# Lensy - Sistema de Monitoreo ELK 📊

![Docker](https://img.shields.io/badge/Docker-20.10+-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.11-orange)
![Kibana](https://img.shields.io/badge/Kibana-8.11-pink)
![License](https://img.shields.io/badge/License-MIT-yellow)
![UVG](https://img.shields.io/badge/UVG-CC3047-red)

Sistema completo de monitoreo y observabilidad utilizando ELK Stack (Elasticsearch, Logstash/Filebeat, Kibana) para la plataforma Lensy - Una solución SaaS que conecta profesionales creativos con clientes.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Dashboard](#-dashboard)
- [Documentación](#-documentación)
- [Equipo](#-equipo)
- [Licencia](#-licencia)

---

## ✨ Características

- ✅ **Stack ELK Completo** - Elasticsearch, Kibana, Filebeat y Heartbeat
- ✅ **API REST de Lensy** - 8 endpoints con generación automática de logs
- ✅ **Logs Estructurados** - Formato JSON con campos estandarizados
- ✅ **Dashboard Pre-configurado** - 6 visualizaciones listas para usar
- ✅ **Monitoreo de Uptime** - Verificación automática cada 30 segundos
- ✅ **Scripts de Automatización** - Setup y generación de tráfico
- ✅ **Containerizado** - Docker Compose para deployment fácil
- ✅ **Documentación Completa** - Guías paso a paso

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│           Lensy Monitoring System            │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────┐    ┌──────────┐              │
│  │ Lensy   │───▶│ Filebeat │              │
│  │  API    │    └────┬─────┘              │
│  │(Flask)  │         │                     │
│  └────┬────┘         │                     │
│       │              ▼                     │
│       │       ┌──────────────┐            │
│       │       │Elasticsearch │            │
│       │       └──────┬───────┘            │
│       │              │                     │
│       ▼              ▼                     │
│  ┌──────────┐  ┌─────────┐               │
│  │Heartbeat │─▶│ Kibana  │               │
│  └──────────┘  └─────────┘               │
│                                             │
└─────────────────────────────────────────────┘
```

### Componentes:

- **Lensy API (Flask)**: API REST que simula operaciones de la plataforma
- **Elasticsearch**: Motor de búsqueda y almacenamiento de logs
- **Kibana**: Interfaz de visualización y análisis
- **Filebeat**: Recolección y envío de logs desde archivos
- **Heartbeat**: Monitoreo de disponibilidad de servicios

---

## 📦 Requisitos

### Software Requerido:
- **Docker** 20.10 o superior
- **Docker Compose** 2.0 o superior
- **Python** 3.11 o superior
- **Git** (para clonar el repositorio)

### Recursos del Sistema:
- **RAM**: Mínimo 8GB
- **Disco**: Mínimo 10GB disponibles
- **CPU**: 2 cores recomendado

### Sistemas Operativos Soportados:
- Linux (Ubuntu 20.04+, Debian 11+, etc.)
- macOS (10.15+)
- Windows 10/11 con WSL2

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/lensy-elk-monitoring.git
cd lensy-elk-monitoring
```

### 2. Preparar el Entorno

```bash
# Dar permisos al script de setup
chmod +x scripts/setup.sh

# Crear directorio y archivo de logs
mkdir -p logs
touch logs/lensy-api.log
chmod 666 logs/lensy-api.log
```

### 3. Levantar el Stack

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs de inicio
docker-compose logs -f
```

### 4. Inicializar Kibana

```bash
# Esperar 2-3 minutos para que Elasticsearch y Kibana inicien completamente
# Luego ejecutar:
./scripts/setup.sh
```

Este script creará automáticamente los index patterns necesarios en Kibana.

### 5. Generar Datos de Prueba

```bash
# Instalar dependencias
pip install requests

# Ejecutar generador de tráfico
python3 scripts/generate_traffic.py
```

Deja el generador corriendo por 10-15 minutos para generar suficientes logs.

---

## 💻 Uso

### Acceso a Servicios

Una vez que todo esté corriendo, puedes acceder a:

- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200
- **Lensy API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

### Verificar que Todo Funciona

```bash
# Ver estado de contenedores
docker-compose ps

# Verificar Elasticsearch
curl http://localhost:9200

# Verificar Kibana
curl http://localhost:5601/api/status

# Verificar API de Lensy
curl http://localhost:5000/api/health

# Ver logs generados
tail -f logs/lensy-api.log

# Contar logs (debe haber 50+)
wc -l logs/lensy-api.log
```

### Endpoints de la API

La API de Lensy incluye los siguientes endpoints:

- `GET /api/health` - Health check
- `GET /api/professionals` - Listar profesionales
- `GET /api/professionals/:id` - Obtener profesional específico
- `POST /api/projects` - Crear proyecto
- `GET /api/projects/:id` - Obtener proyecto
- `POST /api/checkout` - Procesar pago
- `POST /api/login` - Autenticación
- `GET /api/search` - Buscar profesionales

---

## 📊 Dashboard

El proyecto incluye un dashboard completo en Kibana con 6 visualizaciones:

### Visualizaciones Principales:

1. **Traffic - Requests Over Time** 📈
   - Gráfico de barras mostrando el volumen de requests
   - Desglosado por método HTTP (GET, POST, etc.)

2. **HTTP Status Distribution** 🥧
   - Gráfico de dona con la distribución de códigos de respuesta
   - Identifica patrones de éxito/error

3. **Average Response Time** ⏱️
   - Métrica del tiempo promedio de respuesta en milisegundos
   - Indicador de performance del sistema

4. **Top Endpoints** 📍
   - Gráfico de barras horizontales
   - Muestra los 10 endpoints más consultados

5. **Error Rate** ⚠️
   - Gráfico de línea con la tendencia de errores
   - Filtrado por status_code >= 400

6. **System Status (Uptime)** 💚
   - Métrica de disponibilidad del sistema
   - Basado en Heartbeat checks

### Cómo Crear el Dashboard

Consulta la [Guía de Dashboard](docs/DASHBOARD_GUIDE.md) para instrucciones detalladas paso a paso.

---

## 📖 Documentación

Documentación completa disponible en la carpeta `/docs`:

- **[Guía de Setup](docs/SETUP.md)** - Instalación y configuración detallada
- **[Guía de Dashboard](docs/DASHBOARD_GUIDE.md)** - Crear visualizaciones en Kibana
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Solución de problemas comunes

### Estructura de Logs

Los logs se generan automáticamente en formato JSON:

```json
{
  "@timestamp": "2025-01-15T10:30:45.123Z",
  "service.name": "lensy-api",
  "log.level": "INFO",
  "http.request.method": "GET",
  "http.response.status_code": 200,
  "url.path": "/api/professionals",
  "event.duration": 45.23,
  "message": "GET /api/professionals - 200"
}
```

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```
lensy-elk-monitoring/
├── api/                    # Código de la API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── config/                 # Configuraciones ELK
│   ├── filebeat.yml
│   └── heartbeat.yml
├── scripts/                # Scripts de automatización
│   ├── generate_traffic.py
│   └── setup.sh
├── docs/                   # Documentación
└── docker-compose.yml      # Stack completo
```

### Ejecutar en Desarrollo

```bash
# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f lensy-api

# Reconstruir API después de cambios
docker-compose up -d --build lensy-api
```

---

## 🧪 Testing

```bash
# Probar endpoints manualmente
curl http://localhost:5000/api/health
curl http://localhost:5000/api/professionals
curl http://localhost:5000/api/search?profession=Fotografia

# Generar tráfico de prueba
python3 scripts/generate_traffic.py

# Verificar logs en Elasticsearch
curl http://localhost:9200/lensy-api-logs-*/_count?pretty
```

---

## 👥 Equipo

Proyecto desarrollado por el equipo de **Lensy**:

- **Francisco Castillo** - Líder de Negocios (Hustler)
- **Fabián Juárez** - Desarrollador Backend (Hacker)
- **Fernanda Esquivel** - Diseñadora UI/UX (Hipster)
- **Andrés Montoya** - Desarrollador Frontend (Hacker)

---

## 🎓 Contexto Académico

Este proyecto fue desarrollado como parte del curso:

- **Curso**: CC3047 - Administración y Mantenimiento de Sistemas
- **Universidad**: Universidad del Valle de Guatemala
- **Proyecto**: Fase 3 - Sistema de Monitoreo (ELK Stack)
- **Semestre**: II 2025

### Aplicación: Lensy

Lensy es una plataforma SaaS que centraliza la gestión de servicios creativos, conectando profesionales (fotógrafos, diseñadores, videógrafos) con clientes en Guatemala.

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Si deseas contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la [documentación](docs/)
2. Consulta la sección de [Troubleshooting](docs/TROUBLESHOOTING.md)
3. Abre un [Issue](https://github.com/TU_USUARIO/lensy-elk-monitoring/issues)

---

## 🔗 Enlaces Útiles

- [Elastic Stack Documentation](https://www.elastic.co/guide/)
- [Filebeat Reference](https://www.elastic.co/guide/en/beats/filebeat/current/)
- [Heartbeat Reference](https://www.elastic.co/guide/en/beats/heartbeat/current/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## ⭐ Dale una estrella!

Si este proyecto te fue útil, considera darle una estrella ⭐ en GitHub!

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025  
**Estado**: ✅ Completo y funcional
