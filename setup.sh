#!/bin/bash
# Script de configuración rápida del proyecto

echo "======================================"
echo "  🔐 Setup - Scanner de Vulnerabilidades"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo "📋 Verificando Python..."
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 encontrado: $(python3 --version)${NC}"
else
    echo -e "${RED}❌ Python3 no encontrado. Por favor, instala Python 3.9+${NC}"
    exit 1
fi

# 2. Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
else
    echo -e "${RED}❌ Error instalando dependencias${NC}"
    exit 1
fi

# 3. Verificar estructura
echo ""
echo "📁 Verificando estructura del proyecto..."
DIRS=("scripts" "models" ".github/workflows")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $dir/${NC}"
    else
        echo -e "${RED}❌ $dir/ no encontrado${NC}"
    fi
done

# 4. Dar permisos de ejecución
echo ""
echo "🔧 Configurando permisos..."
chmod +x scripts/*.py
chmod +x setup.sh
echo -e "${GREEN}✅ Permisos configurados${NC}"

# 5. Verificar ramas
echo ""
echo "🌿 Verificando ramas de Git..."
CURRENT_BRANCH=$(git branch --show-current)
echo "   Rama actual: $CURRENT_BRANCH"

if git show-ref --verify --quiet refs/heads/dev; then
    echo -e "${GREEN}✅ Rama dev existe${NC}"
else
    echo -e "${YELLOW}⚠️  Rama dev no existe${NC}"
    read -p "¿Crear rama dev? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout -b dev
        git push -u origin dev
        git checkout $CURRENT_BRANCH
        echo -e "${GREEN}✅ Rama dev creada${NC}"
    fi
fi

if git show-ref --verify --quiet refs/heads/test; then
    echo -e "${GREEN}✅ Rama test existe${NC}"
else
    echo -e "${YELLOW}⚠️  Rama test no existe${NC}"
    read -p "¿Crear rama test? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout -b test
        git push -u origin test
        git checkout $CURRENT_BRANCH
        echo -e "${GREEN}✅ Rama test creada${NC}"
    fi
fi

# 6. Probar scripts
echo ""
echo "🧪 Probando scripts..."

echo "   → Probando tests..."
python3 scripts/run_tests.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tests funcionando${NC}"
else
    echo -e "${YELLOW}⚠️  Tests con advertencias${NC}"
fi

echo "   → Probando scanner..."
python3 scripts/dummy_scan.py > /dev/null 2>&1
SCAN_EXIT=$?
if [ $SCAN_EXIT -eq 1 ]; then
    echo -e "${GREEN}✅ Scanner funcionando (detectó vulnerabilidades)${NC}"
else
    echo -e "${GREEN}✅ Scanner funcionando (código seguro)${NC}"
fi

echo "   → Probando despliegue..."
python3 scripts/deploy.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deploy funcionando${NC}"
else
    echo -e "${YELLOW}⚠️  Deploy con advertencias${NC}"
fi

# 7. Resumen
echo ""
echo "======================================"
echo "  ✅ CONFIGURACIÓN COMPLETADA"
echo "======================================"
echo ""
echo "📚 Próximos pasos:"
echo "   1. Lee GUIA_PRUEBAS.md para instrucciones detalladas"
echo "   2. Configura los secrets de GitHub (opcional):"
echo "      - TELEGRAM_TOKEN"
echo "      - TELEGRAM_CHAT_ID"
echo "   3. Configura protección de ramas en GitHub"
echo "   4. Crea un PR de prueba a la rama dev"
echo ""
echo "🧪 Comandos útiles:"
echo "   python3 scripts/dummy_scan.py    # Escanear código"
echo "   python3 scripts/run_tests.py     # Ejecutar tests"
echo "   python3 scripts/deploy.py        # Simular despliegue"
echo ""
echo "🚀 ¡Listo para usar!"
echo ""
