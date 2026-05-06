import json
from api_handler import get_metrics

def print_human_metrics(metrics):
    if "error" in metrics:
        print(f"Error: {metrics['error']}")
        return

    print(f"Ingresos: ${metrics['total_revenue']}")
    print(f"Compras:  {metrics['purchases']}")
    print(f"Usuarios: {metrics['unique_users']}")
    print(f"Conversión:     {metrics['conversion_rate']*100:.1f}%")
    print("-" * 20)

def print_scenario(title, description, metrics):
    """Muestra un escenario de prueba con formato amigable y técnico."""
    import json
    print(f"\n--- \n {title}")
    print(f"OBJETIVO: {description}\n---")
    print("\n--- RESUMEN EJECUTIVO ---")
    
    if "error" in metrics:
        print(f"   Error: {metrics['error']}")
    else:
        print(f"   Ingresos:   ${metrics['total_revenue']:.2f}")
        print(f"   Compras:    {metrics['purchases']}")
        print(f"   Conversion: {metrics['conversion_rate']*100:.1f}%")
    
    print("\n--- RESPUESTA TÉCNICA (JSON) ---\n")
    print(json.dumps(metrics, indent=2))
    print("\n")

def run_api_tests():
    # Datos de ejemplo
    sample_events = [
        {"event_id": "1", "user_id": "u1", "event_type": "product_view", "product_id": "p1", "timestamp": "2026-05-01T10:00:00Z", "price": 0, "country": "CR"},
        {"event_id": "2", "user_id": "u1", "event_type": "purchase", "product_id": "p1", "timestamp": "2026-05-01T10:05:00Z", "price": 100.0, "country": "CR"},
        {"event_id": "3", "user_id": "u2", "event_type": "product_view", "product_id": "p2", "timestamp": "2026-05-02T10:00:00Z", "price": 0, "country": "ES"},
        {"event_id": "4", "user_id": "u2", "event_type": "purchase", "product_id": "p2", "timestamp": "2026-05-02T10:05:00Z", "price": 50.0, "country": "ES"},
        {"event_id": "5", "user_id": "u3", "event_type": "product_view", "product_id": "p1", "timestamp": "2026-05-03T10:00:00Z", "price": 0, "country": "MX"}
    ]

    print_scenario(
        "DATOS GLOBALES", 
        "Ver el rendimiento total sin aplicar ningún filtro.",
        get_metrics(sample_events)
    )

    print_scenario(
        "SOLO COSTA RICA", 
        "Filtrar eventos para analizar únicamente el mercado de CR.",
        get_metrics(sample_events, country="CR")
    )

    print_scenario(
        "RANGO TEMPORAL (DESDE 2 MAYO)", 
        "Analizar actividad reciente ignorando eventos del 1 de Mayo.",
        get_metrics(sample_events, from_date="2026-05-02T00:00:00Z")
    )

    print_scenario(
        "FILTRO COMBINADO (ESPAÑA + 2 MAYO)", 
        "Búsqueda específica de ventas en España durante un día concreto.",
        get_metrics(sample_events, country="ES", from_date="2026-05-02T00:00:00Z", to_date="2026-05-02T23:59:59Z")
    )

if __name__ == "__main__":
    run_api_tests()
