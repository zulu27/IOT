#!/bin/bash
echo "Step 1 - Add PostgreSQL Repository"
echo "First, update the package index and install required packages:"
sudo apt update -y

echo "Add the PostgreSQL 17 repository:"
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

echo "Import the repository signing key:"
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

echo "Update the package list:"
sudo apt update -y

echo "Step 2 - Install PostgreSQL 17"
echo "Install PostgreSQL 17 and contrib modules:"
sudo apt install postgresql-17 -y

echo "Start and enable PostgreSQL service:"
sudo systemctl start postgresql
sudo systemctl enable postgresql

echo "Check the version and ensure it's Postgresql 17:"
psql --version

echo "Step 3 - Configure PostgreSQL 17"
echo "Edit postgresql.conf to allow remote connections by changing listen_addresses to *:"

sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/17/main/postgresql.conf

echo "Configure PostgreSQL to use md5 password authentication by editing pg_hba.conf , this is important if you wish to connect remotely e.g. via PGADMIN :"

sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/17/main/pg_hba.conf
sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/17/main/pg_hba.conf
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/17/main/pg_hba.conf

echo "Restart PostgreSQL for changes to take effect:"
sudo systemctl restart postgresql

echo "Allow PostgreSQL port through the firewall:"
sudo ufw allow 5432/tcp

echo "Step 4 - Connect to PostgreSQL"
echo "Connect as the postgres user:"
echo "Set a password for postgres user:"

sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Password123';"

sudo -u postgres psql -c "CREATE DATABASE d1;"
sudo -u postgres psql -c "CREATE USER guest WITH PASSWORD 'guest';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE d1 TO guest;"

echo "PostgreSQL installation complete."

