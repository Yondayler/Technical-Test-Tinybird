import sys
import os
import json

# Agregar el directorio padre al path para importar el validador y el procesador de la Parte 1
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validator import EventValidator
from metrics_calculator import MetricsCalculator

def run_analytics():
    # Dataset extendido para probar métricas
    test_events = [
        # Usuario 1: Ve y Compra (Conversión 1/1)
        {"event_id": "e1", "user_id": "u1", "event_type": "product_view", "product_id": "p1", "timestamp": "2026-05-01T10:00:00Z", "price": 0, "country": "CR"},
        {"event_id": "e2", "user_id": "u1", "event_type": "purchase", "product_id": "p1", "timestamp": "2026-05-01T10:05:00Z", "price": 100.0, "country": "CR"},
        
        # Usuario 2: Ve 2 productos pero no compra
        {"event_id": "e3", "user_id": "u2", "event_type": "product_view", "product_id": "p1", "timestamp": "2026-05-01T10:10:00Z", "price": 0, "country": "CR"},
        {"event_id": "e4", "user_id": "u2", "event_type": "product_view", "product_id": "p2", "timestamp": "2026-05-01T10:15:00Z", "price": 0, "country": "CR"},
        
        # Usuario 3: Compra directamente (sin view previo en este dataset)
        {"event_id": "e5", "user_id": "u3", "event_type": "purchase", "product_id": "p2", "timestamp": "2026-05-01T10:20:00Z", "price": 50.0, "country": "ES"},
        
        # Duplicado (debe ser ignorado por el validador)
        {"event_id": "e2", "user_id": "u1", "event_type": "purchase", "product_id": "p1", "timestamp": "2026-05-01T10:05:00Z", "price": 100.0, "country": "CR"},
        
        # Inválido (debe ser ignorado)
        {"event_id": "e6", "user_id": "u4", "event_type": "purchase", "product_id": "p3", "timestamp": "2026-05-01T10:25:00Z", "price": 0, "country": "MX"}
    ]

 
    
    # 1. Validación (Reutilizando Parte 1)
    validator = EventValidator()
    valid_events_list = []
    
    for e in test_events:
        is_valid, is_duplicate = validator.validate(e)
        if is_valid and not is_duplicate:
            valid_events_list.append(e)

    print(f"Eventos procesados: {len(test_events)}")
    print(f"Eventos válidos para métricas: {len(valid_events_list)}")

    # 2. Cálculo de Métricas
    calculator = MetricsCalculator(valid_events_list)
    metrics = calculator.calculate_all()

    print("\nResultados de métricas:\n")
    print(json.dumps(metrics, indent=4))

    # Verificaciones esperadas:
    # Revenue: 100 + 50 = 150
    # Purchases: 2 (u1 y u3)
    # Unique Users: 3 (u1, u2, u3)
    # Viewers: 2 (u1, u2)
    # Purchasers who viewed: 1 (u1) -> Conv Rate: 1/2 = 0.5
    # Top Products: p1 (3 events), p2 (2 events)

if __name__ == "__main__":
    run_analytics()
