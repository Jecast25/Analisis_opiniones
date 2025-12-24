# 🚀 Plataforma Universal de Análisis Inteligente de Opiniones

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Gemini API](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Status](https://img.shields.io/badge/Status-Prototipo%20V5.0-success)

> **Proyecto de Grado - Ingeniería de Ciencia de Datos e Inteligencia Artificial** > **Institución:** SENATI  
> **Autores:** Jean Steven Acosta Cruz, Daniel Adrián López Cerpa  
> **Año:** 2025

## 📋 Descripción del Proyecto

Este repositorio contiene el código fuente de una **Plataforma de Análisis de Sentimientos y Opiniones** basada en Modelos de Lenguaje Grande (LLMs). El sistema utiliza la API de **Google Gemini** para procesar grandes volúmenes de comentarios de clientes, clasificando automáticamente el sentimiento, la categoría del negocio, la intención del usuario y generando una explicación justificada.

El proyecto implementa una arquitectura **Cloud-Native Batch Processing** optimizada para manejar los límites de velocidad (Rate Limits) de la capa gratuita de Google, e introduce un módulo innovador de **Auditoría Cognitiva (LLM-as-a-Judge)** para validar la calidad de las predicciones.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python
* **Frontend/Backend:** Streamlit (Modular)
* **Motor de IA:**
    * *Producción:* Google Gemini 1.5 Flash (Optimizado para velocidad y costo).
    * *Auditoría:* Google Gemini 1.5 Pro (Optimizado para razonamiento complejo).
* **Manipulación de Datos:** Pandas.
* **Visualización:** Plotly Express & Figure Factory.
* **Métricas:** Scikit-learn (Accuracy, Matriz de Confusión).

## ✨ Características Principales

1.  **🏭 Motor de Inferencia por Lotes (Batch Processing):**
    * Procesa archivos CSV masivos.
    * Manejo inteligente de *Rate Limits* (algoritmo de espera dinámica y reintentos).
    * **Monitor de Tiempos en Vivo:** Visualización en tiempo real de la velocidad de procesamiento y latencia por lote.
    * **Resiliencia de Red:** Configuración optimizada para operar en redes corporativas o educativas con restricciones SSL.

2.  **🧪 Módulo de Validación Cruzada:**
    * Permite cargar un *Ground Truth* (datos etiquetados manualmente).
    * Limpieza automática de datos (normalización de strings y eliminación de caracteres sucios).
    * Genera métricas de rendimiento (Accuracy) y Matrices de Confusión interactivas.

3.  **⚖️ Auditoría Cognitiva (Juez IA):**
    * Implementación del patrón *LLM-as-a-Judge*.
    * Un modelo superior (Gemini 1.5 Pro) audita y califica del 1 al 5 las explicaciones generadas por el modelo de producción.
    * Detecta alucinaciones, errores de contexto (sarcasmo, jerga peruana) y falta de coherencia.

## 🚀 Instalación y Uso Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Jecast25/Analisis_opinones.git](https://github.com/Jecast25/Analisis_opiniones.git)
cd Analisis_opiniones
```
### 2. Crear un entorno (Recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate
```
```bash
# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
streamlit run proyecto.py
```
---
## 📊 Estructura de Datos

### 📝 Producción (Análisis)
Para ejecutar el análisis en la pestaña de Producción, tu archivo CSV debe incluir al menos una columna llamada `comentario`. Por ejemplo:

```
id,comentario
1,"El servicio fue excelente, me encantó."
2,"La comida demoró mucho en llegar."
```

### ✅ Validación
Para utilizar la pestaña de Validación, se requiere un archivo CSV con las siguientes columnas: 

- **comentario**: Contiene el texto del comentario.
- **sentimiento_manual**: Contiene la etiqueta de sentimiento asignada manualmente. 

Por ejemplo:

```
comentario,sentimiento_manual
"El producto llegó roto",Negativo
"Es justo lo que pedí",Positivo
```

---

## ⚙️ Configuración

### 🔑 API Key
1. Obtén tu **API Key** gratuita desde **Google AI Studio**.
2. Ingresa la **API Key** en el campo "Añadir API Key" de la barra lateral.

Una vez configurado, sigue estos pasos:
1. **Haz clic en Agregar Nodo.**
2. **¡Listo!** Ahora podrás cargar tus archivos CSV y realizar análisis.

---

## 🤝 Contribución

Este proyecto es desarrollado con fines académicos en el área de **Procesamiento de Lenguaje Natural (NLP)**. ¡Las sugerencias y Pull Requests son siempre bienvenidos!

Si quieres contribuir, sigue estos pasos:
1. Haz un **fork** del repositorio.
2. Crea una nueva rama para tu funcionalidad o mejora (`git checkout -b feature/nueva-funcionalidad`).
3. Asegúrate de probar los cambios antes de enviar un **Pull Request**.
4. Envía tu PR con una descripción detallada.

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **Licencia MIT**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
