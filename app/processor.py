from typing import List, Dict, Any
from validator import EventValidator

def process_events(events: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Procesa una lista de eventos y retorna un resumen de validación.
    """
    validator = EventValidator()
    
    summary = {
        "total_events": len(events),
        "valid_events": 0,
        "invalid_events": 0,
        "duplicated_events": 0
    }
    
    for event_data in events:
        is_valid, is_duplicate = validator.validate(event_data)
        
        if is_duplicate:
            summary["duplicated_events"] += 1
            # Un evento duplicado no se cuenta como válido o inválido adicional,
            # según la interpretación estándar de "clean pipelines", 
            # pero aquí lo mantendremos simple: si es duplicado, se cuenta en su bolsa.
            continue
            
        if is_valid:
            summary["valid_events"] += 1
        else:
            summary["invalid_events"] += 1
            
    return summary
