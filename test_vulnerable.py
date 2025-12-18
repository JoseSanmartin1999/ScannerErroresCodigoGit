#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Código con Vulnerabilidades - PARA PRUEBAS
===========================================
Este archivo contiene código intencionalmente vulnerable para probar el scanner.
"""

import os
import pickle

# VULNERABILIDAD 1: SQL Injection
def buscar_usuario_vulnerable(user_id):
    """Código vulnerable a SQL Injection"""
    query = "SELECT * FROM users WHERE id = " + user_id
    # cursor.execute(query)  # Esto sería ejecutado en producción
    return query

# VULNERABILIDAD 2: Command Injection
def ejecutar_comando_vulnerable(filename):
    """Código vulnerable a Command Injection"""
    os.system("cat " + filename)

# VULNERABILIDAD 3: Uso de eval() con entrada del usuario
def calcular_vulnerable(expresion):
    """Código vulnerable a Code Injection"""
    resultado = eval(expresion)
    return resultado

# VULNERABILIDAD 4: Deserialización insegura
def cargar_datos_vulnerable(data):
    """Código vulnerable a deserialización insegura"""
    obj = pickle.loads(data)
    return obj

# VULNERABILIDAD 5: Path Traversal
def leer_archivo_vulnerable(filepath):
    """Código vulnerable a Path Traversal"""
    with open("/var/www/uploads/" + filepath, 'r') as f:
        return f.read()

# VULNERABILIDAD 6: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
SECRET_TOKEN = "my_secret_token_12345"

if __name__ == "__main__":
    print("Este archivo contiene vulnerabilidades intencionalmente para pruebas")
    print("NO usar en producción")
