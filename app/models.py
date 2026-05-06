from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional, Literal

class Event(BaseModel):
    """
    Modelo de datos para eventos de e-commerce.
    Define el esquema que Tinybird esperaría en una Data Source.
    """
    event_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    event_type: Literal["product_view", "add_to_cart", "purchase"]
    product_id: str
    timestamp: datetime
    price: float = Field(default=0.0)
    country: str

    @model_validator(mode="after")
    def validate_purchase_price(self) -> "Event":
        """
        Regla de negocio: Los eventos de compra deben tener un valor económico.
        Equivale a una validación de transformación en un Pipe de Tinybird.
        """
        if self.event_type == "purchase" and self.price <= 0:
            raise ValueError("Purchase events must have a price greater than 0")
        return self
