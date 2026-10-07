# Guía: Crear un Sitio Web con Balanceador de Carga (ALB)

Esta guía detalla los pasos para crear dos instancias EC2 ejecutando un servidor web y colocar un Balanceador de Carga de Aplicaciones (Application Load Balancer) frente a ellas para distribuir el tráfico.

## 1. Opcional: Probar un balanceador en local con Docker

Antes de ir a AWS, puedes probar cómo funciona un balanceador de forma local:

1. Ejecuta el entorno: `docker compose up -d --build`
2. Abre tu navegador en `http://localhost:5001`.
3. Cuando termines, apaga y limpia el entorno: `docker compose down --rmi all`

---

## 2. Crear un balanceador de carga en AWS

Para configurar nuestro balanceador en la nube, seguiremos un orden específico: crear las reglas de seguridad, lanzar las máquinas virtuales, definir el grupo de destino y finalmente crear el balanceador.

### Paso 1: Crear el Security Group
Antes de las máquinas, necesitamos definir quién puede entrar.

1. Ve a **EC2** > **Security Groups** y haz clic en **Create security group**.
2. **Security group name**: `dummy-web-sg`.
3. **Description**: Grupo de seguridad para web y balanceador.
4. **Inbound rules** (Reglas de entrada):
   - **Type**: HTTP (Puerto 80) -> **Source**: `0.0.0.0/0` (Para que el balanceador reciba tráfico de internet).
   - **Type**: SSH (Puerto 22) -> **Source**: `My IP` o `0.0.0.0/0` (Opcional, si quieres entrar a las máquinas por consola).
5. Haz clic en **Create security group**.

> [!IMPORTANT]
> El puerto 80 debe estar abierto desde cualquier lugar (`0.0.0.0/0`) para que los usuarios puedan ver tu página web.

### Paso 2: Lanzar las Instancias EC2

Vamos a lanzar **dos instancias** idénticas, preferiblemente en diferentes zonas de disponibilidad.

1. Ve a **Instances** > **Launch instances**.
2. **Name**: `Web-Server`. Al lanzar dos a la vez, se llamarán igual.
3. **Number of instances**: Cambia el número a **2** en el panel lateral derecho (Summary).
4. **Application and OS Images**: Selecciona **Ubuntu Server 24.04 LTS**.
5. **Instance type**: Selecciona `t3.micro` o `t2.micro` (dentro de la capa gratuita).
6. **Network settings** (Edit):
   - En **Firewall (security groups)**, elige **Select existing security group** y selecciona el `dummy-web-sg` que acabas de crear.
   - *(Importante para Alta Disponibilidad)*: Al lanzar 2 instancias juntas desde aquí, AWS suele colocarlas en la **misma subred (misma Zona de Disponibilidad)**. Para un entorno real de producción, lo ideal es lanzarlas una por una seleccionando subredes (Zonas) distintas, o bien utilizar un **Auto Scaling Group**. Por ahora, para esta prueba básica, se hara manual.
7. **Advanced details**:
   - Pega el siguiente script en **User data** para que el sitio se instale solo al arrancar:

```bash
#!/bin/bash
# Actualizar los paquetes e instalar el servidor web Apache
apt update -y
apt install -y apache2

# Asegurar que el servicio inicie automáticamente
systemctl start apache2
systemctl enable apache2

# Extraer el nombre del host para identificar qué máquina está respondiendo
INSTANCE_HOSTNAME=$(hostname -f)

# Crear un archivo index.html simple y limpio
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sitio Dummy</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
    <h1>¡Sitio web funcionando perfectamente! 🚀</h1>
    <p>El balanceador de carga te ha enviado a la instancia:</p>
    <h2>$INSTANCE_HOSTNAME</h2>
</body>
</html>
EOF
```

8. Haz clic en **Launch instances**.

### Paso 3: Crear el Target Group (El "Destino")

El balanceador necesita saber a dónde enviar el tráfico (nuestro grupo de servidores).

1. En el panel izquierdo, ve a **Target Groups** (bajo *Load Balancing*) y haz clic en **Create target group**.
2. **Choose a target type**: `Instances`.
3. **Target group name**: `tg-web-dummy`.
4. **Protocol / Port**: HTTP (Puerto 80).
5. **Health checks (Chequeos de Salud - Opcional)**: 
   - AWS configurará por defecto un chequeo usando HTTP hacia la ruta `/`.
   - Si despliegas **Advanced health check settings**, puedes hacer que el balanceador detecte fallas más rápido configurando:
     - *Health check interval*: `10` segundos (en vez de 30).
     - *Healthy threshold*: `2` (necesita 2 aciertos para considerarla sana).
     - *Unhealthy threshold*: `2` (con 2 fallos la sacará del balanceo).
6. Dale a **Next**.
7. **Register targets**: Selecciona tus dos instancias (`Web-Server`) marcando la casilla al lado de ellas.
8. Haz clic en **Include as pending below**.
9. Finalmente, haz clic en **Create target group**.

### Paso 4: Crear el Application Load Balancer (ALB)

1. En el panel izquierdo, ve a **Load Balancers** y haz clic en **Create Load balancer**.
2. En la opción de **Application Load Balancer**, haz clic en **Create**.
3. **Load balancer name**: `alb-dummy-web`.
4. **Network mapping**: 
   - Selecciona tu VPC predeterminada.
   - Selecciona al menos **dos Subnets** marcando las casillas (asegúrate de incluir las zonas donde se crearon tus EC2, por ejemplo, `us-east-1a` y `us-east-1b`).
5. **Security groups**: Selecciona tu `dummy-web-sg` (puedes quitar el `default`).
6. **Listeners and routing**:
   - En Protocol HTTP, Port 80, despliega el menú de **Forward to** / **Default action** y selecciona tu grupo de destino: `tg-web-dummy`.
7. Revisa todo al final y haz clic en **Create load balancer**.

> [!TIP]
> Los balanceadores de carga de aplicaciones (ALB) distribuyen automáticamente el tráfico a nivel de HTTP/HTTPS, asegurando que si una instancia se satura, el tráfico vaya a la otra.

### Paso 5: Probar el Balanceador

1. Ve a la lista de **Load Balancers** y espera a que el estado (State) de tu `alb-dummy-web` cambie a **Active** (puede tardar un par de minutos).
2. Copia el **DNS name** (lo encontrarás en la pestaña de detalles, ej. `alb-dummy-web-1234.us-east-1.elb.amazonaws.com`).
3. Abre una nueva pestaña y pega esa dirección en tu navegador web.
4. Deberías ver el mensaje: **"¡Sitio web funcionando perfectamente!"** junto al nombre de una de las instancias.
5. **¡Prueba la magia!** Recarga la página varias veces (pulsa `F5` o refrescar). Deberías ver cómo el nombre del host (la máquina) cambia, demostrando que el balanceador está alternando el tráfico exitosamente entre tus dos servidores web.