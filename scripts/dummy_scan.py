import sys
import os

def scan_code():
    print("Iniciando escaneo de seguridad...")
    vulnerable = False
    
    # Recorremos todas las carpetas y archivos
    for root, dirs, files in os.walk("."):
        
        # 1. Ignorar carpeta oculta de git y la carpeta de scripts
        if ".git" in root or "scripts" in root:
            continue

        for file in files:
            # 2. IMPORTANTE: Ignorar este mismo archivo para no detectarse a sí mismo
            if file == "dummy_scan.py":
                continue

            # Analizar solo archivos de código
            if file.endswith((".py", ".js", ".java", ".ts")):
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        # Buscamos la palabra clave
                        if "PELIGRO" in content:
                            vulnerable = True
                            print(f"Patrón peligroso detectado en: {file}")
                except Exception as e:
                    print(f"No se pudo leer {file}: {e}")

    if vulnerable:
        print("CLASIFICACIÓN: VULNERABLE")
        print("Probabilidad: 99.9%")
        sys.exit(1) # Falla el pipeline
    else:
        print("CLASIFICACIÓN: SEGURO")
        print("Probabilidad: 0.0%")
        sys.exit(0) # Pasa el pipeline

if __name__ == "__main__":
    scan_code()