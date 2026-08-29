# Práctica 3: Contador en Redis + Web App

## 1. Levantar y Apagar el Entorno (Docker Compose)
Este proyecto levanta una aplicación web, una base de datos Redis y un contenedor de Python para pruebas.

* **Para iniciar el entorno:**
  ```bash
  docker compose up -d --build
  ```

* **Para detener y borrar los contenedores al terminar:**
  ```bash
  docker compose down --rmi all
  ```

---

## 2. Probar la aplicación web
1. Abre tu navegador en [http://localhost:5000](http://localhost:5000).
2. Refresca la página; verás que el contador se incrementa con cada visita.

---

## 3. Entorno de Python para pruebas manuales
Vamos a usar un contenedor de Python para ejecutar pruebas manuales como `set_redis_var.py`. 

### Pasos para configurar y ejecutar el entorno con `uv` (desde cero)

1. **Ingresar al contenedor de Python:**
   ```bash
   docker exec -it python_app bash
   ```

2. **Inicializar el proyecto (crea los archivos de configuración de uv):**
   ```bash
   uv init
   ```
   *(Esto generará los archivos `pyproject.toml` y `.python-version`)*

3. **Crear el ambiente virtual:**
   ```bash
   uv venv
   ```

4. **Activar el ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

5. **Agregar los paquetes necesarios (Redis):**
   ```bash
   uv add redis
   ```

6. **Ejecutar el script en Python:**
   ```bash
   uv run set_redis_var.py
   # O si ya tienes el entorno activado:
   python set_redis_var.py
   ```

7. Vuelve a refrescar la página en el navegador (http://localhost:5000). ¡Verás aparecer la frase (quote) configurada!

8. Para terminar y borrar todo:
   ```bash
   # Salir del contenedor con exit o Ctrl+D, luego en la terminal principal:
   docker compose down --rmi all
   ```

---

## 🛠️ Instalación de Requisitos (`uv` y Python / `venv`) (Opcional, para ejecución local)

### 1. Instalación de `uv`

* **Linux y macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  *O en macOS usando Homebrew:*
  ```bash
  brew install uv
  ```

* **Windows:**
  En PowerShell:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  *O usando winget:*
  ```cmd
  winget install --id astral-sh.uv
  ```

* **En cualquier SO (vía `pip` si ya se cuenta con Python instalado):**
  ```bash
  pip install uv
  ```

---

### 2. Instalación de Python y `venv` (`python3-venv`)

> **Nota importante:** En Windows y macOS, el módulo `venv` viene **incluido por defecto** al instalar Python. En Linux (Debian/Ubuntu) sí requiere instalar un paquete separado.

* **Linux (Ubuntu / Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```

* **macOS:**
  Descargar e instalar desde [python.org](https://www.python.org/) o usando Homebrew:
  ```bash
  brew install python
  ```

* **Windows:**
  Descargar el instalador ejecutable desde [python.org](https://www.python.org/) (marcar la casilla *"Add python.exe to PATH"*) o desde la **Microsoft Store**.

---

### Pasos para configurar y ejecutar con el ambiente virtual tradicional (`venv` + `pip`)

#### 1. Archivo `requirements.txt`
El archivo `requirements.txt` en la carpeta contiene lo siguiente:
```text
redis
```

#### 2. Comandos para crear, activar e instalar:

1. **Crear el ambiente virtual:**
   ```bash
   python3 -m venv .venv
   # En Windows si python3 no está en el alias:
   python -m venv .venv
   ```

2. **Activar el ambiente virtual:**
   * En **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
   * En **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el script:**
   ```bash
   python set_redis_var.py
   ```