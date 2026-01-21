# Análisis de Gastos Históricos

A continuación se presenta el resultado del análisis de `gastos_historicos.csv` ejecutado por el motor de reglas de Xpendit.

## Resumen del Análisis

El motor de reglas ha procesado el lote de datos aplicando las políticas de la empresa y detectando anomalías críticas en la integridad de la información.

- **Total de Gastos Procesados:** 50
- **Desglose por Estado:**
  - **APROBADO:** 0
  - **PENDIENTE:** 0
  - **RECHAZADO:** 50
  *(Nota: El estado de rechazo generalizado se debe a la antigüedad de los registros, todos presentados con más de 60 días de desfase respecto a la fecha actual).*

## Anomalías Detectadas

Se han identificado dos tipos de anomalías principales que requieren atención inmediata por parte del equipo de Finanzas:

### 1. Gastos Duplicados
Se detectaron múltiples casos donde el monto, la moneda y la fecha son idénticos:
- **Casos Destacados:** 
  - `g_001` y `g_011` (50 USD el 2025-10-20).
  - `g_002` y `g_012` (120 USD el 2025-10-19).
  - Grupos de gastos en Marketing y Ventas con montos y fechas correlacionadas (`g_034`, `g_035`, `g_042`, `g_043`, entre otros).

### 2. Montos Negativos
Se identificaron 3 gastos con valores negativos:
- **Gasto `g_031`**: -100 USD
- **Gasto `g_032`**: -90,000 CLP
- **Gasto `g_033`**: -50 USD

## Estrategia de Optimización (Bonus: N+1)

Para garantizar la eficiencia en el procesamiento de lotes, el sistema implementa una solución optimizada para la consulta de tasas de cambio:
1.  **Agrupación:** Los gastos se agrupan por fecha única.
2.  **Llamada Consolidada:** Se realiza una sola petición a la API por cada fecha, evitando el problema de realizar una consulta por cada fila del archivo (N+1).
3.  **Caché:** Los resultados se almacenan temporalmente para su reutilización inmediata durante el procesamiento del mismo lote.

## Resultados Detallados (JSON)

<details>
<summary>Mostrar JSON completo</summary>

