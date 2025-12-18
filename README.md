# 🔐 ScannerErroresCodigoGit

Scanner automático de vulnerabilidades en código con CI/CD integrado.

## 👥 Integrantes
- Chiliquinga Yeshua
- Ferrin Josue
- Sanmartin Jose

## 📋 Descripción

Sistema de detección automática de vulnerabilidades que implementa un pipeline CI/CD de 3 etapas:

```
DEV → TEST → MAIN
 ↓      ↓      ↓
🔍    🧪    🚀
```

### Flujo de Trabajo

1. **DEV (Detección)**: Analiza código con IA para detectar vulnerabilidades
   - ✅ Seguro → Permite merge a TEST
   - ❌ Vulnerable → Bloquea merge y notifica

2. **TEST (Validación)**: Ejecuta pruebas automáticas
   - ✅ Pasa → Permite merge a MAIN
   - ❌ Falla → Bloquea merge

3. **MAIN (Despliegue)**: Despliega a producción
   - 🚀 Despliegue automático
   - 📊 Reportes de estado

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd ScannerErroresCodigoGit

# Instalar dependencias
pip3 install -r requirements.txt

# Crear ramas
git checkout -b dev
git push -u origin dev
git checkout -b test
git push -u origin test
```

### Prueba Local

```bash
# Probar scanner (versión simulada)
python3 scripts/dummy_scan.py

# Probar tests
python3 scripts/run_tests.py

# Probar despliegue
python3 scripts/deploy.py
```

## 📚 Documentación

Ver **[GUIA_PRUEBAS.md](GUIA_PRUEBAS.md)** para instrucciones detalladas.

## 🛠️ Tecnologías

- Python 3.9+
- scikit-learn (ML)
- GitHub Actions (CI/CD)
- Telegram Bot (Notificaciones)

## 📁 Estructura

```
├── .github/workflows/    # Workflows CI/CD
├── scripts/              # Scripts de automatización
├── models/               # Modelos ML entrenados
└── tests/                # Archivos de prueba
```

## ⚙️ Configuración

### Variables de Entorno (Opcional)

- `TELEGRAM_TOKEN`: Token del bot de Telegram
- `TELEGRAM_CHAT_ID`: ID del chat para notificaciones

## 🧪 Tests

Los tests verifican:
- ✅ Existencia de archivos necesarios
- ✅ Estructura del proyecto
- ✅ Sintaxis de código Python
- ✅ Imports correctos

## 🔒 Seguridad

El sistema detecta:
- SQL Injection
- Command Injection
- Code Injection (eval, exec)
- Path Traversal
- Deserialización insegura
- Credenciales hardcodeadas

## 📊 Estado

![CI/CD Status](https://img.shields.io/badge/CI%2FCD-Automated-success)
![Security](https://img.shields.io/badge/Security-Enabled-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-green)

---

**Universidad**: [Tu Universidad]  
**Materia**: Seguridad de Software  
**Fecha**: Diciembre 2024
