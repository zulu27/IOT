# Práctica 3: Caché con Redis, FastAPI y PostgreSQL

En este ejemplo se muestra una arquitectura típica donde **Redis** actúa como una capa de caché de alto rendimiento frente a una base de datos relacional (**PostgreSQL**). El backend está construido en Python usando **FastAPI**.

La idea es simular un escenario donde consultamos la información de un estudiante (como su ciudad de origen y carrera). La primera vez que se consulta, los datos se traen desde PostgreSQL (más lento) y se guardan temporalmente en Redis. Las consultas subsecuentes del mismo estudiante se responderán desde Redis (mucho más rápido), sin tocar la base de datos, hasta que el caché expire (60 segundos en este ejemplo).

## 1. Arquitectura del Proyecto

El archivo `docker-compose.yml` levanta 4 servicios:
- `db`: Contenedor con **PostgreSQL**.
- `redis`: Contenedor con **Redis**.
- `api`: Contenedor con la aplicación **FastAPI**.
- `client`: Contenedor con un script en **Python** para interactuar con la API.

---

## 2. Levantar el Entorno

Para iniciar todos los servicios (Base de Datos, Caché, API y Cliente), ejecuta:

```bash
docker compose up -d --build
```

*(La primera vez puede tardar un poco mientras descarga las imágenes de PostgreSQL, Redis, y construye los contenedores de Python).*

Puedes ver los logs de la API para asegurarte de que levantó correctamente:
```bash
docker compose logs -f api
```
*(Presiona `Ctrl+C` para salir de los logs).*

---

## 3. Probar el Funcionamiento (Contenedor Cliente)

Hemos preparado un contenedor cliente que tiene un script interactivo. Este script hace peticiones HTTP a la API.

1. **Ingresa al contenedor cliente:**
   ```bash
   docker exec -it redis_api_client bash
   ```

2. **Ejecuta el menú interactivo:**
   Dentro del contenedor, escribe:
   ```bash
   python main.py
   ```

3. **Sigue las opciones del menú:**
   * **Opción 1:** Crea un par de estudiantes (ej. "Juan", Ciudad: "Bogotá", Carrera: "Ingeniería").
   * **Opción 2:** Consulta un estudiante por el ID que te arrojó al crearlo. 
     * *La primera vez* que lo consultes, notarás que dice `[INFO] Datos obtenidos desde: DATABASE`.
     * *Si lo vuelves a consultar inmediatamente*, verás que dice `[INFO] Datos obtenidos desde: REDIS_CACHE`. (Notarás que el tiempo de respuesta reportado suele ser menor o la infraestructura no carga la BD).
   * **Opción 3:** Lista todos los estudiantes.
   * **Opción 4:** Salir del script.

4. **Salir del contenedor:**
   Cuando termines de usar el menú, escribe `exit` (o presiona `Ctrl+D`) para volver a la terminal de tu máquina.

---

## 4. Detener y Limpiar

Para apagar los contenedores y eliminar todo (incluyendo los volúmenes de datos creados en los contenedores):

```bash
docker compose down --rmi all -v
```
