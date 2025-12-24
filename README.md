# Analisis_opiniones 🔍💬

Sistema inteligente de análisis de opiniones para la mejora continua, potenciado por los modelos de IA avanzados **Gemini 2.5 Flash** y **Gemini 2.5 Pro** de Google.

## 📋 Descripción del Proyecto

**Analisis_opiniones** es una herramienta diseñada para procesar, analizar y extraer insights valiosos de opiniones y comentarios de usuarios. Utilizando la tecnología de vanguardia de Google Gemini 2.5, este sistema permite a las organizaciones comprender mejor las percepciones de sus clientes, identificar áreas de mejora y tomar decisiones basadas en datos para la mejora continua.

### 🎯 Objetivo Principal

Transformar grandes volúmenes de opiniones y comentarios en información accionable mediante el análisis automático de sentimientos, detección de temas clave y generación de reportes inteligentes que faciliten la toma de decisiones estratégicas.

## ✨ Características Principales

- **Análisis de Sentimientos Avanzado**: Determina automáticamente si las opiniones son positivas, negativas o neutrales con alta precisión.
- **Detección de Temas**: Identifica los temas principales y tendencias en grandes conjuntos de opiniones.
- **Procesamiento en Tiempo Real**: Analiza opiniones de manera rápida y eficiente utilizando Gemini 2.5 Flash para respuestas rápidas.
- **Análisis Profundo**: Utiliza Gemini 2.5 Pro para análisis más complejos y detallados cuando se requiere mayor profundidad.
- **Generación de Insights**: Extrae conclusiones y recomendaciones accionables automáticamente.
- **Clasificación Inteligente**: Categoriza opiniones por temas, prioridad y tipo de feedback.
- **Reportes Visuales**: Genera reportes comprensibles y visualizaciones de los datos analizados.

## 🤖 Tecnología: Gemini 2.5

Este proyecto aprovecha dos modelos de la familia Gemini 2.5 de Google:

### Gemini 2.5 Flash
- **Propósito**: Análisis rápido y eficiente
- **Uso en el proyecto**: Procesamiento en tiempo real de grandes volúmenes de opiniones
- **Ventajas**: Baja latencia, ideal para aplicaciones interactivas

### Gemini 2.5 Pro
- **Propósito**: Análisis profundo y complejo
- **Uso en el proyecto**: Análisis detallado, generación de insights complejos y reportes elaborados
- **Ventajas**: Mayor capacidad de razonamiento, mejor comprensión contextual

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google Cloud con acceso a la API de Gemini
- Clave de API de Google Gemini

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Jecast25/Analisis_opiniones.git
   cd Analisis_opiniones
   ```

2. **Crear un entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar credenciales**
   - Crea un archivo `.env` en la raíz del proyecto
   - Añade tu clave de API de Gemini:
     ```
     GEMINI_API_KEY=tu_clave_api_aqui
     ```

## 💻 Uso

### Uso Básico

```python
from analisis_opiniones import AnalizadorOpiniones

# Inicializar el analizador
analizador = AnalizadorOpiniones(modelo="flash")  # o "pro"

# Analizar una opinión
opinion = "El producto es excelente, superó mis expectativas"
resultado = analizador.analizar(opinion)

print(f"Sentimiento: {resultado['sentimiento']}")
print(f"Confianza: {resultado['confianza']}")
print(f"Temas: {resultado['temas']}")
```

### Análisis por Lotes

```python
# Analizar múltiples opiniones
opiniones = [
    "Muy satisfecho con el servicio",
    "La entrega fue tardía",
    "Excelente calidad-precio"
]

resultados = analizador.analizar_lote(opiniones)
```

### Generación de Reportes

```python
# Generar un reporte completo
reporte = analizador.generar_reporte(opiniones)
reporte.guardar("reporte_opiniones.pdf")
```

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│                  Entrada de Datos                    │
│         (Opiniones, Comentarios, Reviews)            │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Preprocesamiento                        │
│    (Limpieza, Normalización, Tokenización)          │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            Selección de Modelo                       │
│     ┌──────────────┐      ┌──────────────┐         │
│     │ Gemini 2.5   │      │ Gemini 2.5   │         │
│     │    Flash     │      │    Pro       │         │
│     │ (Rápido)     │      │ (Profundo)   │         │
│     └──────────────┘      └──────────────┘         │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│                 Análisis IA                          │
│  - Análisis de Sentimientos                         │
│  - Extracción de Temas                              │
│  - Clasificación de Intenciones                     │
│  - Generación de Insights                           │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Post-procesamiento                      │
│    (Agregación, Visualización, Reportes)            │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│                  Salida                              │
│     (Insights, Reportes, Recomendaciones)           │
└─────────────────────────────────────────────────────┘
```

## 🔧 Configuración Avanzada

### Selección de Modelo

Puedes configurar qué modelo usar según tus necesidades:

```python
# Para análisis rápido (mayor velocidad)
analizador = AnalizadorOpiniones(
    modelo="flash",
    temperatura=0.7,
    max_tokens=1024
)

# Para análisis profundo (mayor precisión)
analizador = AnalizadorOpiniones(
    modelo="pro",
    temperatura=0.3,
    max_tokens=2048
)
```

### Parámetros de Configuración

- **modelo**: `"flash"` o `"pro"` - Selección del modelo Gemini
- **temperatura**: `0.0-1.0` - Controla la creatividad de las respuestas
- **max_tokens**: Número máximo de tokens en la respuesta
- **idioma**: Idioma de análisis (por defecto: `"es"`)

## 📈 Casos de Uso

1. **E-commerce**: Análisis de reviews de productos para identificar áreas de mejora
2. **Servicios**: Evaluación de comentarios de clientes para mejorar la calidad del servicio
3. **Redes Sociales**: Monitoreo de menciones de marca y análisis de percepción pública
4. **Encuestas**: Procesamiento automático de respuestas abiertas en encuestas
5. **Soporte al Cliente**: Análisis de tickets y feedback para optimizar procesos

## 🤝 Contribuciones

Las contribuciones son bienvenidas y apreciadas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código establecidas
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Asegúrate de que todos los tests pasen antes de enviar un PR

## 📝 Roadmap

- [ ] Integración con APIs de redes sociales
- [ ] Dashboard web interactivo
- [ ] Soporte para más idiomas
- [ ] Análisis de tendencias temporales
- [ ] Exportación de datos a múltiples formatos
- [ ] API REST para integración con otros sistemas
- [ ] Análisis de imágenes en opiniones
- [ ] Sistema de alertas en tiempo real

## 🔒 Seguridad

- Las claves de API nunca deben commitearse al repositorio
- Utiliza variables de entorno para información sensible
- Los datos de usuarios se procesan de manera confidencial
- Cumplimiento con normativas de protección de datos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Jean Steven Acosta Cruz** - [@Jecast25](https://github.com/Jecast25)

## 🙏 Agradecimientos

- Google por proporcionar acceso a los modelos Gemini 2.5
- La comunidad de código abierto por sus valiosas contribuciones
- Todos los contribuidores que han ayudado a mejorar este proyecto

## 📞 Contacto

Para preguntas, sugerencias o reportar problemas:
- Abre un issue en GitHub
- Contacta al autor a través de su perfil de GitHub

## 🔗 Enlaces Útiles

- [Documentación de Google Gemini](https://ai.google.dev/gemini-api/docs)
- [Guía de API de Gemini](https://ai.google.dev/gemini-api)
- [Mejores Prácticas de Análisis de Sentimientos](https://cloud.google.com/natural-language/docs/sentiment-tutorial)

---

⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub
