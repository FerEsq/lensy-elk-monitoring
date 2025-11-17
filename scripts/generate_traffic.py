import requests
import time
import random

API_BASE_URL = "http://localhost:5000/api"

def generate_traffic():
    """Genera tráfico simulado hacia la API de Lensy"""
    
    endpoints = [
        ('GET', '/health', None),
        ('GET', '/professionals', None),
        ('GET', '/professionals/1', None),
        ('GET', '/professionals/2', None),
        ('GET', '/professionals/999', None),  # Este dará 404
        ('POST', '/projects', {'professional_id': 1, 'client_id': 100, 'description': 'Sesión fotográfica'}),
        ('GET', '/projects/123', None),
        ('POST', '/checkout', {'plan': 'Silver', 'user_id': 100}),
        ('POST', '/checkout', {'plan': 'Gold', 'user_id': 101}),
        ('POST', '/checkout', {'plan': 'Platinum', 'user_id': 102}),
        ('POST', '/login', {'email': 'user@example.com', 'password': 'password123'}),
        ('GET', '/search?profession=Fotografia&location=Guatemala', None),
        ('GET', '/search?profession=Diseño', None),
    ]
    
    print("Generando tráfico simulado hacia Lensy API...")
    print("Presiona Ctrl+C para detener\n")
    
    request_count = 0
    
    try:
        while True:
            # Seleccionar endpoint aleatorio
            method, endpoint, data = random.choice(endpoints)
            
            url = f"{API_BASE_URL}{endpoint}"
            
            try:
                if method == 'GET':
                    response = requests.get(url, timeout=5)
                elif method == 'POST':
                    response = requests.post(url, json=data, timeout=5)
                
                request_count += 1
                status_icon = "✓" if response.status_code < 400 else "✗"
                print(f"{status_icon} [{request_count}] {method} {endpoint} - Status: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Error en request: {e}")
            
            # Esperar entre requests (simular tráfico realista)
            time.sleep(random.uniform(0.5, 3))
            
    except KeyboardInterrupt:
        print(f"\n\nTráfico generado completado. Total de requests: {request_count}")

if __name__ == "__main__":
    generate_traffic()
