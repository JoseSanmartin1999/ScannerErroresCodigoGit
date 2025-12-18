#!/usr/bin/env python3
"""
Scanner de Seguridad Simulado (Dummy)
======================================
Versión simplificada que busca patrones peligrosos en el código.
Útil para pruebas cuando el modelo ML no está disponible.
"""

import sys
import os

def scan_code():
    """Escanea archivos buscando patrones peligrosos"""
    print("Iniciando escaneo de seguridad...")
    vulnerable = False
    
    # Patrones peligrosos a detectar
    dangerous_patterns = [
        "PELIGRO",
        "eval(",
        "exec(",
        'os.system(',
        'subprocess.call(',
        'pickle.loads(',
        '" + ',  # Concatenación en queries (SQL injection)
        "' + ",  # Concatenación en queries
    ]
    
    # Escanea archivos en el directorio actual
    for root, dirs, files in os.walk("."):
        # Ignorar directorios
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'models'}]
        
        for file in files:
            if file.endswith((".py", ".js", ".java", ".cpp", ".c")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", errors="ignore") as f:
                        content = f.read()
                        
                        # Buscar patrones peligrosos
                        for pattern in dangerous_patterns:
                            if pattern in content:
                                vulnerable = True
                                print(f"⚠️  Patrón peligroso '{pattern}' detectado en: {filepath}")
                                break
                except Exception as e:
                    pass

    if vulnerable:
        print("\n" + "="*70)
        print("❌ CLASIFICACIÓN: VULNERABLE")
        print("="*70)
        print("Probabilidad: 99.9%")
        print("\nSe detectaron patrones de código potencialmente peligrosos.")
        print("="*70)
        sys.exit(1)  # Código de error para fallar el pipeline
    else:
        print("\n" + "="*70)
        print("✅ CLASIFICACIÓN: SEGURO")
        print("="*70)
        print("Probabilidad: 95.0%")
        print("\nNo se detectaron patrones peligrosos evidentes.")
        print("="*70)
        sys.exit(0)  # Éxito

if __name__ == "__main__":
    scan_code()
