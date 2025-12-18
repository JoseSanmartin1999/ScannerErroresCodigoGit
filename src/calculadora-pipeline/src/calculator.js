const calculator = {
    // FUNCIÓN INSEGURA: Vulnerable a Code Injection
    calculateInsecure: (expression) => {
        try {
            // El uso de eval() es una mala práctica crítica de seguridad
            return eval(expression); 
        } catch (e) {
            return "Error";
        }
    },

    // FUNCIÓN SEGURA: Solo permite operaciones aritméticas básicas
    calculateSecure: (a, b, operation) => {
        const num1 = parseFloat(a);
        const num2 = parseFloat(b);
        
        if (isNaN(num1) || isNaN(num2)) return "Error: Not a number";

        switch (operation) {
            case 'add': return num1 + num2;
            case 'subtract': return num1 - num2;
            case 'multiply': return num1 * num2;
            case 'divide': return num2 !== 0 ? num1 / num2 : "Error: Div by zero";
            default: return "Invalid Operation";
        }
    }
};

module.exports = calculator;