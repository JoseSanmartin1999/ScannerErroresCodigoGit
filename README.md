# Vulnerability Detection System

## 🎯 Objetivo

Sistema de detección de vulnerabilidades en código JavaScript/Node.js utilizando técnicas de minería de datos tradicionales (Machine Learning clásico) siguiendo la metodología SEMMA. El sistema puede analizar código nuevo y clasificarlo como **vulnerable** o **seguro** con alta precisión.

## 📊 Metodología SEMMA

Este proyecto implementa las 5 fases de SEMMA:

1. **Sample (Muestreo)**: Recolección de código vulnerable y seguro de repositorios públicos
2. **Explore (Exploración)**: Análisis exploratorio de datos con visualizaciones
3. **Modify (Modificación)**: Limpieza, feature engineering y normalización
4. **Model (Modelado)**: Entrenamiento de múltiples algoritmos de ML
5. **Assess (Evaluación)**: Evaluación exhaustiva con métricas y comparación

## 🏆 Resultados del Modelo

### Métricas en Test Set (145 muestras)

| Modelo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|--------|----------|-----------|--------|----------|---------|
| **Ensemble** | **95.2%** | **97.1%** | **93.1%** | **0.950** | **0.993** |
| Random Forest | 94.5% | 97.1% | 91.7% | 0.943 | 0.986 |
| XGBoost | 94.5% | 95.7% | 93.1% | 0.944 | 0.994 |
| SVM | 93.1% | 93.1% | 93.1% | 0.931 | 0.988 |
| Decision Tree | 89.7% | 89.0% | 90.3% | 0.897 | 0.908 |

### Dataset

- **Total de muestras**: 966 (balanceadas 50/50)
- **Características extraídas**: 517
  - 17 características estáticas (complejidad, métricas de código)
  - 500 características TF-IDF (análisis de texto)
- **División**: 70% entrenamiento, 15% validación, 15% test

## 🚀 Instalación

### Requisitos Previos

- Python 3.8+
- pip

### Instalación de Dependencias

```bash
# Crear entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso

### 1. Recolección de Datos (SEMMA - Sample)

```bash
python 1_collect_data.py
```

Escanea los repositorios en `dataset_sources/` y crea `data/raw_dataset.csv`.

### 2. Análisis Exploratorio (SEMMA - Explore)

```bash
python 2_explore_data.py
```

Genera visualizaciones y reporte HTML en `reports/eda_report.html`.

### 3. Preprocesamiento (SEMMA - Modify Parte 1)

```bash
python 3_preprocess_data.py
```

Limpia datos, elimina duplicados y balancea clases.

### 4. Ingeniería de Características (SEMMA - Modify Parte 2)

```bash
python 4_feature_engineering.py
```

Extrae características estáticas, TF-IDF y normaliza.

### 5. División de Datos (SEMMA - Modify Parte 3)

```bash
python 5_split_data.py
```

Divide en train/val/test (70/15/15).

### 6. Entrenamiento de Modelos (SEMMA - Model)

```bash
python 6_train_models.py
```

Entrena 5 modelos con hyperparameter tuning:
- Decision Tree (baseline)
- Random Forest
- XGBoost
- SVM
- Ensemble (votación)

**Tiempo estimado**: 20-40 minutos

### 7. Evaluación de Modelos (SEMMA - Assess)

```bash
python 7_evaluate_models.py
```

Evalúa todos los modelos y genera:
- `reports/evaluation_results.png` (visualizaciones)
- `reports/evaluation_report.html` (reporte completo)

### 8. Predicción en Código Nuevo

```bash
# Analizar un archivo
python 8_predict.py --file path/to/code.js

# Analizar código directamente
python 8_predict.py --code "const query = 'SELECT * FROM users WHERE id=' + userId;"

