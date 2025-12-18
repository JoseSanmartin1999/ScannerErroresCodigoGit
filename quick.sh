#!/bin/bash
# Comandos rápidos para pruebas del sistema CI/CD

echo "🚀 Comandos Rápidos - Scanner CI/CD"
echo ""

show_help() {
    echo "Uso: ./quick.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup       - Configuración inicial completa"
    echo "  scan        - Ejecutar scanner de vulnerabilidades"
    echo "  test        - Ejecutar tests"
    echo "  deploy      - Simular despliegue"
    echo "  all         - Ejecutar todo (scan + test + deploy)"
    echo "  status      - Ver estado del repositorio"
    echo "  vuln-test   - Crear PR de prueba con código vulnerable"
    echo "  safe-test   - Crear PR de prueba con código seguro"
    echo "  help        - Mostrar esta ayuda"
    echo ""
}

run_setup() {
    echo "⚙️  Ejecutando setup..."
    ./setup.sh
}

run_scan() {
    echo "🔍 Ejecutando scanner..."
    python3 scripts/dummy_scan.py
    echo ""
    echo "Código de salida: $?"
    echo "(0 = seguro, 1 = vulnerable)"
}

run_tests() {
    echo "🧪 Ejecutando tests..."
    python3 scripts/run_tests.py
}

run_deploy() {
    echo "🚀 Ejecutando despliegue..."
    python3 scripts/deploy.py
}

run_all() {
    echo "📋 Ejecutando suite completa..."
    echo ""
    run_scan
    echo ""
    echo "================================"
    echo ""
    run_tests
    echo ""
    echo "================================"
    echo ""
    run_deploy
}

show_status() {
    echo "📊 Estado del Repositorio"
    echo "================================"
    echo ""
    echo "Rama actual:"
    git branch --show-current
    echo ""
    echo "Ramas disponibles:"
    git branch -a
    echo ""
    echo "Estado de archivos:"
    git status -s
    echo ""
    echo "Últimos commits:"
    git log --oneline -5
}

create_vuln_pr() {
    echo "🧪 Creando PR con código VULNERABLE..."
    
    BRANCH="test/vulnerable-$(date +%s)"
    
    git checkout dev
    git checkout -b "$BRANCH"
    
    cat > test_vuln_pr.py << 'EOF'
# Código vulnerable de prueba
import os

print("PELIGRO")

# SQL Injection
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = " + user_id

# Command Injection
filename = input("File: ")
os.system("cat " + filename)

# eval() peligroso
calc = input("Calc: ")
result = eval(calc)
EOF
    
    git add test_vuln_pr.py
    git commit -m "test: código vulnerable para prueba"
    git push -u origin "$BRANCH"
    
    echo ""
    echo "✅ Branch creado: $BRANCH"
    echo ""
    echo "Ahora crea el PR manualmente con:"
    echo "  gh pr create --base dev --head $BRANCH --title 'Test: Vulnerable' --body 'Prueba con código vulnerable'"
    echo ""
    echo "O ve a GitHub y crea el PR desde la interfaz"
}

create_safe_pr() {
    echo "🧪 Creando PR con código SEGURO..."
    
    BRANCH="test/safe-$(date +%s)"
    
    git checkout dev
    git checkout -b "$BRANCH"
    
    cat > test_safe_pr.py << 'EOF'
# Código seguro de prueba

def calcular_area_rectangulo(base, altura):
    """Calcula el área de un rectángulo"""
    if base <= 0 or altura <= 0:
        raise ValueError("Base y altura deben ser positivos")
    return base * altura

def validar_email(email):
    """Valida formato de email"""
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# Uso seguro
if __name__ == "__main__":
    area = calcular_area_rectangulo(5, 3)
    print(f"Área: {area}")
    
    email = "user@example.com"
    if validar_email(email):
        print(f"Email válido: {email}")
EOF
    
    git add test_safe_pr.py
    git commit -m "feat: agregar funciones seguras"
    git push -u origin "$BRANCH"
    
    echo ""
    echo "✅ Branch creado: $BRANCH"
    echo ""
    echo "Ahora crea el PR manualmente con:"
    echo "  gh pr create --base dev --head $BRANCH --title 'Test: Seguro' --body 'Prueba con código seguro'"
    echo ""
    echo "O ve a GitHub y crea el PR desde la interfaz"
}

# Main
case "${1:-help}" in
    setup)
        run_setup
        ;;
    scan)
        run_scan
        ;;
    test)
        run_tests
        ;;
    deploy)
        run_deploy
        ;;
    all)
        run_all
        ;;
    status)
        show_status
        ;;
    vuln-test)
        create_vuln_pr
        ;;
    safe-test)
        create_safe_pr
        ;;
    help|*)
        show_help
        ;;
esac
