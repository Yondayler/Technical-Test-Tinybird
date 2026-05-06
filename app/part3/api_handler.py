import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Agregar directorios necesarios al path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
sys.path.append(os.path.join(base_path, "part2"))

from part2.metrics_calculator import MetricsCalculator

def get_metrics(
    events: List[Dict[str, Any]], 
    country: Optional[str] = None, 
    from_date: Optional[str] = None, 
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Filtra los eventos y calcula métricas según los parámetros proporcionados.
    
    Esta función emula un Endpoint de Tinybird parametrizado:
    SELECT * FROM clean_events WHERE country = {{ country }} ...
    
    :param events: Lista de eventos (diccionarios).
    :param country: Filtro por código de país (ej: 'CR').
    :param from_date: Fecha inicio en formato ISO (YYYY-MM-DDTHH:MM:SSZ).
    :param to_date: Fecha fin en formato ISO (YYYY-MM-DDTHH:MM:SSZ).
    """
    filtered_events = events

    # 1. Filtrado por País
    if country:
        filtered_events = [e for e in filtered_events if e.get("country") == country]

    # 2. Filtrado por Fecha
    try:
        if from_date:
            f_date = datetime.fromisoformat(from_date.replace("Z", "+00:00"))
            filtered_events = [
                e for e in filtered_events 
                if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) >= f_date
            ]
        
        if to_date:
            t_date = datetime.fromisoformat(to_date.replace("Z", "+00:00"))
            filtered_events = [
                e for e in filtered_events 
                if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) <= t_date
            ]
    except (ValueError, KeyError) as e:
        # En una API real, aquí lanzaríamos una excepción HTTP 400
        print(f"Error parseando fechas: {e}")
        return {"error": "Invalid date format"}

    # 3. Cálculo de métricas sobre el set filtrado
    calculator = MetricsCalculator(filtered_events)
    return calculator.calculate_all()