# Usar modelo específico
python 8_predict.py --file code.js --model random_forest
```

**Modelos disponibles**: `decision_tree`, `random_forest`, `xgboost`, `svm`, `ensemble` (default)

## 📁 Estructura del Proyecto

```
MODELO_V2/
├── config.py                    # Configuración y patrones de vulnerabilidades
├── 1_collect_data.py           # Recolección de datos
├── 2_explore_data.py           # Análisis exploratorio
├── 3_preprocess_data.py        # Preprocesamiento
├── 4_feature_engineering.py    # Extracción de características
├── 5_split_data.py             # División de datos
├── 6_train_models.py           # Entrenamiento de modelos
├── 7_evaluate_models.py        # Evaluación de modelos
├── 8_predict.py                # Script de predicción
├── requirements.txt            # Dependencias
├── data/                       # Datasets generados
│   ├── raw_dataset.csv
│   ├── cleaned_dataset.csv
│   ├── features_dataset.csv
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
├── models/                     # Modelos entrenados
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── svm.pkl
│   ├── ensemble.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── reports/                    # Reportes y visualizaciones
│   ├── eda_report.html
│   ├── eda_visualizations.png
│   ├── correlation_heatmap.png
│   ├── evaluation_report.html
│   └── evaluation_results.png
├── test_samples/               # Ejemplos de código para pruebas
│   ├── sqli_vuln.js
│   ├── xss_vuln.js
│   ├── cmd_injection.js
│   ├── safe_query.js
│   └── safe_render.js
└── dataset_sources/            # Repositorios de código fuente
    ├── NodeGoat/
    ├── dvna/
    ├── juice-shop/
    ├── express/
    ├── fastify/
    ├── next.js/
    └── react/
```

## 🔍 Tipos de Vulnerabilidades Detectadas

El sistema puede identificar los siguientes tipos de vulnerabilidades:

1. **SQL Injection**: Concatenación de strings en queries SQL
2. **Command Injection**: Ejecución de comandos con input del usuario
3. **Cross-Site Scripting (XSS)**: HTML sin escapar
4. **Path Traversal**: Acceso a archivos con rutas del usuario
5. **Insecure Deserialization**: Deserialización de datos no confiables
6. **Weak Cryptography**: Uso de MD5, SHA1, Math.random()
7. **Authentication Issues**: Secretos débiles, contraseñas hardcodeadas

## 🎓 Características Extraídas

### Características Estáticas (17)

- Líneas de código
- Longitud del código
- Complejidad ciclomática (promedio y máxima)
- Índice de mantenibilidad
- Número de funciones
- Profundidad de anidamiento
- Conteo de funciones peligrosas (`eval`, `exec`, `child_process`, etc.)
- Scores de patrones de vulnerabilidad (7 tipos)
- Concatenación de strings
- Uso de input del usuario (`req.`, `request.`)

### Características TF-IDF (500)

- Vectorización TF-IDF de tokens de código
- N-gramas (1-3)
- Captura patrones léxicos y sintácticos

## 📊 Ejemplos de Uso

### Ejemplo 1: Detectar SQL Injection

```bash
$ python 8_predict.py --file test_samples/sqli_vuln.js

============================================================
VULNERABILITY DETECTION RESULT
============================================================
File: test_samples/sqli_vuln.js

Prediction: VULNERABLE
Confidence: 70.84%

⚠️  WARNING: This code appears to be VULNERABLE!

Potential Vulnerabilities Detected:
  • SQL Injection
  • Authentication Issues

Code Metrics:
  Dangerous Functions: 0
  Avg Complexity: 1.00
============================================================
```

### Ejemplo 2: Código Seguro

```bash
$ python 8_predict.py --file test_samples/safe_query.js

============================================================
VULNERABILITY DETECTION RESULT
============================================================
File: test_samples/safe_query.js

Prediction: SAFE
Confidence: 85.23%

✓ This code appears to be SAFE

Code Metrics:
  Dangerous Functions: 0
  Avg Complexity: 1.00
============================================================
```

## 🔧 Configuración Avanzada

Edita `config.py` para personalizar:

- Patrones de vulnerabilidades (regex)
- Parámetros de TF-IDF
- Hiperparámetros de modelos
- Tamaño del dataset
- Archivos a excluir

## 📈 Mejoras Futuras

1. **Más lenguajes**: Soporte para Python, Java, C++
2. **Deep Learning**: Modelos basados en transformers (CodeBERT)
3. **Análisis de AST**: Parsing completo del árbol sintáctico
4. **Integración CI/CD**: Plugin para GitHub Actions, GitLab CI
5. **Explicabilidad**: SHAP values para explicar predicciones
6. **Dataset más grande**: Aumentar a 50K+ muestras
7. **Detección de 0-days**: Anomaly detection para vulnerabilidades desconocidas

## 🤝 Contribuciones

Este proyecto fue desarrollado siguiendo la metodología SEMMA para el curso de Seguridad en el Desarrollo de Software.

## 📄 Licencia

MIT License

## 🙏 Agradecimientos

- **Datasets**: NodeGoat, DVNA, OWASP Juice Shop
- **Frameworks**: Express.js, Fastify, Next.js, React
- **Librerías**: scikit-learn, XGBoost, pandas, radon

---

**Desarrollado con ❤️ para mejorar la seguridad del software**
