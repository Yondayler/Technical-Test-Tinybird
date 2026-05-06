from typing import Set, List, Dict, Any, Tuple
from models import Event
from pydantic import ValidationError

class EventValidator:
    def __init__(self):
        self.seen_ids: Set[str] = set()

    def validate(self, event_data: Dict[str, Any]) -> Tuple[bool, bool]:
        """
        Valida la integridad de un evento y detecta duplicados.
        
        Esta lógica simula el proceso de 'Clean Pipes' en Tinybird antes de 
        la ingesta final, asegurando que solo datos de calidad lleguen a las métricas.
        """
        event_id = event_data.get("event_id")
        
        # Simulación de deduplicación por ID único (como un ReplacingMergeTree)
        is_duplicate = False
        if event_id:
            if event_id in self.seen_ids:
                is_duplicate = True
            else:
                self.seen_ids.add(event_id)
        
        try:
            # Validación de tipos y reglas de negocio con Pydantic
            Event(**event_data)
            is_valid = True
        except (ValidationError, ValueError, TypeError):
            is_valid = False

        return is_valid, is_duplicate
