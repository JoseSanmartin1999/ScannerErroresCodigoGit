from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Sistema Seguro v2.0 - Funcionando Correctamente"

# EJEMPLO 1: Cálculo Seguro
# Antes usabas 'eval' (Peligroso). Ahora usamos 'int()' (Seguro).
@app.route('/calcular')
def calcular():
    entrada = request.args.get('numero', '0')
    try:
        # VALIDACIÓN: Forzamos que sea un número. 
        # Si el usuario pone código malicioso, esto dará error y no se ejecutará.
        numero = int(entrada)
        resultado = numero * 10
        return jsonify({"input": numero, "resultado": resultado})
    except ValueError:
        return jsonify({"error": "Entrada inválida. Solo se aceptan números."}), 400

# EJEMPLO 2: Manejo de Texto Seguro
# Antes hacías inyección de comandos. Ahora solo devolvemos texto limpio.
@app.route('/perfil')
def perfil():
    usuario = request.args.get('user', 'Invitado')
    
    # SANITIZACIÓN BÁSICA: Quitamos caracteres que podrían romper el HTML
    usuario_limpio = usuario.replace("<", "").replace(">", "")
    
    return f"Bienvenido al perfil de: {usuario_limpio}"

if __name__ == '__main__':
    # En producción, debug debe ser False
    app.run(host='0.0.0.0', port=5000, debug=False)