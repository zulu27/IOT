# Práctica 4: Contenedores con RabbitMQ y Python

En esta práctica, vamos a levantar un entorno que incluye un servidor de mensajería **RabbitMQ** y contenedores con Python configurados para ejecutar ejemplos de envío y recepción de mensajes. Aprenderemos a utilizar colas simples y un sistema de publicación/suscripción (Publish/Subscribe) mediante "exchanges".

## 1. Levantar y Apagar el Entorno (Docker Compose)

El proyecto está configurado para levantar RabbitMQ y los contenedores de Python de manera sencilla.

* **Para iniciar el entorno (RabbitMQ + Contenedores Python):**
  Vamos a levantar el entorno escalando el contenedor de Python para tener 3 instancias. Esto nos permitirá ver cómo funciona la distribución de mensajes a múltiples consumidores.
  ```bash
  docker compose up -d --scale python-client=3
  ```

* **Para detener y borrar los contenedores al terminar:**
  ```bash
  docker compose down --rmi all
  ```

---

## 2. Scripts de Python Incluidos

En la carpeta principal encontrarás varios scripts en Python que demuestran diferentes patrones de mensajería usando la librería `pika`:

### Ejemplo Básico (Cola Simple)
- `send.py`: Envía un único mensaje ("Hello World!") a una cola llamada `hello`.
- `receive.py`: Escucha la cola `hello` y muestra los mensajes recibidos.

### Ejemplo de Publicación/Suscripción (Logs)
- `emit_logs.py`: Envía un mensaje a todos los consumidores conectados a través de un *exchange* de tipo `fanout` llamado `logs`.
- `receive_logs.py`: Crea una cola persistente y se vincula al *exchange* `logs` para recibir todos los mensajes emitidos.

---

## 3. Ejecutar los Ejemplos

Vamos a usar los contenedores de Python que levantamos previamente para ejecutar los scripts. Primero, identifica los nombres o IDs de los contenedores usando `docker ps` (generalmente serán `practice4-python-client-1`, `practice4-python-client-2`, etc.).

### A. Ejemplo de Logs (Publish/Subscribe)

1. **Abrir terminales para los consumidores:**
   Abre un par de terminales diferentes y en cada una ejecuta un consumidor.

   En la **Terminal 1**:
   ```bash
   docker exec -it <CONTAINER_ID_1> python receive_logs.py
   ```

   En la **Terminal 2**:
   ```bash
   docker exec -it <CONTAINER_ID_2> python receive_logs.py
   ```

2. **Emitir un mensaje:**
   Abre una tercera terminal y ejecuta el script que emite los logs usando el tercer contenedor:
   ```bash
   docker exec -it <CONTAINER_ID_3> python emit_logs.py
   ```
   *Deberías ver cómo el mensaje es recibido simultáneamente en las Terminales 1 y 2.*

### B. Ejemplo Básico (Cola Simple)

1. **Iniciar el receptor:**
   En una terminal:
   ```bash
   docker exec -it <CONTAINER_ID_1> python receive.py
   ```

2. **Enviar el mensaje:**
   En otra terminal:
   ```bash
   docker exec -it <CONTAINER_ID_2> python send.py
   ```
   *Verás que el mensaje es recibido por la terminal que ejecuta `receive.py`.*

---

## 4. Acceder al Panel de Gestión de RabbitMQ

RabbitMQ incluye una interfaz gráfica de administración. Puedes acceder a ella abriendo tu navegador en la siguiente dirección:

* **URL:** `http://localhost:15672/`
* **Usuario:** `user`
* **Contraseña:** `password`

Allí podrás monitorear las colas, las conexiones, los "exchanges" y ver en tiempo real cómo viajan los mensajes entre tus contenedores de Python.