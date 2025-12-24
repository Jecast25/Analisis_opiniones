# Análisis de Opiniones

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5-brightgreen.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Sistema inteligente de análisis de opiniones para la mejora continua utilizando los modelos avanzados de Google Gemini 2.5 Flash y 2.5 Pro.

## 📋 Descripción

**Análisis de Opiniones** es una herramienta diseñada para procesar y analizar opiniones de usuarios, comentarios, reseñas y feedback de manera automatizada. El sistema utiliza modelos de inteligencia artificial de última generación (Gemini 2.5 Flash y 2.5 Pro) para extraer información valiosa, identificar sentimientos, detectar tendencias y proporcionar insights accionables para la mejora continua de productos y servicios.

## ✨ Características Principales

- **Análisis de Sentimientos**: Clasifica opiniones en positivas, negativas o neutrales con alta precisión
- **Extracción de Temas**: Identifica automáticamente los temas principales mencionados en las opiniones
- **Detección de Tendencias**: Analiza patrones y tendencias a lo largo del tiempo
- **Procesamiento por Lotes**: Capacidad para analizar grandes volúmenes de opiniones simultáneamente
- **Modelos Gemini Duales**: 
  - **Gemini 2.5 Flash**: Para análisis rápidos y respuestas en tiempo real
  - **Gemini 2.5 Pro**: Para análisis profundos y complejos
- **Reportes Detallados**: Genera informes comprensibles con visualizaciones y métricas clave
- **API REST**: Interfaz de programación para integración con otros sistemas
- **Soporte Multiidioma**: Análisis de opiniones en múltiples idiomas

## 🚀 Casos de Uso

- Análisis de reseñas de productos en e-commerce
- Evaluación de comentarios en redes sociales
- Procesamiento de encuestas de satisfacción del cliente
- Monitoreo de feedback en aplicaciones móviles
- Análisis de opiniones en foros y comunidades online
- Evaluación de comentarios en sitios de reseñas

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **Google Gemini 2.5 Flash**: Modelo de IA para análisis rápidos
- **Google Gemini 2.5 Pro**: Modelo de IA para análisis avanzados
- **Natural Language Processing (NLP)**: Procesamiento de lenguaje natural
- **API REST**: Para integración y comunicación

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una cuenta de Google Cloud con acceso a la API de Gemini
- Clave API de Google Gemini

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jecast25/Analisis_opiniones.git
cd Analisis_opiniones
```

### 2. Crear un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las credenciales

Crea un archivo `.env` en el directorio raíz del proyecto:

```bash
cp .env.example .env
```

Edita el archivo `.env` y añade tu clave API de Gemini:

```env
GEMINI_API_KEY=tu_clave_api_aqui
GEMINI_MODEL_FLASH=gemini-2.5-flash
GEMINI_MODEL_PRO=gemini-2.5-pro
```

## 🎯 Uso

### Uso Básico

```python
from analisis_opiniones import AnalizadorOpiniones

# Inicializar el analizador
analizador = AnalizadorOpiniones(model='flash')

# Analizar una opinión individual
opinion = "Me encantó el producto, la calidad es excelente y llegó muy rápido"
resultado = analizador.analizar(opinion)

print(f"Sentimiento: {resultado['sentimiento']}")
print(f"Confianza: {resultado['confianza']}")
print(f"Temas: {resultado['temas']}")
```

### Análisis por Lotes

```python
from analisis_opiniones import AnalizadorOpiniones

# Usar el modelo Pro para análisis más complejos
analizador = AnalizadorOpiniones(model='pro')

# Lista de opiniones
opiniones = [
    "Excelente servicio al cliente",
    "El producto llegó dañado",
    "Precio justo y buena calidad",
    "No cumplió mis expectativas"
]

# Analizar múltiples opiniones
resultados = analizador.analizar_lote(opiniones)

for i, resultado in enumerate(resultados):
    print(f"Opinión {i+1}: {resultado['sentimiento']} ({resultado['confianza']:.2%})")
```

### Generar Reportes

```python
from analisis_opiniones import GeneradorReportes

# Crear reporte a partir de los resultados
generador = GeneradorReportes()
reporte = generador.crear_reporte(
    resultados,
    formato='html',
    incluir_graficos=True
)

