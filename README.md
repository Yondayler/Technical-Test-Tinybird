# Tinybird Technical Assessment - Python Developer

Este repositorio contiene la resolución de la prueba técnica para el rol de Desarrollador Python con enfoque en Tinybird. El proyecto implementa un pipeline de procesamiento de eventos de e-commerce, cálculo de métricas de negocio y una interfaz de consulta tipo API.

##  Estructura del Proyecto

El proyecto está organizado en 4 componentes principales:

- **Parte 1: Procesamiento y Validación**: Ingesta de eventos crudos, validación de esquemas con Pydantic y lógica de deduplicación.
- **Parte 2: Cálculo de Métricas**: Algoritmos para obtener Revenue, Conversion Rate, Unique Users y Top Products.
- **Parte 3: API Handler**: Lógica de filtrado dinámico (país, fechas) sin el uso de frameworks externos, simulando el comportamiento de un endpoint de Tinybird.
- **Parte 4: Diseño y Arquitectura**: Documentación técnica sobre cómo escalar esta solución en producción utilizando Tinybird/ClickHouse.

## 🛠️ Requisitos e Instalación

1. **Python 3.8+**
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Ejecución de Pruebas

Para validar toda la solución de forma automática, se ha incluido un suite de pruebas que ejecuta secuencialmente todas las partes:

```bash
python3 app/test_suite.py
```

### Componentes Individuales
También puedes ejecutar cada parte de forma independiente:
- **Validación**: `python3 app/main.py`
- **Métricas**: `python3 app/part2/metrics_runner.py`
- **API**: `python3 app/part3/api_runner.py`

## 💡 Decisiones Técnicas
- **Pydantic**: Elegido para asegurar la integridad de los datos de forma declarativa.
- **Deduplicación**: Implementada mediante seguimiento de estados en memoria (Set), simulando la lógica de `ReplacingMergeTree` de ClickHouse.
- **Modularidad**: Cada parte es independiente, permitiendo su fácil integración en pipelines de datos reales o funciones serverless.

---
*Desarrollado como parte de la prueba técnica - Mayo 2026*
