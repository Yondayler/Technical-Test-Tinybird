from processor import process_events
import json

def run_test():
    test_events = [
        # Válido
        {
            "event_id": "evt_001",
            "user_id": "u_123",
            "event_type": "product_view",
            "product_id": "p_10",
            "timestamp": "2026-05-03T10:15:00Z",
            "price": 0,
            "country": "CR"
        },
        # Válido (Purchase con precio > 0)
        {
            "event_id": "evt_002",
            "user_id": "u_123",
            "event_type": "purchase",
            "product_id": "p_11",
            "timestamp": "2026-05-03T10:20:00Z",
            "price": 25.5,
            "country": "CR"
        },
        # Inválido (Purchase con precio 0)
        {
            "event_id": "evt_003",
            "user_id": "u_124",
            "event_type": "purchase",
            "product_id": "p_10",
            "timestamp": "2026-05-03T10:25:00Z",
            "price": 0,
            "country": "ES"
        },
        # Duplicado (Mismo ID que el primero)
        {
            "event_id": "evt_001",
            "user_id": "u_123",
            "event_type": "product_view",
            "product_id": "p_10",
            "timestamp": "2026-05-03T10:15:00Z",
            "price": 0,
            "country": "CR"
        },
        # Inválido (Tipo de evento inexistente)
        {
            "event_id": "evt_004",
            "user_id": "u_125",
            "event_type": "click_ad",
            "product_id": "p_12",
            "timestamp": "2026-05-03T10:30:00Z",
            "price": 0,
            "country": "MX"
        },
        # Inválido (Falta user_id)
        {
            "event_id": "evt_005",
            "event_type": "product_view",
            "product_id": "p_10",
            "timestamp": "2026-05-03T10:35:00Z",
            "price": 0,
            "country": "CR"
        }
    ]

    print("--- Procesando Eventos de Prueba ---")
    results = process_events(test_events)
    print(json.dumps(results, indent=4))
    
    # Verificaciones esperadas:
    # Total: 6
    # Válidos: 2 (evt_001, evt_002)
    # Inválidos: 3 (evt_003, evt_004, evt_005)
    # Duplicados: 1 (evt_001 repetido)

if __name__ == "__main__":
    run_test()
