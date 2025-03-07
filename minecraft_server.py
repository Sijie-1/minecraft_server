import os
import requests
import subprocess

# Constantes
MOJANG_API = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
IP_API = "https://api.ipify.org?format=json"
SERVER_FOLDER = "minecraft_server"
VERSION = None
SERVER_PROCESS = None

# Función para obtener la URL de descarga del server.jar
def get_download_url(version):
    """Obtiene la URL de descarga del `server.jar` de la versión elegida."""
    response = requests.get(MOJANG_API)
    if response.status_code != 200:
        return None

    data = response.json()
    for v in data["versions"]:
        if v["id"] == version:
            version_data = requests.get(v["url"]).json()
            return version_data["downloads"]["server"]["url"]

    return None

# Función para descargar el server.jar
def download_server(version):
    """Descarga el archivo `server.jar`."""
    url = get_download_url(version)
    if not url:
        print(f"No se encontró el `server.jar` para la versión {version}.")
        return False

    jar_path = os.path.join(SERVER_FOLDER, "server.jar")
    print(f"Descargando {version}...")

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(jar_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Descarga completada.")
        return True
    else:
        print("Error en la descarga.")
        return False

# Función para crear la estructura de carpetas
def create_server_structure():
    """Crea la estructura de carpetas del servidor."""
    os.makedirs(SERVER_FOLDER, exist_ok=True)
    subfolders = ["mods", "world", "datapacks", "config", "logs", "backups"]
    for folder in subfolders:
        os.makedirs(os.path.join(SERVER_FOLDER, folder), exist_ok=True)
    print("Estructura de carpetas creada:")
    for folder in subfolders:
        print(f"  - {folder}")

# Función para configurar la dificultad
def configure_difficulty():
    """Configura la dificultad en `server.properties`."""
    properties_path = os.path.join(SERVER_FOLDER, "server.properties")

    print("\n============================================")
    print(" Selecciona la dificultad")
    print("============================================")
    print("1. Pacífico (peaceful)")
    print("2. Fácil (easy)")
    print("3. Normal (normal)")
    print("4. Difícil (hard)")
    print("5. Regresar a la configuración general")
    print("6. Salir")
    print("============================================")
    choice = input("Selecciona una opción (1-6): ").strip()

    difficulties = {
        "1": "peaceful",
        "2": "easy",
        "3": "normal",
        "4": "hard"
    }

    if choice in difficulties:
        difficulty = difficulties[choice]
        with open(properties_path, "w") as file:
            file.write(f"difficulty={difficulty}\n")
        print(f"Dificultad configurada a {difficulty}.")
    elif choice == "5":
        return
    elif choice == "6":
        print("Saliendo...")
        exit()
    else:
        print("Opción no válida. Se usará 'normal' por defecto.")
        with open(properties_path, "w") as file:
            file.write("difficulty=normal\n")

# Función para obtener la IP pública (IPv4)
def get_public_ip():
    """Obtiene la IP pública del usuario."""
    try:
        response = requests.get(IP_API)
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            return "No se pudo obtener la IP"
    except requests.RequestException:
        return "No se pudo obtener la IP"

# Función para aceptar automáticamente el EULA
def accept_eula():
    """Crea o edita el archivo eula.txt para aceptar los términos de Mojang."""
    eula_path = os.path.join(SERVER_FOLDER, "eula.txt")
    with open(eula_path, "w") as file:
        file.write("eula=true\n")
    print("EULA aceptado automáticamente.")

# Función para iniciar el servidor y mostrar el log
def start_server():
    global SERVER_PROCESS
    if not os.path.exists(os.path.join(SERVER_FOLDER, "server.jar")):
        print("No se ha descargado el servidor. Selecciona una versión primero.")
        return

    # Aceptar el EULA antes de iniciar el servidor
    accept_eula()

    print("Iniciando el servidor de Minecraft...")
    try:
        SERVER_PROCESS = subprocess.Popen(
            ["java", "-Xmx2G", "-Xms2G", "-jar", "server.jar", "nogui"],
            cwd=SERVER_FOLDER,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
        )

        print("\n=== Log del servidor ===")
        while True:
            output = SERVER_PROCESS.stdout.readline()
            if output == "" and SERVER_PROCESS.poll() is not None:
                break
            if output:
                print(output.strip())
        print("=== Fin del log ===")

    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

# Función para detener el servidor
def stop_server():
    global SERVER_PROCESS
    if SERVER_PROCESS:
        print("Deteniendo el servidor...")
        SERVER_PROCESS.terminate()
        SERVER_PROCESS = None
        print("Servidor detenido.")
    else:
        print("No hay un servidor en ejecución.")

# Función para detectar si ya hay una versión instalada
def detect_installed_version():
    """Detecta si ya hay una versión del servidor instalada."""
    jar_path = os.path.join(SERVER_FOLDER, "server.jar")
    if os.path.exists(jar_path):
        # Obtener la versión del servidor (esto es un ejemplo, puede variar)
        try:
            with open(os.path.join(SERVER_FOLDER, "version.txt"), "r") as file:
                version = file.read().strip()
                return version
        except FileNotFoundError:
            return "desconocida"
    return None

# Menú inicial
def show_initial_menu():
    while True:
        print("\n============================================")
        print(" Configuración Inicial del Servidor")
        print("============================================")

        # Detectar si ya hay una versión instalada
        installed_version = detect_installed_version()
        if installed_version:
            print(f"Se ha detectado una versión ya instalada. Versión: {installed_version}.")
            print("1. Ir a la configuración general")
            print("2. Descargar una nueva versión")
            print("3. Salir")
            print("============================================")
            choice = input("Selecciona una opción (1-3): ")

            if choice == "1":
                show_configuration_menu()
            elif choice == "2":
                select_version()
                show_configuration_menu()
            elif choice == "3":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        else:
            print("1. Seleccionar versión de Minecraft")
            print("2. Salir")
            print("============================================")
            choice = input("Selecciona una opción (1-2): ")

            if choice == "1":
                select_version()
                show_configuration_menu()
            elif choice == "2":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

# Menú de configuración general
def show_configuration_menu():
    while True:
        print("\n============================================")
        print(" Configuración General del Servidor")
        print("============================================")
        print("1. Configurar dificultad")
        print("2. Mostrar IP pública")
        print("3. Iniciar servidor")
        print("4. Detener servidor")
        print("5. Regresar a la configuración inicial")
        print("6. Salir")
        print("============================================")
        choice = input("Selecciona una opción (1-6): ")

        if choice == "1":
            configure_difficulty()
        elif choice == "2":
            ip = get_public_ip()
            print("\n============================================")
            print(f"La IP del servidor es: {ip}")
            print("============================================")
        elif choice == "3":
            start_server()
        elif choice == "4":
            stop_server()
        elif choice == "5":
            break
        elif choice == "6":
            print("Saliendo...")
            exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Función para seleccionar la versión
def select_version():
    global VERSION
    print("\n============================================")
    print(" Versión de Minecraft")
    print("============================================")
    print("(Si usted ya tiene un server.jar ya instalado, necesita")
    print("borrar la carpeta minecraft_server para continuar)")
    print("1. Continuar con la descarga")
    print("2. Salir")
    print("============================================")
    choice = input("Selecciona una opción (1-2): ").strip()

    if choice == "1":
        print("Ejemplo: 1.20.1")
        VERSION = input("Ingresa la versión de Minecraft: ").strip()
        print(f"Preparando servidor para la versión {VERSION}...")
        create_server_structure()
        if not download_server(VERSION):
            return

        # Guardar la versión instalada
        with open(os.path.join(SERVER_FOLDER, "version.txt"), "w") as file:
            file.write(VERSION)
    elif choice == "2":
        print("Saliendo...")
        exit()
    else:
        print("Opción no válida. Inténtalo de nuevo.")

# Punto de entrada del script
if __name__ == "__main__":
    show_initial_menu()