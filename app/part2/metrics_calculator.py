from typing import List, Dict, Any, Set
from collections import Counter

class MetricsCalculator:
    def __init__(self, valid_events: List[Dict[str, Any]]):
        self.events = valid_events

    def calculate_all(self) -> Dict[str, Any]:
        """
        Calcula el set completo de KPIs requeridos.
        Estas funciones simulan las queries SQL que se ejecutarían en un Pipe de Tinybird.
        """
        return {
            "total_revenue": self.get_total_revenue(),
            "purchases": self.get_purchases_count(),
            "unique_users": self.get_unique_users_count(),
            "conversion_rate": self.get_conversion_rate(),
            "top_products": self.get_top_products(5)
        }

    def get_total_revenue(self) -> float:
        """Suma de precios para eventos tipo 'purchase'."""
        return sum(event.get("price", 0) for event in self.events if event["event_type"] == "purchase")

    def get_purchases_count(self) -> int:
        """Conteo total de transacciones exitosas."""
        return sum(1 for event in self.events if event["event_type"] == "purchase")

    def get_unique_users_count(self) -> int:
        """Conteo de usuarios distintos (Simulación de la función uniq() de ClickHouse)."""
        return len({event["user_id"] for event in self.events})

    def get_conversion_rate(self) -> float:
        """
        Calcula la tasa de conversión siguiendo la regla: 
        Usuarios que compraron / Usuarios que vieron productos.
        """
        users_who_purchased = {event["user_id"] for event in self.events if event["event_type"] == "purchase"}
        users_who_viewed = {event["user_id"] for event in self.events if event["event_type"] == "product_view"}
        
        if not users_who_viewed:
            return 0.0
            
        return len(users_who_purchased) / len(users_who_viewed)

    def get_top_products(self, n: int = 5) -> List[Dict[str, Any]]:
        """Identifica los productos más frecuentes (Top-N)."""
        product_counts = Counter(event["product_id"] for event in self.events if event.get("product_id"))
        return [{"product_id": pid, "count": count} for pid, count in product_counts.most_common(n)]