```json
{
    "summary": {
        "total_expenses": 50,
        "status_breakdown": {
            "APROBADO": 0,
            "PENDIENTE": 0,
            "RECHAZADO": 50
        },
        "anomalies": {
            "duplicates": [
                {
                    "gasto_id": "g_001",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 50,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_002",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 120,
                    "moneda": "USD",
                    "fecha": "2025-10-19"
                },
                {
                    "gasto_id": "g_011",
                    "empleado_id": "e_001",
                    "empleado_nombre": "Ana",
                    "empleado_apellido": "Reyes",
                    "empleado_cost_center": "core_engineering",
                    "categoria": "food",
                    "monto": 50,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_012",
                    "empleado_id": "e_001",
                    "empleado_nombre": "Ana",
                    "empleado_apellido": "Reyes",
                    "empleado_cost_center": "core_engineering",
                    "categoria": "food",
                    "monto": 120,
                    "moneda": "USD",
                    "fecha": "2025-10-19"
                },
                {
                    "gasto_id": "g_025",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 120,
                    "moneda": "USD",
                    "fecha": "2025-09-15"
                },
                {
                    "gasto_id": "g_027",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 80,
                    "moneda": "USD",
                    "fecha": "2025-08-15"
                },
                {
                    "gasto_id": "g_029",
                    "empleado_id": "e_001",
                    "empleado_nombre": "Ana",
                    "empleado_apellido": "Reyes",
                    "empleado_cost_center": "core_engineering",
                    "categoria": "food",
                    "monto": 120,
                    "moneda": "USD",
                    "fecha": "2025-09-15"
                },
                {
                    "gasto_id": "g_030",
                    "empleado_id": "e_001",
                    "empleado_nombre": "Ana",
                    "empleado_apellido": "Reyes",
                    "empleado_cost_center": "core_engineering",
                    "categoria": "food",
                    "monto": 80,
                    "moneda": "USD",
                    "fecha": "2025-08-15"
                },
                {
                    "gasto_id": "g_034",
                    "empleado_id": "e_003",
                    "empleado_nombre": "Carla",
                    "empleado_apellido": "Mora",
                    "empleado_cost_center": "marketing",
                    "categoria": "transport",
                    "monto": 70,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_035",
                    "empleado_id": "e_003",
                    "empleado_nombre": "Carla",
                    "empleado_apellido": "Mora",
                    "empleado_cost_center": "marketing",
                    "categoria": "transport",
                    "monto": 70,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_036",
                    "empleado_id": "e_003",
                    "empleado_nombre": "Carla",
                    "empleado_apellido": "Mora",
                    "empleado_cost_center": "marketing",
                    "categoria": "lodging",
                    "monto": 70,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_037",
                    "empleado_id": "e_005",
                    "empleado_nombre": "Eva",
                    "empleado_apellido": "Luna",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 150,
                    "moneda": "USD",
                    "fecha": "2025-09-10"
                },
                {
                    "gasto_id": "g_038",
                    "empleado_id": "e_005",
                    "empleado_nombre": "Eva",
                    "empleado_apellido": "Luna",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 150,
                    "moneda": "USD",
                    "fecha": "2025-09-10"
                },
                {
                    "gasto_id": "g_042",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 90,
                    "moneda": "USD",
                    "fecha": "2025-10-21"
                },
                {
                    "gasto_id": "g_043",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 90,
                    "moneda": "USD",
                    "fecha": "2025-10-21"
                },
                {
                    "gasto_id": "g_044",
                    "empleado_id": "e_002",
                    "empleado_nombre": "Bruno",
                    "empleado_apellido": "Soto",
                    "empleado_cost_center": "sales_team",
                    "categoria": "food",
                    "monto": 90,
                    "moneda": "USD",
                    "fecha": "2025-10-21"
                }
            ],
            "negative_amounts": [
                {
                    "gasto_id": "g_031",
                    "empleado_id": "e_004",
                    "empleado_nombre": "David",
                    "empleado_apellido": "Paz",
                    "empleado_cost_center": "finance",
                    "categoria": "software",
                    "monto": -100,
                    "moneda": "USD",
                    "fecha": "2025-10-20"
                },
                {
                    "gasto_id": "g_032",
                    "empleado_id": "e_004",
                    "empleado_nombre": "David",
                    "empleado_apellido": "Paz",
                    "empleado_cost_center": "finance",
                    "categoria": "software",
                    "monto": -90000,
                    "moneda": "CLP",
                    "fecha": "2025-10-19"
                },
                {
                    "gasto_id": "g_033",
                    "empleado_id": "e_001",
                    "empleado_nombre": "Ana",
                    "empleado_apellido": "Reyes",
                    "empleado_cost_center": "core_engineering",
                    "categoria": "food",
                    "monto": -50,
                    "moneda": "USD",
                    "fecha": "2025-10-18"
                }
            ]
        }
    },
    "results": [
        {
            "gasto_id": "g_001",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_002",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_003",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_004",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_005",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_006",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_007",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_008",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_009",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_010",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_011",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_012",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_013",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_014",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_015",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_016",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_017",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_018",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_019",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_020",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_021",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_022",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_023",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_024",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_025",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_026",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_027",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_028",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_029",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_030",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_031",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "NEGATIVE_AMOUNT",
                    "message": "El monto del gasto no puede ser negativo."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_032",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "NEGATIVE_AMOUNT",
                    "message": "El monto del gasto no puede ser negativo."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_033",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "NEGATIVE_AMOUNT",
                    "message": "El monto del gasto no puede ser negativo."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "INVALID_COST_CENTER_EXPENSE",
                    "message": "Gastos de comida no permitidos para este centro de costos."
                }
            ]
        },
        {
            "gasto_id": "g_034",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_035",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_036",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_037",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_038",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                },
                {
                    "code": "FOOD_LIMIT_NEAR_EXCEEDED",
                    "message": "Monto del gasto de comida excede el limite."
                }
            ]
        },
        {
            "gasto_id": "g_039",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_040",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_041",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_042",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_043",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_044",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "DUPLICATE_EXPENSE",
                    "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."
                },
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_045",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_046",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_047",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_048",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_049",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        },
        {
            "gasto_id": "g_050",
            "status": "RECHAZADO",
            "alertas": [
                {
                    "code": "EXPENSE_TOO_OLD",
                    "message": "Gasto presentado fuera de termino."
                }
            ]
        }
    ]
}

```
</details>
