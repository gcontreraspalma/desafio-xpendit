# Xpendit - Motor de Reglas de Gastos

Este proyecto implementa un motor de reglas para la validación de gastos empresariales. El sistema está diseñado para procesar transacciones, validarlas contra políticas de la empresa, integrar tasas de cambio en tiempo real y analizar lotes de datos históricos para detectar anomalías.

## Arquitectura

El proyecto sigue una **Arquitectura Hexagonal (Puertos y Adaptadores)** para garantizar una clara separación entre la lógica de negocio principal y los componentes de infraestructura (como APIs externas, bases de datos o interfaces de usuario).

La estructura del proyecto es la siguiente:

```
desafio-xpendit/
├── src/
│   ├── domain/         # Entidades y Lógica de Negocio (Lógica Pura)
│   ├── application/    # Puertos (Interfaces)
│   └── infrastructure/ # Adaptadores (API, Pandas, CLI)
├── tests/              # Pruebas unitarias (Pytest)
├── .env                # Configuración de entorno
├── requirements.txt    # Dependencias de Python
└── README.md
```

- **Capa de Dominio (`domain`):** Contiene los modelos de datos (`Pydantic`) y la lógica de validación de gastos (`rules_engine.py`), que es el núcleo de la aplicación.
- **Capa de Aplicación (`application`):** Define los puertos, que son interfaces abstractas (`ExchangeRateService`) que describen cómo la lógica de negocio interactúa con el mundo exterior.
- **Capa de Infraestructura (`infrastructure`):** Implementa los adaptadores para los puertos definidos. Por ejemplo, `OpenExchangeAdapter` se conecta a una API externa para obtener tasas de cambio, y `analyzer.py` actúa como un adaptador para procesar archivos CSV usando Pandas.

## Configuración del Entorno

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### Prerrequisitos

- Python 3.10 o superior

### Pasos

1.  **Clonar el repositorio (opcional):**
    ```bash
    git clone <repository-url>
    cd desafio-xpendit
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Crear el entorno
    python3 -m venv venv

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Asegúrate de que tu entorno virtual esté activado y luego instala los paquetes necesarios.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto copiando el archivo de ejemplo si existiera, o creándolo desde cero. Este archivo es necesario para proporcionar el App ID para el servicio de tasas de cambio.
    ```
    OPEN_EXCHANGE_APP_ID="tu_api_key_aqui"
    ```
    Si no se proporciona una `OPEN_EXCHANGE_APP_ID`, el sistema utilizará un adaptador de mock con tasas de cambio fijas para fines de demostración.

## Uso

### 1. Ejecutar las Pruebas Unitarias

Para verificar que toda la lógica de negocio funciona como se espera, ejecuta las pruebas unitarias con `pytest`.

```bash
# Asegúrate de tener el entorno virtual activado
venv/bin/pytest
```

### 2. Ejecutar el Analizador de Gastos Históricos

El script principal para analizar un archivo de gastos es `analyzer.py`. Se debe ejecutar como un módulo para asegurar que las importaciones funcionen correctamente.

```bash
# Reemplaza 'gastos_historicos.csv' con la ruta a tu archivo
venv/bin/python3 -m src.infrastructure.analyzer gastos_historicos.csv
```

El script generará un resumen en formato JSON con el desglose de estados (`APROBADO`, `PENDIENTE`, `RECHAZADO`), una lista de anomalías detectadas (duplicados, montos negativos) y el resultado detallado de cada gasto.

## Lógica de Negocio: Reglas de Validación

El motor de reglas (`rules_engine.py`) aplica las siguientes validaciones:

1.  **Antigüedad del Gasto:**
    - **0-30 días:** `APROBADO`
    - **31-60 días:** `PENDIENTE`
    - **>60 días:** `RECHAZADO`

2.  **Límites por Categoría (Comida):**
    Los montos se convierten a USD para la validación.
    - **<= 100 USD:** `APROBADO`
    - **101-150 USD:** `PENDIENTE`
    - **> 150 USD:** `RECHAZADO`

3.  **Restricciones por Centro de Costo:**
    - Si el `cost_center` es `"core_engineering"` y la `category` es `"food"`, el estado es `RECHAZADO`.

### Resolución de Estado Final

La jerarquía para determinar el estado final de un gasto es: `RECHAZADO` > `PENDIENTE` > `APROBADO`. Si una sola regla marca un gasto como `RECHAZADO`, ese será su estado final, independientemente de las demás reglas.