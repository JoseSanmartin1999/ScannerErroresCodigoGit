# 🔐 Guía de Pruebas - Scanner de Vulnerabilidades con CI/CD

## 📋 Resumen del Sistema

Este proyecto implementa un **pipeline de CI/CD automatizado** con 3 etapas:

```
DEV (detección) → TEST (validación) → MAIN (despliegue)
```

### Flujo de Trabajo

1. **DEV**: Detecta vulnerabilidades con IA
   - ✅ Si es seguro → Permite merge a TEST
   - ❌ Si es vulnerable → Bloquea merge y crea issue

2. **TEST**: Ejecuta pruebas automáticas
   - ✅ Si pasa tests → Permite merge a MAIN
   - ❌ Si falla → Bloquea merge a MAIN

3. **MAIN**: Despliega a producción
   - 🚀 Despliegue automático
   - 📢 Notificaciones de estado

---

## 🏗️ Estructura del Proyecto

```
ScannerErroresCodigoGit/
├── .github/workflows/
│   ├── dev-security.yml       # Workflow para rama dev
│   ├── test-validation.yml    # Workflow para rama test
│   └── main-deploy.yml        # Workflow para rama main
├── scripts/
│   ├── scan_with_ia.py        # Scanner con modelo IA real
│   ├── dummy_scan.py          # Scanner simulado (para pruebas)
│   ├── run_tests.py           # Tests automáticos
│   ├── deploy.py              # Script de despliegue
│   └── telegram_bot.py        # Notificaciones Telegram
├── models/                     # Modelos ML entrenados
├── test_vulnerable.py         # Código vulnerable (para pruebas)
└── test_seguro.py            # Código seguro (para pruebas)
```

---

## 🚀 Instrucciones de Prueba

### Paso 1: Configurar Secrets en GitHub

Ve a: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**Secrets necesarios:**
- `TELEGRAM_TOKEN`: Token del bot de Telegram (opcional)
- `TELEGRAM_CHAT_ID`: ID del chat de Telegram (opcional)

> ⚠️ Si no configuras Telegram, los workflows funcionarán igual pero sin notificaciones.

---

### Paso 2: Crear las Ramas

```bash
# Asegúrate de estar en main
git checkout main

# Crear rama dev
git checkout -b dev
git push -u origin dev

# Crear rama test
git checkout -b test
git push -u origin test

# Volver a main
git checkout main
```

---

### Paso 3: Configurar Protección de Ramas

#### Para la rama `test`:
1. Ve a: `Settings` → `Branches` → `Add branch protection rule`
2. Branch name pattern: `test`
3. Habilitar:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Agregar check: `security-scan`

#### Para la rama `main`:
1. Branch name pattern: `main`
2. Habilitar:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Agregar check: `run-tests`

---

### Paso 4: Probar el Flujo - Código VULNERABLE

#### 4.1. Crear branch desde dev
```bash
git checkout dev
git checkout -b feature/test-vulnerable
```

#### 4.2. Agregar código vulnerable
```bash
# Editar un archivo existente o crear uno nuevo con vulnerabilidades
echo 'print("PELIGRO")' > test_injection.py
echo 'query = "SELECT * FROM users WHERE id = " + user_id' >> test_injection.py

git add test_injection.py
git commit -m "feat: agregar funcionalidad (con vulnerabilidad)"
git push -u origin feature/test-vulnerable
```

#### 4.3. Crear Pull Request a `dev`
```bash
# Opción 1: Usando GitHub CLI
gh pr create --base dev --head feature/test-vulnerable --title "Test: código vulnerable" --body "Probando detección de vulnerabilidades"

# Opción 2: Desde la interfaz de GitHub
# Ve a: Pull requests → New pull request
```

#### 4.4. Observar el resultado
- ❌ El workflow `dev-security.yml` debería **FALLAR**
- 📝 Debería crear un comentario en el PR
- 🏷️ Debería agregar la etiqueta `security-issue`
- 📋 Debería crear un issue automático
- 🔒 **NO** debería permitir el merge a `test`

---

### Paso 5: Probar el Flujo - Código SEGURO

#### 5.1. Crear branch desde dev
```bash
git checkout dev
git checkout -b feature/test-seguro
```

#### 5.2. Agregar código seguro
```bash
# Usar el archivo seguro que ya existe
cat test_seguro.py

# O crear nuevo código seguro
echo 'def suma(a, b):' > calculadora.py
echo '    """Suma dos números"""' >> calculadora.py
echo '    return a + b' >> calculadora.py

git add calculadora.py
git commit -m "feat: agregar calculadora segura"
git push -u origin feature/test-seguro
```

