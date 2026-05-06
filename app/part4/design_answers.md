# Diseño y Arquitectura en Tinybird

A continuación se presentan las respuestas estratégicas sobre cómo implementar y escalar esta solución analítica utilizando la plataforma Tinybird.

## 1. Cómo modelar en Tinybird
Para este caso de e-commerce, el modelado se centraría en una única **Data Source** de eventos (`events_landing`) optimizada para lecturas analíticas.

- **Estructura**: Usaríamos un archivo `.datasource` definiendo los tipos de datos de ClickHouse:
  - `event_id` (String): ID único del evento.
  - `user_id` (String): ID del usuario.
  - `event_type` (Enum8 o String): Categoría del evento.
  - `product_id` (String): Identificador del producto.
  - `timestamp` (DateTime): Fecha y hora del evento.
  - `price` (Float64 o Decimal): Valor monetario.
  - `country` (LowCardinality(String)): Optimizado para filtros frecuentes por país.
- **Sorting Key**: La clave de ordenación sería `(country, event_type, timestamp)`. Esto permite que las consultas filtradas por país o tipo de evento sean extremadamente rápidas al reducir la cantidad de datos escaneados del disco.

## 2. Qué pipes crear
Para transformar los datos crudos en métricas accionables, diseñaría los siguientes pipes:

1.  **`clean_events`**: Un pipe de transformación inicial que aplique las validaciones de la Parte 1 (asegurar que `user_id` no sea nulo y que los precios de compra sean > 0).
2.  **`kpi_analytics`**: Un pipe que realice las agregaciones de la Parte 2. Este pipe tendría varios nodos:
    - `revenue_node`: Calcula sumas y conteos.
    - `users_node`: Calcula usuarios únicos usando la función `uniq()` de ClickHouse (que es muy eficiente).
    - `conversion_node`: Realiza el ratio entre visualizadores y compradores.
3.  **`api_endpoints`**: Pipes dedicados a exponer los resultados a través de HTTP, utilizando parámetros (`{{ String(country) }}`) para implementar los filtros de la Parte 3 de forma nativa en SQL.

## 3. Cómo evitar duplicados
En Tinybird, la deduplicación a escala se maneja mediante el motor de almacenamiento:

- **ReplacingMergeTree**: Configuraría la Data Source para usar este motor con el `event_id` como parte de la clave. Esto permite que ClickHouse limpie los duplicados automáticamente en segundo plano (background merges).
- **Deduplicación en Query**: Para asegurar consistencia total en tiempo real (antes de que ocurra el merge), usaríamos la cláusula `FINAL` en las queries o una ventana de filtrado:
  ```sql
  SELECT * FROM events_landing 
  WHERE event_id IN (SELECT event_id FROM ...)
  QUALIFY ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY timestamp DESC) = 1
  ```

## 4. Cómo escalar
Tinybird está diseñado para manejar miles de millones de filas, pero para optimizar costos y latencia aplicaría estas estrategias:

- **Materialized Views (Vistas Materializadas)**: En lugar de calcular el `total_revenue` sobre millones de filas en cada petición, crearía una vista materializada que pre-agregue los datos por minuto/hora y por país. Así, la API solo lee unos pocos cientos de filas pre-calculadas.
- **TTL (Time To Live)**: Si los datos de eventos individuales pierden valor después de un tiempo, configuraría un TTL para borrarlos automáticamente, manteniendo solo las agregaciones en las vistas materializadas.
- **Copy Pipes**: Para mover datos validados a una fuente de "Producción" más limpia, separando el ruido del tráfico crudo del tráfico de negocio.
