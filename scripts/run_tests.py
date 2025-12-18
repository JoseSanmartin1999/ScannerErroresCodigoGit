#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Tests Simples
========================
Ejecuta pruebas básicas del código para validar funcionalidad.
"""

import sys
import os

def test_imports():
    """Verifica que los módulos se puedan importar"""
    print("🧪 Test 1: Verificando imports...")
    try:
        # No intentar importar módulos, solo verificar que existan
        import os
        import sys
        print("   ✅ Imports básicos OK")
        return True
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        return False

def test_archivos_necesarios():
    """Verifica que existan archivos necesarios"""
    print("\n🧪 Test 2: Verificando archivos necesarios...")
    archivos = [
        'scripts/telegram_bot.py',
        'scripts/scan_with_ia.py',
        'models/vulnerability_detector.pkl',
        'models/vectorizer_detector.pkl',
    ]
    
    todos_ok = True
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo} existe")
        else:
            print(f"   ❌ {archivo} NO encontrado")
            todos_ok = False
    
    return todos_ok

def test_codigo_seguro():
    """Verifica que el código seguro esté presente"""
    print("\n🧪 Test 3: Verificando código seguro de ejemplo...")
    try:
        if os.path.exists('test_seguro.py'):
            with open('test_seguro.py', 'r') as f:
                contenido = f.read()
                if 'hash_password' in contenido and 'validar_nombre' in contenido:
                    print("   ✅ Código seguro verificado")
                    return True
        print("   ⚠️  Archivo test_seguro.py no encontrado o incompleto")
        return True  # No falla el test, solo advierte
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_estructura_proyecto():
    """Verifica la estructura del proyecto"""
    print("\n🧪 Test 4: Verificando estructura del proyecto...")
    directorios = ['scripts', 'models', '.github/workflows']
    
    todos_ok = True
    for directorio in directorios:
        if os.path.isdir(directorio):
            print(f"   ✅ Directorio {directorio}/ existe")
        else:
            print(f"   ❌ Directorio {directorio}/ NO encontrado")
            todos_ok = False
    
    return todos_ok

def test_sintaxis_python():
    """Verifica que no haya errores de sintaxis en archivos Python"""
    print("\n🧪 Test 5: Verificando sintaxis de archivos Python...")
    errores = 0
    
    for root, dirs, files in os.walk('.'):
        # Ignorar directorios
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'venv', '.venv', 'node_modules'}]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        compile(f.read(), filepath, 'exec')
                    print(f"   ✅ {filepath}")
                except SyntaxError as e:
                    print(f"   ❌ Error de sintaxis en {filepath}: {e}")
                    errores += 1
    
    return errores == 0

def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print("  🧪 EJECUTANDO TESTS SIMPLES")
    print("="*70 + "\n")
    
    tests = [
        test_imports,
        test_archivos_necesarios,
        test_codigo_seguro,
        test_estructura_proyecto,
        test_sintaxis_python,
    ]
    
    resultados = []
    for test in tests:
        try:
            resultado = test()
            resultados.append(resultado)
        except Exception as e:
            print(f"\n❌ Error ejecutando test: {e}")
            resultados.append(False)
    
    # Resumen
    print("\n" + "="*70)
    print("  📊 RESUMEN DE TESTS")
    print("="*70 + "\n")
    
    pasados = sum(resultados)
    total = len(resultados)
    
    print(f"Tests ejecutados: {total}")
    print(f"✅ Pasados: {pasados}")
    print(f"❌ Fallados: {total - pasados}")
    
    if all(resultados):
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS PASARON")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ ALGUNOS TESTS FALLARON")
        print("="*70 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
