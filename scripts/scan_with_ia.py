#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scanner de Vulnerabilidades con IA
===================================
Escanea archivos de código en el repositorio usando modelos ML entrenados.
Retorna exit code 1 si encuentra vulnerabilidades, 0 si está seguro.
"""

import pickle
import sys
import os
from pathlib import Path

def cargar_modelos():
    """Carga los modelos de detección y clasificación"""
    try:
        # Ruta relativa desde scripts/ a models/
        base_dir = Path(__file__).parent.parent
        models_dir = base_dir / "models"
        
        print("🔄 Cargando modelos de IA...")
        
        modelos = {
            'detector': pickle.load(open(models_dir / 'vulnerability_detector.pkl', 'rb')),
            'vectorizer': pickle.load(open(models_dir / 'vectorizer_detector.pkl', 'rb')),
            'cwe_classifier': pickle.load(open(models_dir / 'cwe_classifier.pkl', 'rb')),
            'vectorizer_cwe': pickle.load(open(models_dir / 'vectorizer_cwe_classifier.pkl', 'rb')),
            'cwe_encoder': pickle.load(open(models_dir / 'cwe_encoder.pkl', 'rb')),
        }
        
        print("✅ Modelos cargados correctamente\n")
        return modelos
    except Exception as e:
        print(f"❌ Error cargando modelos: {e}")
        sys.exit(1)

def obtener_archivos_codigo(directorio="."):
    """Encuentra todos los archivos de código en el repositorio"""
    extensiones = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go'}
    archivos = []
    
    for root, dirs, files in os.walk(directorio):
        # Ignorar directorios comunes que no son código fuente
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'models'}]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensiones):
                archivos.append(os.path.join(root, file))
    
    return archivos

def analizar_archivo(filepath, modelos):
    """Analiza un archivo individual con el modelo IA"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            codigo = f.read()
        
        # Si el archivo está vacío o muy pequeño, considerarlo seguro
        if len(codigo.strip()) < 10:
            return {'vulnerable': False, 'file': filepath}
        
        # Paso 1: Detectar vulnerabilidad
        features = modelos['vectorizer'].transform([codigo])
        es_vulnerable = modelos['detector'].predict(features)[0]
        probabilidades = modelos['detector'].predict_proba(features)[0]
        
        resultado = {
            'file': filepath,
            'vulnerable': bool(es_vulnerable),
            'probabilidad_vulnerable': float(probabilidades[1]),
            'probabilidad_seguro': float(probabilidades[0]),
        }
        
        # Paso 2: Si es vulnerable, clasificar el tipo
        if es_vulnerable:
            features_cwe = modelos['vectorizer_cwe'].transform([codigo])
            tipo_idx = modelos['cwe_classifier'].predict(features_cwe)[0]
            tipo_cwe = modelos['cwe_encoder'].inverse_transform([tipo_idx])[0]
            probabilidades_cwe = modelos['cwe_classifier'].predict_proba(features_cwe)[0]
            
            resultado['tipo_vulnerabilidad'] = tipo_cwe
            resultado['confianza_tipo'] = float(probabilidades_cwe[tipo_idx])
        
        return resultado
        
    except Exception as e:
        print(f"⚠️  Error analizando {filepath}: {e}")
        return {'vulnerable': False, 'file': filepath, 'error': str(e)}

def main():
    """Función principal del scanner"""
    print("\n" + "="*70)
    print("  🔍 SCANNER DE VULNERABILIDADES CON IA")
    print("="*70 + "\n")
    
    # Cargar modelos
    modelos = cargar_modelos()
    
    # Obtener archivos a escanear
    archivos = obtener_archivos_codigo()
    print(f"📂 Archivos encontrados: {len(archivos)}\n")
    
    if not archivos:
        print("✅ No se encontraron archivos de código para analizar.")
        sys.exit(0)
    
    # Analizar cada archivo
    vulnerabilidades_encontradas = []
    archivos_seguros = []
    
    for archivo in archivos:
        print(f"Analizando: {archivo}...", end=" ")
        resultado = analizar_archivo(archivo, modelos)
        
        # Si hay error, considerar como seguro pero advertir
        if 'error' in resultado:
            print(f"⚠️  OMITIDO (error)")
            continue
        
        if resultado['vulnerable']:
            print(f"🔴 VULNERABLE ({resultado['probabilidad_vulnerable']:.1%})")
            vulnerabilidades_encontradas.append(resultado)
        else:
            print(f"🟢 SEGURO ({resultado['probabilidad_seguro']:.1%})")
            archivos_seguros.append(resultado)
    
    # Resumen final
    print("\n" + "="*70)
    print("  📊 RESUMEN DEL ESCANEO")
    print("="*70 + "\n")
    
    print(f"Total de archivos analizados: {len(archivos)}")
    print(f"🟢 Seguros: {len(archivos_seguros)}")
    print(f"🔴 Vulnerables: {len(vulnerabilidades_encontradas)}")
    
    # Si hay vulnerabilidades, mostrar detalles
    if vulnerabilidades_encontradas:
        print("\n" + "="*70)
        print("  ⚠️  VULNERABILIDADES DETECTADAS")
        print("="*70 + "\n")
        
        for vuln in vulnerabilidades_encontradas:
            print(f"📄 Archivo: {vuln['file']}")
            print(f"   Tipo: {vuln.get('tipo_vulnerabilidad', 'Desconocido')}")
            print(f"   Confianza: {vuln['probabilidad_vulnerable']:.1%}")
            if 'confianza_tipo' in vuln:
                print(f"   Confianza tipo: {vuln['confianza_tipo']:.1%}")
            print()
        
        print("="*70)
        print("❌ ESCANEO FALLIDO: Se detectaron vulnerabilidades críticas")
        print("="*70 + "\n")
        sys.exit(1)  # Código de error para fallar el pipeline
    else:
        print("\n" + "="*70)
        print("✅ ESCANEO EXITOSO: No se detectaron vulnerabilidades")
        print("="*70 + "\n")
        sys.exit(0)  # Éxito

if __name__ == "__main__":
    main()