# Guardar el reporte
reporte.guardar('reporte_opiniones.html')
```

## 📁 Estructura del Proyecto

```
Analisis_opiniones/
│
├── .streamlit/
│   ├── config.toml
│
├── proyecto.py
|
└── README.md
```

## 🔧 Configuración Avanzada

### Selección de Modelo

El sistema permite elegir entre dos modelos según las necesidades:

**Gemini 2.5 Flash** (Recomendado para):
- Análisis en tiempo real
- Grandes volúmenes de datos
- Aplicaciones que requieren respuestas rápidas
- Casos de uso con presupuesto limitado

**Gemini 2.5 Pro** (Recomendado para):
- Análisis profundos y detallados
- Detección de matices complejos
- Análisis contextual avanzado
- Máxima precisión en la clasificación

### Parámetros de Configuración

```python
config = {
    'temperatura': 0.7,          # Control de aleatoriedad (0.0 - 1.0)
    'max_tokens': 1000,          # Longitud máxima de respuesta
    'top_p': 0.9,                # Muestreo de núcleo
    'umbral_confianza': 0.75,    # Umbral mínimo de confianza
    'idioma_principal': 'es',    # Idioma por defecto
}

analizador = AnalizadorOpiniones(config=config)
```

## 📊 Métricas y Resultados

El sistema proporciona las siguientes métricas:

- **Puntuación de Sentimiento**: Escala de -1 (muy negativo) a +1 (muy positivo)
- **Nivel de Confianza**: Porcentaje de certeza en la clasificación
- **Temas Identificados**: Lista de temas principales con relevancia
- **Palabras Clave**: Términos más significativos en la opinión
- **Intención del Usuario**: Clasificación de la intención (queja, sugerencia, elogio, etc.)

## 🤝 Contribuciones

Las contribuciones son bienvenidas y apreciadas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

Por favor, asegúrate de:
- Seguir las convenciones de código del proyecto
- Añadir tests para nuevas funcionalidades
- Actualizar la documentación según sea necesario
- Mantener la compatibilidad con versiones anteriores

## 📝 Buenas Prácticas

- **Validación de Entrada**: Siempre valida y sanitiza las opiniones antes de procesarlas
- **Manejo de Errores**: Implementa manejo robusto de errores y logs
- **Caché**: Considera implementar caché para opiniones analizadas frecuentemente
- **Monitoreo**: Monitorea el uso de la API y establece límites apropiados
- **Privacidad**: Asegúrate de cumplir con las regulaciones de privacidad de datos

## 🔒 Seguridad

- Nunca compartas tu clave API de Gemini públicamente
- Usa variables de entorno para almacenar credenciales sensibles
- Implementa límites de rate limiting en producción
- Valida y sanitiza todas las entradas de usuario
- Mantén las dependencias actualizadas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Jecast25**

- GitHub: [@Jecast25](https://github.com/Jecast25)
- Proyecto: [Analisis_opiniones](https://github.com/Jecast25/Analisis_opiniones)

## 🙏 Agradecimientos

- Google AI por proporcionar los modelos Gemini
- La comunidad de código abierto por las herramientas y bibliotecas utilizadas
- Todos los contribuidores que hacen posible este proyecto

## 📞 Soporte

Si tienes preguntas, problemas o sugerencias:

1. Revisa la [documentación](docs/)
2. Busca en los [issues existentes](https://github.com/Jecast25/Analisis_opiniones/issues)
3. Crea un [nuevo issue](https://github.com/Jecast25/Analisis_opiniones/issues/new) si es necesario

## 🗺️ Roadmap

- [ ] Implementar análisis de emociones específicas (alegría, enojo, tristeza, etc.)
- [ ] Añadir soporte para análisis de audio y video
- [ ] Desarrollar dashboard web interactivo
- [ ] Integración con más plataformas (Twitter, Facebook, etc.)
- [ ] Análisis comparativo entre diferentes períodos de tiempo
- [ ] Exportación de datos a múltiples formatos (CSV, JSON, Excel)
- [ ] Sistema de alertas automáticas para opiniones críticas

## 📚 Recursos Adicionales

- [Documentación de Google Gemini](https://ai.google.dev/docs)
- [Guía de NLP en Python](https://realpython.com/nltk-nlp-python/)
- [Best Practices para Análisis de Sentimientos](https://towardsdatascience.com/sentiment-analysis-concept-analysis-and-applications-6c94d6f58c17)

---

**Nota**: Este proyecto utiliza modelos de IA avanzados. Los resultados pueden variar según el contexto y la calidad de los datos de entrada. Se recomienda revisar y validar los resultados en casos críticos.