#### 5.3. Crear Pull Request a `dev`
```bash
gh pr create --base dev --head feature/test-seguro --title "Test: código seguro" --body "Probando código seguro"
```

#### 5.4. Observar el resultado
- ✅ El workflow `dev-security.yml` debería **PASAR**
- 🟢 Debería mostrar "Código SEGURO"
- ✔️ Debería permitir el merge a `test`

#### 5.5. Hacer merge a `test`
```bash
# Opción 1: Auto-merge (si está configurado)
gh pr merge --merge --auto

# Opción 2: Merge manual
gh pr merge --merge
```

---

### Paso 6: Probar Rama TEST

#### 6.1. Una vez en `test`, el workflow automáticamente:
- 🧪 Ejecuta `run_tests.py`
- ✅ Si pasa → Permite merge a `main`
- ❌ Si falla → Bloquea merge

#### 6.2. Crear PR de `test` a `main`
```bash
git checkout test
gh pr create --base main --head test --title "Release: deploy to production" --body "Cambios listos para producción"
```

---

### Paso 7: Probar Rama MAIN (Despliegue)

#### 7.1. Una vez mergeado a `main`:
- 🚀 Se ejecuta `deploy.py`
- 📦 Simula despliegue a producción
- 📊 Genera reporte de despliegue

---

## 🧪 Pruebas Locales

### Probar el Scanner de IA localmente:
```bash
# Instalar dependencias
pip3 install scikit-learn numpy requests

# Ejecutar scanner
python3 scripts/scan_with_ia.py
```

### Probar el Scanner Dummy (simulado):
```bash
# Este busca la palabra "PELIGRO" en el código
python3 scripts/dummy_scan.py
```

### Probar los Tests:
```bash
python3 scripts/run_tests.py
```

### Probar el Despliegue:
```bash
python3 scripts/deploy.py
```

---

## 📊 Verificar Estado de los Workflows

### Ver workflows en GitHub:
```bash
# Listar últimas ejecuciones
gh run list

# Ver detalles de un workflow
gh run view [RUN_ID]

# Ver logs
gh run view [RUN_ID] --log
```

### Ver estado de PRs:
```bash
# Listar PRs
gh pr list

# Ver detalles de un PR
gh pr view [PR_NUMBER]

# Ver checks de un PR
gh pr checks [PR_NUMBER]
```

---

## 🔧 Solución de Problemas

### El modelo IA no funciona:
- **Problema**: Error "X has 1000 features, but expecting 1001"
- **Solución**: Usar `dummy_scan.py` en lugar de `scan_with_ia.py` en los workflows
- **Editar**: `.github/workflows/dev-security.yml`
  ```yaml
  # Cambiar esta línea:
  run: python scripts/scan_with_ia.py
  # Por:
  run: python scripts/dummy_scan.py
  ```

### Auto-merge no funciona:
- Verificar que la protección de ramas esté configurada correctamente
- Verificar que el workflow tenga permisos: `contents: write`
- Puede requerir aprobación manual dependiendo de la configuración

### Telegram no envía notificaciones:
- Verificar que los secrets estén configurados
- El bot debe estar agregado al chat
- Los workflows continuarán funcionando sin Telegram

---

## 📝 Notas Importantes

1. **Modelo IA**: Por incompatibilidad de versiones, se recomienda usar `dummy_scan.py` para pruebas
2. **Telegram**: Es opcional, los workflows funcionan sin él
3. **Protección de ramas**: Necesaria para que el flujo funcione correctamente
4. **Auto-merge**: Puede requerir configuración adicional según tu repo

---

## 🎯 Checklist de Validación

- [ ] Las 3 ramas están creadas (dev, test, main)
- [ ] Los workflows están en `.github/workflows/`
- [ ] Los scripts tienen permisos de ejecución
- [ ] La protección de ramas está configurada
- [ ] Se probó con código vulnerable (debe fallar)
- [ ] Se probó con código seguro (debe pasar)
- [ ] Los tests en `test` ejecutan correctamente
- [ ] El despliegue en `main` funciona
- [ ] Las notificaciones funcionan (opcional)

---

## 🎉 Resultado Esperado

**Flujo exitoso:**
1. ✅ Código seguro en DEV → Pasa scanner → Merge a TEST
2. ✅ Tests en TEST → Pasan → Merge a MAIN
3. ✅ Despliegue en MAIN → Exitoso → Producción

**Flujo bloqueado:**
1. ❌ Código vulnerable en DEV → Falla scanner → NO merge
2. ❌ Tests fallan en TEST → NO merge a MAIN
3. 🔒 Nunca llega a producción

---

## 📞 Contacto

- Chiliquinga Yeshua
- Ferrin Josue
- Sanmartin Jose

¡Listo para probar! 🚀
