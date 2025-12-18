#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Código Seguro - PARA PRUEBAS
=============================
Este archivo contiene código seguro que debería pasar el scanner.
"""

import hashlib
import secrets

# CÓDIGO SEGURO: Uso de prepared statements
def buscar_usuario_seguro(user_id):
    """Código seguro usando parametrización"""
    query = "SELECT * FROM users WHERE id = ?"
    # cursor.execute(query, (user_id,))
    return query

# CÓDIGO SEGURO: Validación de entrada
def validar_nombre(nombre):
    """Validación segura de entrada"""
    if not nombre.isalnum():
        raise ValueError("Nombre inválido")
    return nombre

# CÓDIGO SEGURO: Hash de contraseñas
def hash_password(password):
    """Hash seguro de contraseñas"""
    salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

# CÓDIGO SEGURO: Función matemática simple
def calcular_area_circulo(radio):
    """Cálculo seguro"""
    if radio < 0:
        raise ValueError("Radio debe ser positivo")
    pi = 3.14159
    return pi * radio * radio

# CÓDIGO SEGURO: Logger
def log_mensaje(mensaje):
    """Logging seguro"""
    import logging
    logging.info("Mensaje: %s", mensaje)

if __name__ == "__main__":
    print("✓ Este archivo contiene código seguro")
    print("✓ Debería pasar todas las verificaciones de seguridad")
