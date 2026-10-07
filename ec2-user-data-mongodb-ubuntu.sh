#!/bin/bash
# ==============================================================================
# Script: Instalación MongoDB 7.0 + Configuración de Admin
# Sistema: Ubuntu 24.04 (usando rama jammy por compatibilidad)
# ==============================================================================

# 1. Limpieza y preparación
rm -f /etc/apt/sources.list.d/mongodb-org-*.list
apt-get update -y
apt-get install -y gnupg curl

# 2. Importar llave GPG y configurar repositorio (rama jammy)
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg --yes

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 3. Instalación de MongoDB
apt-get update -y
apt-get install -y mongodb-org

# 4. Configuración inicial de red (Bind IP)
sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf

# 5. Iniciar servicio
systemctl daemon-reload
systemctl enable mongod
systemctl start mongod

# 6. Esperar a que MongoDB esté listo para recibir comandos (Loop de salud)
until mongosh --eval "db.adminCommand('ping')" &>/dev/null; do
  echo "Esperando a MongoDB..."
  sleep 2
done

# 7. Crear usuario administrador
mongosh admin --eval "
  db.createUser({
    user: 'admin',
    pwd: 'password123',
    roles: [ { role: 'userAdminAnyDatabase', db: 'admin' }, 'readWriteAnyDatabase' ]
  })
"

# 8. Activar la autenticación en el archivo de configuración
cat <<EOF >> /etc/mongod.conf
security:
  authorization: enabled
EOF

# 9. Reiniciar para aplicar seguridad
systemctl restart mongod

echo "MongoDB instalado y securizado con usuario 'admin' a las $(date)" >> /var/log/mongodb_setup.log