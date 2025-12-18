const calculator = require('../src/calculator');

describe('Pruebas de la Calculadora', () => {
    test('Seguro: Suma 2 + 3 debe ser 5', () => {
        expect(calculator.calculateSecure(2, 3, 'add')).toBe(5);
    });

    test('Inseguro: eval("10 / 2") debe ser 5', () => {
        expect(calculator.calculateInsecure("10 / 2")).toBe(5);
    });

    test('Seguro: División por cero debe retornar error', () => {
        expect(calculator.calculateSecure(10, 0, 'divide')).toBe("Error: Div by zero");
    });
});