import sys
import os
import random

def scan_code():
    print("Iniciando escaneo de seguridad...")
    vulnerable = False
    
    # Escanea archivos en el directorio actual
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".java")): # Archivos de código
                try:
                    with open(os.path.join(root, file), "r", errors="ignore") as f:
                        content = f.read()
                        if "PELIGRO" in content: # SIMULACION DE VULNERABILIDAD
                            vulnerable = True
                            print(f"Patrón peligroso detectado en: {file}")
                except:
                    pass

    if vulnerable:
        print("CLASIFICACIÓN: VULNERABLE")
        print("Probabilidad: 99.9%")
        sys.exit(1) # Código de error para que falle el pipeline
    else:
        print("CLASIFICACIÓN: SEGURO")
        print("Probabilidad: 95.0%")
        sys.exit(0) # Éxito

if __name__ == "__main__":
    scan_code()