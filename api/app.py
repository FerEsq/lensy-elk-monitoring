from flask import Flask, request, jsonify
import logging
import json
import time
from datetime import datetime
import random

app = Flask(__name__)

# Configuración de logging en formato JSON para ELK
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            '@timestamp': datetime.utcnow().isoformat() + 'Z',
            'service.name': 'lensy-api',
            'log.level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name
        }
        
        # Agregar información de request si está disponible
        if hasattr(record, 'http_method'):
            log_data['http.request.method'] = record.http_method
        if hasattr(record, 'http_status'):
            log_data['http.response.status_code'] = record.http_status
        if hasattr(record, 'url_path'):
            log_data['url.path'] = record.url_path
        if hasattr(record, 'duration'):
            log_data['event.duration'] = record.duration
        if hasattr(record, 'user_id'):
            log_data['user.id'] = record.user_id
            
        return json.dumps(log_data)

# Configurar el logger
handler = logging.FileHandler('lensy-api.log')
handler.setFormatter(JSONFormatter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Middleware para logging automático
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = (time.time() - request.start_time) * 1000  # en milisegundos
    
    log_record = app.logger.makeRecord(
        app.logger.name,
        logging.INFO,
        '',
        0,
        f"{request.method} {request.path} - {response.status_code}",
        (),
        None
    )
    
    log_record.http_method = request.method
    log_record.http_status = response.status_code
    log_record.url_path = request.path
    log_record.duration = round(duration, 2)
    
    app.logger.handle(log_record)
    
    return response

# Endpoints de Lensy

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint para Heartbeat"""
    return jsonify({
        'status': 'healthy',
        'service': 'lensy-api',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/professionals', methods=['GET'])
def get_professionals():
    """Obtener lista de profesionales creativos"""
    # Simular datos de profesionales
    professionals = [
        {
            'id': 1,
            'name': 'Alejandra González',
            'profession': 'Fotógrafa',
            'rating': 4.8,
            'projects_completed': 45
        },
        {
            'id': 2,
            'name': 'Carlos Méndez',
            'profession': 'Diseñador Gráfico',
            'rating': 4.6,
            'projects_completed': 32
        }
    ]
    
    return jsonify({'professionals': professionals, 'count': len(professionals)}), 200

@app.route('/api/professionals/<int:professional_id>', methods=['GET'])
def get_professional(professional_id):
    """Obtener detalles de un profesional específico"""
    # Simular caso de profesional no encontrado ocasionalmente
    if random.random() < 0.1:  # 10% de probabilidad de error
        app.logger.error(f"Professional {professional_id} not found")
        return jsonify({'error': 'Professional not found'}), 404
    
    professional = {
        'id': professional_id,
        'name': 'Alejandra González',
        'profession': 'Fotógrafa',
        'rating': 4.8,
        'portfolio': ['photo1.jpg', 'photo2.jpg'],
        'availability': True
    }
    
    return jsonify(professional), 200

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Crear un nuevo proyecto/contratación"""
    data = request.get_json()
    
    # Validación básica
    if not data or 'professional_id' not in data or 'client_id' not in data:
        app.logger.warning("Invalid project creation request - missing required fields")
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Simular creación exitosa
    project = {
        'id': random.randint(1000, 9999),
        'professional_id': data['professional_id'],
        'client_id': data['client_id'],
        'status': 'pending',
        'created_at': datetime.utcnow().isoformat()
    }
    
    log_record = app.logger.makeRecord(
        app.logger.name,
        logging.INFO,
        '',
        0,
        f"New project created: {project['id']}",
        (),
        None
    )
    log_record.user_id = data['client_id']
    app.logger.handle(log_record)
    
    return jsonify(project), 201

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Obtener detalles de un proyecto"""
    project = {
        'id': project_id,
        'professional_id': 1,
        'client_id': 100,
        'status': 'in_progress',
        'deadline': '2025-12-15'
    }
    
    return jsonify(project), 200

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Procesar pago de suscripción"""
    data = request.get_json()
    
    if not data or 'plan' not in data:
        return jsonify({'error': 'Plan is required'}), 400
    
    # Simular algunos errores de pago
    if random.random() < 0.05:  # 5% de probabilidad de error de pago
        app.logger.error("Payment processing failed")
        return jsonify({'error': 'Payment failed'}), 500
    
    payment = {
        'transaction_id': random.randint(10000, 99999),
        'plan': data['plan'],
        'amount': {'Silver': 9.99, 'Gold': 24.99, 'Platinum': 49.99}.get(data['plan'], 0),
        'status': 'completed'
    }
    
    return jsonify(payment), 200

@app.route('/api/login', methods=['POST'])
def login():
    """Autenticación de usuarios"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Simular login exitoso
    token = f"token_{random.randint(1000, 9999)}"
    
    return jsonify({
        'token': token,
        'user_type': 'professional',
        'expires_in': 3600
    }), 200

@app.route('/api/search', methods=['GET'])
def search_professionals():
    """Buscar profesionales por criterios"""
    profession = request.args.get('profession', 'all')
    location = request.args.get('location', 'Guatemala')
    
    # Simular búsqueda
    results = [
        {'id': 1, 'name': 'Professional 1', 'profession': profession},
        {'id': 2, 'name': 'Professional 2', 'profession': profession}
    ]
    
    return jsonify({'results': results, 'count': len(results)}), 200

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.logger.info("Lensy API starting...")
    app.run(host='0.0.0.0', port=5000, debug=False)
