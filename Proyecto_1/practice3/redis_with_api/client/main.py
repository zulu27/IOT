import requests
import time

API_URL_STUDENTS = "http://api:8000/students/"
API_URL_TEACHERS = "http://api:8000/teachers/"

def create_entity(url, entity_type):
    print(f"\n--- Crear {entity_type} ---")
    name = input("Nombre: ")
    city = input("Ciudad de Origen: ")
    program = input("Programa: ")
    
    data = {
        "name": name,
        "city": city,
        "program": program
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            entity = response.json()
            print(f"Éxito: {entity_type} creado con ID {entity['id']}")
        else:
            print(f"Error al crear {entity_type.lower()}: {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")

def get_entity(url, entity_type):
    print(f"\n--- Consultar {entity_type} por ID ---")
    entity_id = input(f"Ingrese el ID del {entity_type.lower()}: ")
    
    start_time = time.time()
    try:
        response = requests.get(f"{url}{entity_id}")
        end_time = time.time()
        
        if response.status_code == 200:
            entity = response.json()
            print("\nResultados:")
            print(f"  ID: {entity['id']}")
            print(f"  Nombre: {entity['name']}")
            print(f"  Ciudad: {entity['city']}")
            print(f"  Programa: {entity['program']}")
            print(f"  Source: {entity['source']}")
            
            source = entity.get('source', 'unknown')
            print(f"\n  [INFO] Datos obtenidos desde: {source.upper()}")
            print(f"  [INFO] Tiempo de respuesta: {(end_time - start_time) * 1000:.2f} ms")
        elif response.status_code == 404:
            print(f"{entity_type} no encontrado.")
        else:
            print(f"Error en la consulta: {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")

def list_all_entities(url, entity_type):
    print(f"\n--- Listar Todos los {entity_type}s ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            entities = response.json()
            if not entities:
                print(f"No hay {entity_type.lower()}s registrados.")
                return
            
            print(f"Se encontraron {len(entities)} {entity_type.lower()}s:")
            for e in entities:
                print(f"  [{e['id']}] {e['name']} - {e['program']} ({e['city']}) ({e['source']})")
        else:
            print(f"Error al listar: {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")

def show_menu():
    print("\n" + "="*45)
    print("   SISTEMA UNIVERSITARIO (FASTAPI + REDIS)")
    print("="*45)
    print("--- ESTUDIANTES ---")
    print("1. Crear nuevo estudiante")
    print("2. Consultar estudiante por ID")
    print("3. Listar estudiantes")
    print("--- PROFESORES ---")
    print("4. Crear nuevo profesor")
    print("5. Consultar profesor por ID")
    print("6. Listar profesores")
    print("--- OTROS ---")
    print("7. Salir")
    print("="*45)

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Seleccione una opción (1-7): ")

        if choice == '1':
            create_entity(API_URL_STUDENTS, "Estudiante")
        elif choice == '2':
            get_entity(API_URL_STUDENTS, "Estudiante")
        elif choice == '3':
            list_all_entities(API_URL_STUDENTS, "Estudiante")
        elif choice == '4':
            create_entity(API_URL_TEACHERS, "Profesor")
        elif choice == '5':
            get_entity(API_URL_TEACHERS, "Profesor")
        elif choice == '6':
            list_all_entities(API_URL_TEACHERS, "Profesor")
        elif choice == '7':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
