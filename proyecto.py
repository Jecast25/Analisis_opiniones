# ==============================================================================
# PROTOTIPO DE TESIS: PLATAFORMA UNIVERSAL DE ANÁLISIS INTELIGENTE DE OPINIONES
# INSTITUCIÓN: SENATI - Ingeniería de Ciencia de Datos e IA
# VERSIÓN: 3.1 (Corrección: Timeout Fix + Rate Limiting)
# AÑO: 2025
# AUTORES: Jean Steven Acosta Cruz, Daniel Adrián López Cerpa
# ==============================================================================

import streamlit as st
import pandas as pd
import requests
import json
import time
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import accuracy_score, confusion_matrix
from typing import List, Dict, Any, Union, Optional

# ==============================================================================
# 1. CONFIGURACIÓN Y CONSTANTES DEL SISTEMA
# ==============================================================================

st.set_page_config(
    layout="wide",
    page_title="Plataforma Universal IA - Tesis 2025",
    page_icon="🤖"
)

# Esquema estricto para forzar la salida JSON determinista
SCHEMA_ANALISIS: Dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "sentimiento": {
            "type": "STRING", 
            "enum": ["Positivo", "Negativo", "Neutral"],
            "description": "Polaridad emocional detectada en el texto."
        },
        "categoria": {
            "type": "STRING", 
            "enum": ["Producto", "Atención al Cliente", "Experiencia", "Precio", "Otro"],
            "description": "Aspecto principal del negocio mencionado."
        },
        "explicacion": {
            "type": "STRING",
            "description": "Breve justificación del porqué se asignó la etiqueta."
        },
        "intencion": {
            "type": "STRING", 
            "enum": ["Queja", "Sugerencia", "Felicitación", "Duda"],
            "description": "Intención subyacente del usuario."
        }
    },
    "required": ["sentimiento", "categoria", "explicacion", "intencion"]
}

# Wrapper para permitir procesamiento por lotes (Array de objetos)
SCHEMA_BATCH: Dict[str, Any] = {"type": "ARRAY", "items": SCHEMA_ANALISIS}

# Esquema para el Módulo de Auditoría (Juez IA)
SCHEMA_JUEZ: Dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "puntuacion_calidad": {
            "type": "INTEGER", 
            "description": "Puntuación del 1 (Pésimo) al 5 (Excelente) sobre la calidad del análisis."
        },
        "justificacion_juez": {
            "type": "STRING", 
            "description": "Explicación técnica de la evaluación del juez."
        }
    },
    "required": ["puntuacion_calidad", "justificacion_juez"]
}

# ==============================================================================
# 2. LÓGICA DE NEGOCIO (CORE BACKEND)
# ==============================================================================

def call_gemini_batch_api(
    list_of_opinions: List[str], 
    api_key_to_use: str, 
    retries: int = 3
) -> List[Dict[str, Any]]:
    """
    Orquesta la llamada a la API de Gemini 2.5 Flash utilizando procesamiento por lotes.
    INCLUYE MEJORAS: Timeout extendido y limpieza de Markdown.
    """
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key_to_use}"
    
    system_prompt = (
        "Eres un analista experto en Customer Experience para Perú y Latam. "
        "Analiza el lote de opiniones. Detecta sarcasmo, jerga peruana y doble sentido. "
        "Responde EXCLUSIVAMENTE con un JSON Array válido siguiendo el esquema provisto."
    )
    
    sanitized_opinions = [str(op).replace('"', "'").strip() for op in list_of_opinions]
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": f"Analiza este lote: {json.dumps(sanitized_opinions)} "}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": SCHEMA_BATCH,
            "temperature": 0.1 
        }
    }
    
    for attempt in range(retries):
        try:
            # CORRECCIÓN 1: Timeout aumentado a 120 segundos para evitar cortes prematuros
            response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=120)
            
            if response.status_code == 200:
                try:
                    text_resp = response.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    # CORRECCIÓN 2: Limpieza de bloques Markdown (```json ... ```)
                    # A veces la API envía el JSON envuelto en texto, lo que rompe el json.loads
                    text_resp = text_resp.replace("```json", "").replace("```", "").strip()
                    
                    return json.loads(text_resp)
                except (KeyError, json.JSONDecodeError, IndexError) as e:
                    return [{"sentimiento": "Error", "categoria": "Error", "explicacion": f"Error Parseo: {str(e)}", "intencion": "Error"}] * len(list_of_opinions)
            
            elif response.status_code in [429, 503]:
                # Backoff Exponencial aumentado: 5s, 10s, 20s...
                wait_time = 5 * (attempt + 1)
                time.sleep(wait_time)
            
            else:
                if "API_KEY_INVALID" in response.text or "PERMISSION_DENIED" in response.text:
                    return [{"sentimiento": "Error", "explicacion": "API_KEY_INVALID"}] 
                break
                
        except requests.exceptions.RequestException as e:
            print(f"\n>>> 🛑 DIAGNÓSTICO ERROR REAL: {e}")
            print(f">>> TIPO DE ERROR: {type(e).__name__}\n")
            time.sleep(2) 
            
    return [{"sentimiento": "Error", "categoria": "Error", "explicacion": "Fallo Conexión/Timeout", "intencion": "Error"}] * len(list_of_opinions)

