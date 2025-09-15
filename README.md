# ArgusCrypto

- [Descripción](#descripción)
- [Base de Datos (PostgreSQL + SQLAlchemy)](#base-de-datos-postgresql--sqlalchemy)
  - [`symbols` (Criptomonedas)](#1-symbols-criptomonedas)
  - [`exchanges` (Plataformas de intercambio)](#2-exchanges-plataformas-de-intercambio)
  - [`tickers` (Pares de cotización criptodivisa)](#3-tickers-pares-de-cotización-criptodivisa)
  - [`prices` (Histórico de precios)](#4-prices-histórico-de-precios)
  - [Datos iniciales (por migraciones)](#datos-iniciales-por-migraciones)
- [Servicio de Ingesta de Precios (Celery + RabbitMQ)](#servicio-de-ingesta-de-precios-celery--rabbitmq)
  - [Funcionamiento](#funcionamiento)
  - [Implementar un nuevo exchange](#implementar-un-nuevo-exchange)
- [API (FastAPI)](#api-fastapi)
  - [Documentación interactiva](#documentación-interactiva)
  - [Endpoints disponibles](#endpoints-disponibles)
  - [Esquemas (Pydantic)](#esquemas-pydantic)
- [Dashboard (Streamlit)](#dashboard-streamlit)
  - [Funcionalidad](#funcionalidad)
  - [Componentes principales](#componentes-principales)
- [Ejecución de Servicios](#ejecución-de-servicios)
  - [Servicios y Perfiles](#servicios-y-perfiles)
  - [Comandos útiles](#comandos-útiles)
    - [Manejar aplicación](#manejar-aplicación)
    - [Utilidades](#utilidades)
  - [Variables de entorno](#variables-de-entorno)


## Descripción
Plataforma que obtiene precios de criptomonedas desde uno o varios *exchanges* y los muestra en un dashboard. 

---

Incluye:  
- Modelo de datos en base de datos relacional.  
- Servicio de ingesta periódica de precios desde Binance y Kraken.  
- API para consulta y escritura sobre el modelo de datos.  
- Dashboard para visualización.  

## Base de Datos (PostgreSQL + SQLAlchemy)

El modelo de datos se compone de **4 tablas principales** relacionadas entre sí:

---

### 1. `symbols` (Criptomonedas)
| Campo  | Tipo     | Constraints           | Descripción                            |
|--------|----------|-----------------------|----------------------------------------|
| id     | INT (PK) | NOT NULL, PRIMARY KEY | Identificador único de la criptomoneda |
| name   | VARCHAR  | NOT NULL              | Nombre completo (ej. *Bitcoin*)        |
| symbol | VARCHAR  | NOT NULL, UNIQUE      | Símbolo único (ej. *BTC*, *ETH*)       |


### 2. `exchanges` (Plataformas de intercambio)
| Campo | Tipo     | Constraints           | Descripción                               |
|-------|----------|-----------------------|-------------------------------------------|
| id    | INT (PK) | NOT NULL, PRIMARY KEY | Identificador único del exchange          |
| name  | VARCHAR  | NOT NULL, UNIQUE      | Nombre único del exchange (ej. *Binance*) |


### 3. `tickers` (Pares de cotización cripto/divisa)
| Campo       | Tipo     | Constraints                            | Descripción                                                     |
|-------------|----------|----------------------------------------|-----------------------------------------------------------------|
| id          | INT (PK) | NOT NULL, PRIMARY KEY                  | Identificador único del ticker                                  |
| symbol_id   | INT (FK) | NOT NULL, FOREIGN KEY → `symbols.id`   | Relación con la tabla `symbols`                                 |
| exchange_id | INT (FK) | NOT NULL, FOREIGN KEY → `exchanges.id` | Relación con la tabla `exchanges`                               |
| ticker      | VARCHAR  | NOT NULL                               | Identificador del par en el exchange (ej. *BTCUSDT*, *BTC-USD*) |

**Constraints adicionales**:  
- UNIQUE (`exchange_id`, `ticker`) → evita duplicados del mismo ticker en un exchange.  


### 4. `prices` (Histórico de precios)
| Campo     | Tipo     | Constraints                          | Descripción                                |
|-----------|----------|--------------------------------------|--------------------------------------------|
| id        | INT (PK) | NOT NULL, PRIMARY KEY                | Identificador único del registro de precio |
| ticker_id | INT (FK) | NOT NULL, FOREIGN KEY → `tickers.id` | Relación con la tabla `tickers`            |
| price     | DECIMAL  | NOT NULL                             | Precio registrado del ticker               |
| timestamp | DATETIME | NOT NULL                             | Fecha y hora de la captura de precio       |

**Índices adicionales**:  
- INDEX (`ticker_id`, `timestamp`) → optimización de consultas de precios por rango temporal.  


### Datos iniciales (por migraciones)

Al aplicar las migraciones de Alembic, la base de datos queda poblada con la siguiente información mínima:

- **Tabla `symbols`**
  - `Bitcoin (BTC)`

- **Tabla `exchanges`**
  - `Binance`
  - `Kraken`

- **Tabla `tickers`**
  - Para `Binance`:
    - `BTCUSDT`
    - `BTCEUR`
  - Para `Kraken`:
    - `XBTUSDT`
    - `XXBTZEUR`

De esta manera, aseguramos que siempre haya al menos una criptomoneda (`BTC`) y dos exchanges con varios tickers listos.

## Servicio de Ingesta de Precios (Celery + RabbitMQ)

La aplicación cuenta con un **servicio de ingesta automática de precios**, implementado con **Celery** y **RabbitMQ**.

### Funcionamiento
- **Celery Beat** programa tareas periódicas que se ejecutan en intervalos configurables.
- **Celery Worker** procesa las tareas y se conecta a los distintos exchanges.
- Para cada exchange configurado:
  1. Se obtiene la lista de *tickers* desde la base de datos.
  2. Se consulta la API pública del exchange con los tickers correspondientes.
  3. Los precios resultantes se almacenan en la tabla `prices`.


### Implementar un nuevo exchange

Para añadir un conector de precios de un nuevo exchange se deben hacer estos pasos:

1. Insertar el nuevo exchange en la tabla `exchanges` de base de datos
2. Crear una nueva implementación de `ExchangeClient` orientada a la lectura de tickers del exchange que vamos a integrar
3. Crear una nueva implementación de `ExchangeFinder` destinada a obtener mediante su método `find` únicamente el exchange que vamos a integrar
4. En la factoría de inyección de dependencias `UpdatePricesFromRemoteCommandFactory` implementar un método de creación exclusivo para nuestro exchange que inyecte las clases que hemos desarrollado
5. En `entrypoints` crear un nuevo `TaskHandler` que utilize el método del paso anterior para la creación del comando `UpdatePricesFromRemoteCommand` y tratar los posibles errores que se puedan lanzar con las nuevas dependencias
6. Registrar una task de celery en `tasks.py` usando el `TaskHandler` implementado y actualizar el Celery Beat con esta.

## API (FastAPI)

La API expone endpoints REST y un WebSocket para consultar y gestionar información sobre **symbols**, **exchanges**, **tickers** y **prices**.

---

### Documentación interactiva

> **Nota:** Estos links solo funcionarán si la aplicación está siendo ejecutada en local

- [Swagger UI (OpenAPI)](http://localhost:8000/docs)  
- [Redoc](http://localhost:8000/redoc)  


### Endpoints disponibles

| Método   | Endpoint                              | Descripción                                                                                         | Parámetros principales                                                                                                        | Respuestas relevantes                                                         |
|----------|---------------------------------------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **GET**  | `/v1/symbols`                         | Devuelve la lista de todos los *symbols*.                                                           | —                                                                                                                             | - `200 OK` lista de `SymbolSchema`                                            |
| **GET**  | `/v1/symbols/{symbol_id}`             | Devuelve un *symbol* por su `id`.                                                                   | - `symbol_id` (path, int)                                                                                                     | - `200 OK` <br/> - `404 Symbol not found`                                     |
| **POST** | `/v1/symbols`                         | Crea un nuevo *symbol*.                                                                             | - Body: `SymbolCreateSchema`                                                                                                  | - `201 Created` <br/> - `409 Symbol already exists`                           |
| **GET**  | `/v1/exchanges`                       | Devuelve la lista de todos los *exchanges*.                                                         | —                                                                                                                             | - `200 OK` lista de `ExchangeSchema`                                          |
| **GET**  | `/v1/exchanges/{exchange_id}`         | Devuelve un *exchange* por su `id`.                                                                 | - `exchange_id` (path, int)                                                                                                   | - `200 OK` <br/> - `404 Exchange not found`                                   |
| **GET**  | `/v1/exchanges/{exchange_id}/tickers` | Devuelve todos los *tickers* de un *exchange*.                                                      | - `exchange_id` (path, int)                                                                                                   | - `200 OK` <br/> - `404 Exchange not found`                                   |
| **GET**  | `/v1/tickers/{ticker_id}`             | Devuelve un *ticker* por su `id`.                                                                   | - `ticker_id` (path, int)                                                                                                     | - `200 OK` <br/> - `404 Ticker not found`                                     |
| **POST** | `/v1/tickers`                         | Crea un nuevo *ticker* asociado a un symbol y un exchange.                                          | - Body: `TickerCreateSchema`                                                                                                  | - `201 Created` <br/> - `409 Ticker already exists` <br/> - `400 Bad Request` |
| **GET**  | `/v1/tickers/{ticker_id}/prices`      | Devuelve los precios históricos de un *ticker*, opcionalmente filtrados.                            | - `ticker_id` (path, int) <br/> - `start_date` (query, datetime, opcionales) <br/> - `end_date` (query, datetime, opcionales) | - `200 OK` <br/> - `400 Bad Request` <br/> - `404 Ticker not found`           |
| **WS**   | `/v1/tickers/{ticker_id}/prices/ws`   | WebSocket: stream en tiempo real de precios de un *ticker*. Con histórico por defecto de 10 minutos | - `ticker_id` (path, int) <br/> - `last_minutes` (query, int, opcional, default=10)                                           | (mensajes JSON en tiempo real)                                                |


### Esquemas (Pydantic)

Los objetos intercambiados en la API están definidos con **Pydantic Schemas**:

#### Symbol
- **`SymbolSchema` (response)**
  ```json
  {
    "id": 1,
    "name": "Bitcoin",
    "symbol": "BTC"
  }
  ```
  
- **`SymbolCreateSchema` (request)**
  ```json
  {
    "name": "Bitcoin",
    "symbol": "BTC"
  }
  ```

#### Exchange
- **`ExchangeSchema` (response)**
  ```json
  {
  "id": 1,
  "name": "Binance"
  }
  ```

#### Ticker
- **`TickerSchema` (response)**
  ```json
  {
  "id": 1,
  "symbol_id": 1,
  "exchange_id": 1,
  "ticker": "BTCUSDT"
  }
  ```
  
- **`TickerCreateSchema` (response)**
  ```json
  {
  "symbol_id": 1,
  "exchange_id": 1,
  "ticker": "BTCUSDT"
  }
  ```

#### Price
- **`PriceSchema` (response)**
  ```json
  {
  "id": 100,
  "ticker_id": 1,
  "price": 26000.50,
  "timestamp": "2025-09-15T12:34:56Z"
  }
  ```
  

> **Notas:**
> - Todos los endpoints REST están documentados automáticamente en **Swagger** y **Redoc**.  
> - El endpoint WebSocket (`/v1/tickers/{ticker_id}/prices/ws`) **no se puede probar desde Swagger UI**, debe abrirse con un cliente WS (ej.: navegador, Postman, o librerías JS/Python).  
> - Por defecto, el WebSocket entrega el histórico de los **últimos 10 minutos**, y luego sigue enviando precios en tiempo real.


## Dashboard (Streamlit)

El **dashboard** está desarrollado con **Streamlit** y se ejecuta en la URL local:

 [http://localhost:8501/](http://localhost:8501/)

---

### Funcionalidad

- Selección dinámica de datos mediante un **sidebar**:
  - **Exchange** → lista de exchanges disponibles en el backend.
  - **Symbol** → lista de criptomonedas disponibles.
  - **Ticker** → pares disponibles para la combinación *Exchange + Symbol*.
- Dos modos de visualización:
  - **Static Chart** → muestra precios históricos filtrados por *rango de fechas* (start_date, end_date).
  - **Live Chart** → conecta con el backend vía **WebSocket** y muestra precios en tiempo real (últimos `N` minutos, configurable).


### Componentes principales


- **`sidebar`**  
  Renderiza el panel lateral de configuración:
  - Selección de exchange, symbol y ticker.
  - Activar/desactivar streaming de precios.
  - Configuración de ventana de datos para el gráfico.

- **`static_chart`**  
  - Obtiene precios del backend vía REST.
  - Genera un gráfico de líneas con **Plotly Express**.
  - Permite filtrar por fecha de inicio y fin.

- **`live_chart`**  
  - Conecta con el endpoint WebSocket del backend:  
    ```
    ws://localhost:8000/v1/tickers/{ticker_id}/prices/ws
    ```
  - Recibe datos en tiempo real y los pinta en un gráfico que se actualiza automáticamente.
  - Se limita la ventana de visualización a los últimos `N` minutos (por defecto 10).

> **Notas:**
> - Si no hay datos en la base de datos para el rango de fechas o el ticker seleccionado, se mostrará un mensaje de advertencia.  
> - Debido a la naturaleza del Dashboard, este ha sido testeado como end-to-end, no formando parte de la suite de test unitarios y de integración
 
## Ejecución de Servicios

La aplicación se despliega mediante **Docker Compose**.  
Los servicios se organizan en perfiles (`profiles`) para ejecutar solo lo necesario según el escenario.

### Servicios y Perfiles

| Servicio        | Descripción                       | Perfiles asociados                                                      |
|-----------------|-----------------------------------|-------------------------------------------------------------------------|
| `db`            | Base de datos PostgreSQL          | - `database` <br/> - `backend` <br/> - `app` <br/> - `mq` <br/> - `all` |
| `backend`       | API FastAPI                       | - `backend` <br/> - `app` <br/> - `all`                                 |
| `dashboard`     | Frontend Streamlit                | - `app` <br/> - `all`                                                   |
| `rabbitmq`      | Broker de mensajería (RabbitMQ)   | - `mq` <br/> - `all`                                                    |
| `celery_beat`   | Scheduler de tareas (Celery Beat) | - `mq` <br/> - `all`                                                    |
| `celery_worker` | Workers de procesamiento (Celery) | - `mq` <br/> - `all`                                                    |

### Comandos útiles

#### Manejar aplicación

> **Nota: Se recomienda añadir el flag `--build` a la hora de hacer el primer `docker compose up` de algún servicio**

- Levantar **toda la aplicación:**
  ```bash
  docker compose --profile all up [--build]
  ```
- Bajar **toda la aplicación:**
  ```bash
  docker compose --profile all down
  ```

- Levantar solo la **base de datos:**
  ```bash
    docker compose --profile database up [--build]
  ```
- Bajar solo la **base de datos:**
  ```bash
    docker compose --profile database down
  ```
  
- Levantar solo el **backend + base de datos:**
  ```bash
    docker compose --profile backend up [--build]
  ```
- Bajar solo el **backend + base de datos:**
  ```bash
    docker compose --profile backend down
  ```

- Levantar el **dashboard + backend +base de datos:**
  ```bash
    docker compose --profile app up [--build]
  ```
- Bajar el **dashboard + backend +base de datos:**
  ```bash
    docker compose --profile app down
  ```

- Levantar solo **mensajería y workers + base de datos**:
  ```bash
    docker compose --profile mq up [--build]
  ```
- Bajar solo **mensajería y workers + base de datos**:
  ```bash
    docker compose --profile mq down
  ```

#### Utilidades

- Ver logs de un servicio:
  ```bash
    docker compose logs -f backend
  ```
  
- Ejecutar tests del backend:
  ```bash
     docker compose exec backend python -m unittest discover -s ./app/tests
  ```
  
### Variables de entorno

> **Nota:** Hay un fichero `.env.example` en la raiz del proyecto el cual puede ser convertido a `.env` y estaría listo para utilizar con el `docker-compose.yml`.
> 
> Si se quieren ver qué variables de entorno se usan exclusivamente en `backend` o `dashboard`, se pueden consultar los `.env.example` de cada uno de esos
> ficheros, ya que son puramente informativos.

A pesar de no ser completamente obligatorio, el sistema está pensado para consumir un fichero `.env` para leer las distintas variables de entorno. 
De no existir este fichero, habría que asegurarse que el entorno en el que ejecutamos la aplicación tenga cargadas estas variables de alguna forma.

| Variable                         | Descripción                                                                                                                                              | Ejemplo                 | Backend | Dashboard |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|:-------:|:---------:|
| `POSTGRES_USER`                  | Username de la base de datos PostgreSQL                                                                                                                  | database                |    ✅    |     ❌     |
| `POSTGRES_PASSWORD`              | Contraseña de la base de datos PostgreSQL                                                                                                                | database                |    ✅    |     ❌     |
| `POSTGRES_DB`                    | Nombre de la base de datos PostgreSQL                                                                                                                    | database                |    ✅    |     ❌     |
| `POSTGRES_PORT`                  | Puerto de la base de datos PostgreSQL                                                                                                                    | 5432                    |    ✅    |     ❌     |
| `BACKEND_HOST`                   | Host definido para exponer la API con Uvicorn                                                                                                            | 0.0.0.0                 |    ✅    |     ❌     |
| `BACKEND_PORT`                   | Puerto definido para exponer la API con Uvicorn                                                                                                          | 8000                    |    ✅    |     ❌     |
| `BINANCE_API_BASE_URL`           | URL base de la API de Binance que se consume                                                                                                             | https://api.binance.com |    ✅    |     ❌     |
| `KRAKEN_API_BASE_URL`            | URL base de la API de Kraken que se consume                                                                                                              | https://api.kraken.com  |    ✅    |     ❌     |
| `CELERY_BROKER_USER`             | Username del broker de Celery                                                                                                                            | celery                  |    ✅    |     ❌     |
| `CELERY_BROKER_PASSWORD`         | Contraseña del broker de Celery                                                                                                                          | celery                  |    ✅    |     ❌     |
| `CELERY_BROKER_HOST`             | Host del broker de Celery                                                                                                                                | rabbitmq                |    ✅    |     ❌     |
| `CELERY_BROKER_PORT`             | Puerto del broker de Celery                                                                                                                              | 5672                    |    ✅    |     ❌     |
| `CELERY_BROKER_VHOST`            | VHost del broker de Celery                                                                                                                               | /                       |    ✅    |     ❌     |
| `CELERY_BACKEND_URL`             | URL del backend de Celery                                                                                                                                | rpc://                  |    ✅    |     ❌     |
| `BINANCE_INTERVAL`               | Intervalo en segundos (número decimal) que define la frecuencia con la que se extraen precios de Binance                                                 | 5.0                     |    ✅    |     ❌     |
| `KRAKEN_INTERVAL`                | Intervalo en segundos (número decimal) que define la frecuencia con la que se extraen precios de Kraken                                                  | 10.0                    |    ✅    |     ❌     |
| `PRICE_WEBSOCKET_WRITE_INTERVAL` | Intervalo en segundos (número decimal) que define la frecuencia con la que se consulta por nuevos mensajes del websocket si se habían agotado            | 0.25                    |    ✅    |     ❌     |
| `PRICE_WEBSOCKET_READ_INTERVAL`  | Intervalo en segundos (número decimal) que define la frecuencia con la que se consulta a base de datos por nuevos datos que envíar mediante el websocket | 0.25                    |    ❌    |     ✅     |
| `RABBITMQ_PORT`                  | Puerto de RabbitMQ                                                                                                                                       | 5672                    |    ✅    |     ❌     |
| `RABBITMQ_MANAGEMENT_PORT`       | Puerto de gestión de RabbitMQ                                                                                                                            | 15672                   |    ✅    |     ❌     |
| `DASHBOARD_PORT`                 | Puerto del dashboard                                                                                                                                     | 8501                    |    ❌    |     ✅     |
| `BASE_BACKEND_URL`               | URL base de nuestro propio backend                                                                                                                       | http://backend:8000     |    ❌    |     ✅     |
| `BASE_BACKEND_WEBSOCKET_URL`     | URL base de nuestro websocket                                                                                                                            | ws://backend:8000       |    ❌    |     ✅     |
| `DEFAULT_LAST_MINUTES`           | Número de minutos (por defecto) de histórico que se le solicitan a los datos de precios en vivo                                                          | 10                      |    ❌    |     ✅     |
