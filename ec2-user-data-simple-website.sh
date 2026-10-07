#!/bin/bash
# Script de User Data para Amazon Linux 2 / 2023
# Instalar el servidor web Apache
yum update -y
yum install -y httpd

# Iniciar y habilitar el servicio de Apache
systemctl start httpd
systemctl enable httpd

# Crear una página web sencilla con el nombre del host
echo "<h1>¡Hola Mundo! Este es mi sitio web alojado en EC2.</h1><p>Ejecutándose en: $(hostname -f)</p>" > /var/www/html/index.html