def audit_with_ai_judge(
    original_text: str, 
    manual_label: str, 
    ai_label: str, 
    ai_explanation: str, 
    api_key: str
) -> Dict[str, Any]:
    """
    Implementa el patrón 'LLM-as-a-Judge' para auditoría cualitativa.
    """
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    prompt_audit = f"""
    Actúa como Auditor Senior de Calidad Lingüística.
    
    DATOS DEL CASO:
    1. Texto Usuario: "{original_text}"
    2. Etiqueta Real (Humano): "{manual_label}"
    3. Predicción Modelo IA: "{ai_label}"
    4. Explicación dada por IA: "{ai_explanation}"

    TAREA:
    Evalúa del 1 al 5 la calidad del análisis de la IA. 
    - 5: Perfecto. Entendió matices, jerga peruana y contexto implícito.
    - 1: Pésimo. Alucinación, error grave de polaridad o no entendió la jerga.
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt_audit}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": SCHEMA_JUEZ,
            "temperature": 0.0
        }
    }
    
    try:
        res = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=120)
        if res.status_code == 200:
            text_resp = res.json()['candidates'][0]['content']['parts'][0]['text']
            text_resp = text_resp.replace("```json", "").replace("```", "").strip()
            return json.loads(text_resp)
    except Exception:
        pass
        
    return {"puntuacion_calidad": 0, "justificacion_juez": "Error técnico en módulo de auditoría"}

# ==============================================================================
# 3. INTERFAZ DE USUARIO (FRONTEND STREAMLIT)
# ==============================================================================

def main():
    st.title("Plataforma Universal de Análisis Inteligente de Opiniones")
    st.markdown("**Arquitectura:** Cloud-Native Batch Processing | **Modelo:** Gemini 2.5 Flash + Pro (Auditor)")

    # --- 3.1 GESTOR DE CLÚSTER (SIDEBAR) ---
    st.sidebar.header("🔑 Configuración de Clúster")
    st.sidebar.info("Gestión dinámica de nodos API para evitar cuellos de botella.")
    
    if 'api_keys_list' not in st.session_state: 
        st.session_state.api_keys_list = []

    with st.sidebar.form("key_form", clear_on_submit=True):
        new_key = st.text_input("Añadir API Key (Google AI Studio)", type="password")
        submitted = st.form_submit_button("Agregar Nodo")
        if submitted and new_key:
            if new_key not in st.session_state.api_keys_list:
                st.session_state.api_keys_list.append(new_key)
                st.sidebar.success("Nodo añadido correctamente.")
            else:
                st.sidebar.warning("Esta Key ya existe en el pool.")

    st.sidebar.markdown(f"**Nodos Activos:** `{len(st.session_state.api_keys_list)}`")
    
    if not st.session_state.api_keys_list:
        st.warning("⚠️ Sistema en Pausa: Añade al menos una API Key en el panel lateral para iniciar el motor de inferencia.")
        st.stop()

    # --- 3.2 NAVEGACIÓN MODULAR ---
    tab_prod, tab_val, tab_audit = st.tabs([
        "🏭 Producción (Análisis Masivo)", 
        "🧪 Validación (Métricas ML)", 
        "⚖️ Auditoría Cognitiva (Juez IA)"
    ])

    # --- PESTAÑA PRODUCCIÓN ---
    with tab_prod:
        st.subheader("Ingesta y Procesamiento de Datos")
        file = st.file_uploader("Cargar Dataset (CSV UTF-8)", type=["csv"], help="Debe contener una columna llamada 'comentario'")
        
        if file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower().str.strip()
            
            if 'comentario' in df.columns:
                st.success(f"Dataset cargado correctamente: {len(df)} registros listos para inferencia.")
                
                if st.button("🚀 Iniciar Motor de Inferencia (Batch)", type="primary"):
                    opiniones = df['comentario'].astype(str).tolist()
                    
                    # CORRECCIÓN 3: Batch Size reducido a 3 para estabilidad en capa gratuita
                    batch_size = 5
                    resultados = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    start_time = time.time()
                    
                    keys = st.session_state.api_keys_list
                    
                    for i in range(0, len(opiniones), batch_size):
                        lote = opiniones[i:i+batch_size]
                        
                        current_key_idx = (i // batch_size) % len(keys)
                        current_key = keys[current_key_idx]
                        
                        status_text.markdown(f"🔄 Procesando bloque **{i} - {i+len(lote)}** | Nodo Activo: `...{current_key[-4:]}`")
                        
                        res_batch = call_gemini_batch_api(lote, current_key)
                        
                        if res_batch and res_batch[0].get("explicacion") == "API_KEY_INVALID":
                            status_text.warning("⚠️ Nodo caído (Key inválida). Reintentando con siguiente nodo...")
                            if len(keys) > 1:
                                next_key = keys[(current_key_idx + 1) % len(keys)]
                                res_batch = call_gemini_batch_api(lote, next_key)
                        
                        resultados.extend(res_batch)
                        
                        progress_bar.progress(min((i + batch_size) / len(opiniones), 1.0))
                            
                        
                        # CORRECCIÓN 4: Espera de 4 segundos obligatoria (15 peticiones/min = 1 cada 4s)
                        time.sleep(5.5) 
                    
                    df_res = pd.DataFrame(resultados)
                    df_final = pd.concat([df, df_res], axis=1)
                    st.session_state['df_prod'] = df_final
                    
                    elapsed_time = time.time() - start_time
                    st.success(f"✅ Procesamiento finalizado en {elapsed_time:.2f} segundos. Velocidad: {len(df)/elapsed_time:.1f} regs/seg.")
            else:
                st.error("Error de Esquema: No se encontró la columna 'comentario' en el CSV.")

        if 'df_prod' in st.session_state:
            df_show = st.session_state['df_prod']
            st.divider()
            
            df_clean = df_show[df_show['sentimiento'] != 'Error']
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("### Distribución de Sentimientos")
                if not df_clean.empty:
                    fig = px.pie(df_clean, names='sentimiento', hole=0.4, 
                                 color='sentimiento', 
                                 color_discrete_map={'Positivo':'#00cc96','Negativo':'#EF553B','Neutral':'#636efa'})
                    st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.markdown("### Intención del Usuario")
                if 'intencion' in df_clean.columns and not df_clean.empty:
                    fig2 = px.bar(df_clean['intencion'].value_counts().reset_index(), x='intencion', y='count', color='intencion')
                    st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(df_show, use_container_width=True)

    # --- PESTAÑA VALIDACIÓN ---
    with tab_val:
        st.subheader("Validación Cruzada (Ground Truth vs Predicción)")
        st.markdown("Carga un dataset etiquetado para calcular la Matriz de Confusión y Accuracy.")
        
        val_file = st.file_uploader("CSV Etiquetado ('comentario', 'sentimiento_manual')", type=["csv"], key="val")
        
        if val_file:
            df_val = pd.read_csv(val_file)
            if st.button("Ejecutar Benchmark de Precisión"):
                with st.spinner("Realizando inferencia sobre set de validación..."):
                    sample_limit = min(len(df_val), 50)
                    df_subset = df_val.head(sample_limit)
                    
                    # Nota: Para validación también usamos el wrapper corregido
                    res = call_gemini_batch_api(df_subset['comentario'].astype(str).tolist(), st.session_state.api_keys_list[0])
                    
                    df_res_val = pd.DataFrame(res)
                    df_combined = pd.concat([df_subset.reset_index(drop=True), df_res_val], axis=1)
                    st.session_state['df_val_results'] = df_combined
                
                y_true = df_combined['sentimiento_manual'].astype(str).str.capitalize().str.strip()
                y_pred = df_combined['sentimiento'].astype(str).str.capitalize().str.strip()
                
                acc = accuracy_score(y_true, y_pred)
                
                kpi1, kpi2 = st.columns(2)
                kpi1.metric("Exactitud Global (Accuracy)", f"{acc*100:.2f}%", delta="Objetivo: >85%")
                kpi2.metric("Muestras Evaluadas", len(df_combined))
                
                labels = ["Positivo", "Negativo", "Neutral"]
                cm = confusion_matrix(y_true, y_pred, labels=labels)
                
                fig_cm = ff.create_annotated_heatmap(
                    z=cm, x=labels, y=labels, colorscale='Blues', showscale=True
                )
                fig_cm.update_layout(title_text="<b>Matriz de Confusión</b>", xaxis_title="Predicción IA", yaxis_title="Verdad Humana")
                st.plotly_chart(fig_cm, use_container_width=True)

    # --- PESTAÑA AUDITORÍA ---
    with tab_audit:
        st.header("⚖️ Auditoría Cognitiva (LLM-as-a-Judge)")
        st.info("Utiliza Gemini 2.5 Pro para evaluar la calidad del razonamiento de Gemini 2.5 Flash.")
        
        if 'df_val_results' in st.session_state:
            df_audit_source = st.session_state['df_val_results']
            
            col_sel, col_btn = st.columns([3, 1])
            with col_sel:
                audit_mode = st.radio("Estrategia de Muestreo:", ["Auditar Discrepancias (Donde la IA falló)", "Muestreo Aleatorio (Auditoría ciega)"])
            
            if "Discrepancias" in audit_mode:
                mask = df_audit_source['sentimiento_manual'].str.lower() != df_audit_source['sentimiento'].str.lower()
                sample_audit = df_audit_source[mask].head(5)
            else:
                sample_audit = df_audit_source.sample(min(5, len(df_audit_source)))
            
            with col_btn:
                st.write("") 
                st.write("")
                run_audit = st.button("Iniciar Juez Virtual")
            
            st.write(f"Muestra seleccionada: {len(sample_audit)} casos.")

            if run_audit:
                audit_results = []
                prog_audit = st.progress(0)
                
                for idx, (index, row) in enumerate(sample_audit.iterrows()):
                    veredicto = audit_with_ai_judge(
                        original_text=row['comentario'],
                        manual_label=row['sentimiento_manual'],
                        ai_label=row['sentimiento'],
                        ai_explanation=row['explicacion'],
                        api_key=st.session_state.api_keys_list[0]
                    )
                    full_row = row.to_dict()
                    full_row.update(veredicto)
                    audit_results.append(full_row)
                    prog_audit.progress((idx + 1) / len(sample_audit))
                    time.sleep(2) # Pequeña pausa para no saturar al Juez
                
                df_audit_final = pd.DataFrame(audit_results)
                
                st.divider()
                if not df_audit_final.empty:
                    avg_score = df_audit_final['puntuacion_calidad'].mean()
                    st.metric("Calidad de Razonamiento Promedio (1-5)", f"{avg_score:.2f}")
                    
                    st.dataframe(
                        df_audit_final[['comentario', 'sentimiento', 'puntuacion_calidad', 'justificacion_juez']],
                        use_container_width=True
                    )
        else:
            st.warning("Requisito: Ejecuta primero la validación en la pestaña anterior para tener datos que auditar.")

if __name__ == "__main__":
    main()