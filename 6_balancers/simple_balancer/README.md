# Simple HAProxy Load Balancer

Este proyecto demuestra un balanceador de carga simple usando **HAProxy** con dos servidores web backend (basados en Alpine Linux y Apache).

## Arquitectura

- **Load Balancer (HAProxy)**: Expuesto en el puerto `5001`. Recibe las peticiones y las distribuye usando el algoritmo *Round Robin*.
- **Web 1 & Web 2 (Apache)**: Servidores web backend que responden con una página HTML indicando su "hostname" para que puedas identificar qué servidor procesó la petición. Expuestos localmente en los puertos `8081` y `8082`.

## Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Uso

1. **Iniciar los servicios**:
   Construye y levanta los contenedores en segundo plano:
   ```bash
   docker compose up -d --build
   ```

2. **Probar el balanceador de carga**:
   Puedes abrir tu navegador en `http://localhost:5001` o usar `curl` desde la terminal múltiples veces para observar cómo la respuesta alterna entre `web1` y `web2`:
   ```bash
   curl http://localhost:5001
   ```

3. **Detener y limpiar**:
   Para detener los contenedores y eliminar las imágenes creadas, volúmenes y contenedores huérfanos, ejecuta:
   ```bash
   docker compose down --rmi all --volumes --remove-orphans
   ```
