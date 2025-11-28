#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Interactivo PPE RECSO Campaña 2024-25
Regiones Pampeanas

Estructura base para implementación con Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Dashboard PPE RECSO 2024-25",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO DE DATOS
# ============================================================================

@st.cache_data
def load_data():
    """Carga y procesa el dataset principal"""
    import os
    # Usar ruta relativa para compatibilidad con Streamlit Cloud
    file_path = "PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

    # Si no existe, intentar con ruta absoluta (para ejecución local)
    if not os.path.exists(file_path):
        file_path = "/home/leodiazdt/dashboard-ppe-2024-25/PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

    # Leer CSV
    df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')

    # Convertir fechas
    fecha_columns = ['FECHA DE SIEMBRA', 'Emergencia', 'COSECHA']
    for col in fecha_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')

    # Convertir columnas numéricas
    numeric_columns = ['RENDIMIENTO', 'IM', 'IT', 'Alt', 'Vuelco', 'P1000']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Agregar columnas calculadas
    df['Mes_Siembra'] = df['FECHA DE SIEMBRA'].dt.month
    df['Año_Siembra'] = df['FECHA DE SIEMBRA'].dt.year
    df['Mes_Cosecha'] = df['COSECHA'].dt.month

    if 'FECHA DE SIEMBRA' in df.columns and 'COSECHA' in df.columns:
        df['Dias_Ciclo'] = (df['COSECHA'] - df['FECHA DE SIEMBRA']).dt.days

    return df

@st.cache_data
def get_summary_stats(df):
    """Calcula estadísticas resumen del dataset"""
    stats = {
        'total_ensayos': len(df),
        'rendimiento_promedio': df['RENDIMIENTO'].mean(),
        'rendimiento_mediano': df['RENDIMIENTO'].median(),
        'rendimiento_min': df['RENDIMIENTO'].min(),
        'rendimiento_max': df['RENDIMIENTO'].max(),
        'cv': (df['RENDIMIENTO'].std() / df['RENDIMIENTO'].mean()) * 100,
        'n_localidades': df['LOCALIDAD'].nunique(),
        'n_variedades': df['VARIEDAD'].nunique(),
        'mejor_localidad': df.groupby('LOCALIDAD')['RENDIMIENTO'].mean().idxmax(),
        'mejor_variedad': df.groupby('VARIEDAD')['RENDIMIENTO'].mean().idxmax()
    }
    return stats

# ============================================================================
# CARGAR DATOS
# ============================================================================

df = load_data()
stats = get_summary_stats(df)

# ============================================================================
# SIDEBAR - FILTROS GLOBALES
# ============================================================================

st.sidebar.header("🔍 Filtros Globales")

# Filtro de Región
regiones = ['Todas'] + sorted(df['REGION'].unique().tolist())
region_seleccionada = st.sidebar.selectbox("Región", regiones)

# Filtro de Subregión
subregiones = ['Todas'] + sorted(df['SUBREGION'].unique().tolist())
subregion_seleccionada = st.sidebar.multiselect("Subregión", subregiones, default=['Todas'])

# Filtro de Localidad
localidades = ['Todas'] + sorted(df['LOCALIDAD'].unique().tolist())
localidad_seleccionada = st.sidebar.multiselect("Localidad", localidades, default=['Todas'])

# Filtro de Variedad
variedades = ['Todas'] + sorted(df['VARIEDAD'].unique().tolist())
variedad_seleccionada = st.sidebar.multiselect("Variedad", variedades, default=['Todas'])

# Filtro de Mes de Siembra
meses_dict = {10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
meses_disponibles = ['Todos'] + [f"{v} ({k})" for k, v in sorted(meses_dict.items())]
mes_seleccionado = st.sidebar.multiselect("Mes de Siembra", meses_disponibles, default=['Todos'])

# Filtro de Rango de Rendimiento
min_rend = int(df['RENDIMIENTO'].min())
max_rend = int(df['RENDIMIENTO'].max())
rango_rendimiento = st.sidebar.slider(
    "Rango de Rendimiento (kg/ha)",
    min_value=min_rend,
    max_value=max_rend,
    value=(min_rend, max_rend)
)

# Botón Reset
if st.sidebar.button("🔄 Reset Filtros"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"**Dataset original:** {len(df):,} ensayos")

# ============================================================================
# APLICAR FILTROS
# ============================================================================

df_filtered = df.copy()

if region_seleccionada != 'Todas':
    df_filtered = df_filtered[df_filtered['REGION'] == region_seleccionada]

if 'Todas' not in subregion_seleccionada:
    df_filtered = df_filtered[df_filtered['SUBREGION'].isin(subregion_seleccionada)]

if 'Todas' not in localidad_seleccionada:
    df_filtered = df_filtered[df_filtered['LOCALIDAD'].isin(localidad_seleccionada)]

if 'Todas' not in variedad_seleccionada:
    df_filtered = df_filtered[df_filtered['VARIEDAD'].isin(variedad_seleccionada)]

if 'Todos' not in mes_seleccionado:
    meses_nums = [int(m.split('(')[1].split(')')[0]) for m in mes_seleccionado]
    df_filtered = df_filtered[df_filtered['Mes_Siembra'].isin(meses_nums)]

df_filtered = df_filtered[
    (df_filtered['RENDIMIENTO'] >= rango_rendimiento[0]) &
    (df_filtered['RENDIMIENTO'] <= rango_rendimiento[1])
]

stats_filtered = get_summary_stats(df_filtered)

st.sidebar.success(f"**Ensayos filtrados:** {len(df_filtered):,}")

# ============================================================================
# PÁGINA PRINCIPAL
# ============================================================================

st.title("🌾 Dashboard PPE RECSO - Campaña 2024-25")
st.markdown("### Regiones Pampeanas - Análisis Interactivo de Rendimientos")

# Crear pestañas para las diferentes páginas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vista General",
    "🗺️ Análisis Geográfico",
    "🧬 Análisis Varietal",
    "📅 Análisis Temporal",
    "🎯 Recomendador"
])

# ============================================================================
# PÁGINA 1: VISTA GENERAL
# ============================================================================

with tab1:
    st.header("Vista General - Executive Summary")

    # KPIs Principales
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Rendimiento Promedio",
            value=f"{stats_filtered['rendimiento_promedio']:.0f} kg/ha",
            delta=f"{stats_filtered['rendimiento_promedio'] - stats['rendimiento_promedio']:.0f} kg/ha"
        )

    with col2:
        st.metric(
            label="Total de Ensayos",
            value=f"{stats_filtered['total_ensayos']:,}",
            delta=f"{stats_filtered['total_ensayos'] - stats['total_ensayos']:,}"
        )

    with col3:
        st.metric(
            label="Localidades",
            value=f"{stats_filtered['n_localidades']}",
            delta=f"{stats_filtered['n_localidades'] - stats['n_localidades']}"
        )

    with col4:
        st.metric(
            label="Variedades",
            value=f"{stats_filtered['n_variedades']}",
            delta=f"{stats_filtered['n_variedades'] - stats['n_variedades']}"
        )

    with col5:
        st.metric(
            label="Coef. Variación",
            value=f"{stats_filtered['cv']:.1f}%"
        )

    st.markdown("---")

    # Fila de gráficos
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 10 Localidades por Rendimiento")

        localidad_stats = df_filtered.groupby('LOCALIDAD')['RENDIMIENTO'].agg([
            'count', 'mean', 'std'
        ]).round(2).reset_index()
        localidad_stats = localidad_stats[localidad_stats['count'] >= 5]
        localidad_stats = localidad_stats.sort_values('mean', ascending=False).head(10)

        fig_barras = px.bar(
            localidad_stats,
            x='mean',
            y='LOCALIDAD',
            orientation='h',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'Rendimiento Promedio (kg/ha)', 'LOCALIDAD': 'Localidad'},
            text='mean'
        )
        fig_barras.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig_barras.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_right:
        st.subheader("Top 10 Variedades por Rendimiento")

        variedad_stats = df_filtered.groupby('VARIEDAD')['RENDIMIENTO'].agg([
            'count', 'mean', 'std'
        ]).round(2).reset_index()
        variedad_stats = variedad_stats[variedad_stats['count'] >= 5]
        variedad_stats = variedad_stats.sort_values('mean', ascending=False).head(10)

        fig_barras_var = px.bar(
            variedad_stats,
            x='mean',
            y='VARIEDAD',
            orientation='h',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'Rendimiento Promedio (kg/ha)', 'VARIEDAD': 'Variedad'},
            text='mean'
        )
        fig_barras_var.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig_barras_var.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_barras_var, use_container_width=True)

    # Gráfico de distribución
    st.subheader("Distribución de Rendimientos")

    fig_hist = px.histogram(
        df_filtered,
        x='RENDIMIENTO',
        nbins=50,
        color_discrete_sequence=['#3498DB'],
        labels={'RENDIMIENTO': 'Rendimiento (kg/ha)', 'count': 'Frecuencia'}
    )
    fig_hist.add_vline(
        x=stats_filtered['rendimiento_promedio'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Media: {stats_filtered['rendimiento_promedio']:.0f} kg/ha"
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Métricas adicionales
    st.markdown("---")
    st.subheader("Métricas de Calidad")

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        completitud = (1 - df_filtered.isnull().sum().sum() / (len(df_filtered) * len(df_filtered.columns))) * 100
        st.metric("Completitud de Datos", f"{completitud:.1f}%")

    with col_b:
        ensayos_sig = df_filtered[df_filtered['Sig'] == '+'].shape[0]
        st.metric("Ensayos Superiores (+)", f"{ensayos_sig}")

    with col_c:
        ensayos_completados = df_filtered['COSECHA'].notna().sum()
        pct_completados = (ensayos_completados / len(df_filtered)) * 100
        st.metric("Ensayos Completados", f"{pct_completados:.1f}%")

    with col_d:
        rango = stats_filtered['rendimiento_max'] - stats_filtered['rendimiento_min']
        st.metric("Rango de Rendimiento", f"{rango:.0f} kg/ha")

# ============================================================================
# PÁGINA 2: ANÁLISIS GEOGRÁFICO
# ============================================================================

with tab2:
    st.header("Análisis Geográfico")

    # Tabla comparativa de localidades
    st.subheader("Tabla Comparativa de Localidades")

    localidad_completa = df_filtered.groupby('LOCALIDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'median', 'std', 'min', 'max'],
        'REGION': 'first',
        'SUBREGION': 'first'
    }).round(2).reset_index()

    localidad_completa.columns = ['Localidad', 'N_Ensayos', 'Media', 'Mediana',
                                    'Desv_Std', 'Min', 'Max', 'Region', 'Subregion']

    # Calcular CV
    localidad_completa['CV_%'] = (localidad_completa['Desv_Std'] / localidad_completa['Media'] * 100).round(1)

    # Ordenar por rendimiento medio
    localidad_completa = localidad_completa.sort_values('Media', ascending=False)

    st.dataframe(
        localidad_completa,
        use_container_width=True,
        height=400
    )

    # Botón de descarga
    csv = localidad_completa.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar tabla como CSV",
        data=csv,
        file_name='localidades_rendimiento.csv',
        mime='text/csv'
    )

    st.markdown("---")

    # Gráficos por región/subregión
    col_reg, col_subreg = st.columns(2)

    with col_reg:
        st.subheader("Rendimiento por Región")

        region_stats = df_filtered.groupby('REGION')['RENDIMIENTO'].agg(['count', 'mean']).reset_index()

        fig_region = px.bar(
            region_stats,
            x='REGION',
            y='mean',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'Rendimiento Promedio (kg/ha)', 'REGION': 'Región'},
            text='mean'
        )
        fig_region.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        st.plotly_chart(fig_region, use_container_width=True)

    with col_subreg:
        st.subheader("Rendimiento por Subregión")

        subregion_stats = df_filtered.groupby('SUBREGION')['RENDIMIENTO'].agg(['count', 'mean']).reset_index()

        fig_subregion = px.bar(
            subregion_stats,
            x='SUBREGION',
            y='mean',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'Rendimiento Promedio (kg/ha)', 'SUBREGION': 'Subregión'},
            text='mean'
        )
        fig_subregion.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        st.plotly_chart(fig_subregion, use_container_width=True)

    # Scatter plot: Rendimiento vs N° ensayos
    st.subheader("Rendimiento vs Cantidad de Ensayos por Localidad")

    scatter_data = df_filtered.groupby('LOCALIDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'std']
    }).reset_index()
    scatter_data.columns = ['Localidad', 'N_Ensayos', 'Rendimiento_Medio', 'Desv_Std']

    fig_scatter = px.scatter(
        scatter_data,
        x='N_Ensayos',
        y='Rendimiento_Medio',
        size='Desv_Std',
        color='Rendimiento_Medio',
        hover_name='Localidad',
        color_continuous_scale='RdYlGn',
        labels={
            'N_Ensayos': 'Número de Ensayos',
            'Rendimiento_Medio': 'Rendimiento Promedio (kg/ha)',
            'Desv_Std': 'Desviación Estándar'
        }
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================================
# PÁGINA 3: ANÁLISIS VARIETAL
# ============================================================================

with tab3:
    st.header("Análisis Varietal")

    # Tabla de variedades
    st.subheader("Tabla de Variedades con Métricas")

    variedad_completa = df_filtered.groupby('VARIEDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'median', 'std', 'min', 'max'],
        'GM': 'first'
    }).round(2).reset_index()

    variedad_completa.columns = ['Variedad', 'N_Ensayos', 'Media', 'Mediana',
                                   'Desv_Std', 'Min', 'Max', 'GM']

    variedad_completa['CV_%'] = (variedad_completa['Desv_Std'] / variedad_completa['Media'] * 100).round(1)

    # Clasificar por consistencia
    def clasificar_consistencia(cv):
        if cv < 15:
            return 'Muy Alta'
        elif cv < 20:
            return 'Alta'
        elif cv < 25:
            return 'Media'
        else:
            return 'Baja'

    variedad_completa['Consistencia'] = variedad_completa['CV_%'].apply(clasificar_consistencia)

    variedad_completa = variedad_completa.sort_values('Media', ascending=False)

    st.dataframe(
        variedad_completa,
        use_container_width=True,
        height=400
    )

    # Botón descarga
    csv_var = variedad_completa.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar tabla de variedades como CSV",
        data=csv_var,
        file_name='variedades_rendimiento.csv',
        mime='text/csv'
    )

    st.markdown("---")

    # Gráfico de burbujas: Rendimiento vs Consistencia
    st.subheader("Rendimiento vs Consistencia (CV)")
    st.caption("Cuadrante inferior derecho = IDEAL (alto rendimiento + alta consistencia)")

    # Filtrar variedades con mínimo 5 ensayos
    bubble_data = variedad_completa[variedad_completa['N_Ensayos'] >= 5].copy()

    fig_bubble = px.scatter(
        bubble_data,
        x='Media',
        y='CV_%',
        size='N_Ensayos',
        color='GM',
        hover_name='Variedad',
        labels={
            'Media': 'Rendimiento Promedio (kg/ha)',
            'CV_%': 'Coeficiente de Variación (%)',
            'N_Ensayos': 'Número de Ensayos'
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Líneas de referencia
    mean_rend = bubble_data['Media'].mean()
    mean_cv = bubble_data['CV_%'].mean()

    fig_bubble.add_hline(y=mean_cv, line_dash="dash", line_color="gray", opacity=0.5)
    fig_bubble.add_vline(x=mean_rend, line_dash="dash", line_color="gray", opacity=0.5)

    fig_bubble.update_layout(height=600)
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Comparador de variedades
    st.markdown("---")
    st.subheader("Comparador de Variedades")

    variedades_disponibles = sorted(df_filtered['VARIEDAD'].unique().tolist())
    variedades_comparar = st.multiselect(
        "Selecciona hasta 4 variedades para comparar:",
        variedades_disponibles,
        max_selections=4
    )

    if variedades_comparar:
        df_comparar = df_filtered[df_filtered['VARIEDAD'].isin(variedades_comparar)]

        # Box plot comparativo
        fig_box = px.box(
            df_comparar,
            x='VARIEDAD',
            y='RENDIMIENTO',
            color='VARIEDAD',
            labels={'RENDIMIENTO': 'Rendimiento (kg/ha)', 'VARIEDAD': 'Variedad'},
            points='all'
        )
        fig_box.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_box, use_container_width=True)

        # Tabla comparativa
        st.subheader("Estadísticas Comparativas")

        comp_stats = df_comparar.groupby('VARIEDAD')['RENDIMIENTO'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)

        st.dataframe(comp_stats, use_container_width=True)

# ============================================================================
# PÁGINA 4: ANÁLISIS TEMPORAL
# ============================================================================

with tab4:
    st.header("Análisis Temporal y Fenológico")

    # Rendimiento por mes de siembra
    st.subheader("Rendimiento por Mes de Siembra")

    df_temp = df_filtered[df_filtered['Mes_Siembra'].notna()].copy()
    df_temp['Mes_Nombre'] = df_temp['Mes_Siembra'].map({10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'})

    mes_stats = df_temp.groupby('Mes_Nombre')['RENDIMIENTO'].agg(['count', 'mean', 'median']).reset_index()

    col_mes1, col_mes2 = st.columns(2)

    with col_mes1:
        fig_mes_bar = px.bar(
            mes_stats,
            x='Mes_Nombre',
            y='mean',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'Rendimiento Promedio (kg/ha)', 'Mes_Nombre': 'Mes de Siembra'},
            text='mean'
        )
        fig_mes_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        st.plotly_chart(fig_mes_bar, use_container_width=True)

    with col_mes2:
        fig_mes_box = px.box(
            df_temp,
            x='Mes_Nombre',
            y='RENDIMIENTO',
            color='Mes_Nombre',
            labels={'RENDIMIENTO': 'Rendimiento (kg/ha)', 'Mes_Nombre': 'Mes de Siembra'},
            category_orders={'Mes_Nombre': ['Octubre', 'Noviembre', 'Diciembre']}
        )
        st.plotly_chart(fig_mes_box, use_container_width=True)

    # Mostrar estadísticas
    st.dataframe(mes_stats, use_container_width=True)

    st.markdown("---")

    # Análisis de ciclo del cultivo
    st.subheader("Análisis de Ciclo del Cultivo (Siembra → Cosecha)")

    df_ciclo = df_filtered[df_filtered['Dias_Ciclo'].notna() & (df_filtered['Dias_Ciclo'] > 0)].copy()

    if not df_ciclo.empty:
        col_ciclo1, col_ciclo2 = st.columns(2)

        with col_ciclo1:
            st.metric("Promedio de Días", f"{df_ciclo['Dias_Ciclo'].mean():.1f}")
            st.metric("Mediana de Días", f"{df_ciclo['Dias_Ciclo'].median():.1f}")

        with col_ciclo2:
            st.metric("Mínimo", f"{df_ciclo['Dias_Ciclo'].min():.0f} días")
            st.metric("Máximo", f"{df_ciclo['Dias_Ciclo'].max():.0f} días")

        # Histograma de días de ciclo
        fig_ciclo = px.histogram(
            df_ciclo,
            x='Dias_Ciclo',
            nbins=30,
            color_discrete_sequence=['#3498DB'],
            labels={'Dias_Ciclo': 'Días de Ciclo', 'count': 'Frecuencia'}
        )
        fig_ciclo.update_layout(height=400)
        st.plotly_chart(fig_ciclo, use_container_width=True)
    else:
        st.info("No hay datos suficientes de ciclo del cultivo en la selección actual.")

# ============================================================================
# PÁGINA 5: RECOMENDADOR INTELIGENTE
# ============================================================================

with tab5:
    st.header("🎯 Recomendador Inteligente de Variedades")

    st.markdown("""
    Selecciona las condiciones de tu siembra y obtén las **Top 5 variedades recomendadas**
    basadas en rendimiento histórico y consistencia.
    """)

    # Inputs del usuario
    col_input1, col_input2, col_input3 = st.columns(3)

    with col_input1:
        localidad_rec = st.selectbox(
            "Localidad:",
            sorted(df['LOCALIDAD'].unique().tolist())
        )

    with col_input2:
        mes_rec = st.selectbox(
            "Mes de Siembra:",
            ['Octubre (10)', 'Noviembre (11)', 'Diciembre (12)']
        )
        mes_rec_num = int(mes_rec.split('(')[1].split(')')[0])

    with col_input3:
        gm_rec = st.selectbox(
            "Grupo de Madurez (opcional):",
            ['Todos'] + sorted(df['GM'].unique().tolist())
        )

    # Botón para generar recomendación
    if st.button("🚀 Generar Recomendación", type="primary"):

        # Filtrar datos según inputs
        df_rec = df[
            (df['LOCALIDAD'] == localidad_rec) &
            (df['Mes_Siembra'] == mes_rec_num)
        ].copy()

        if gm_rec != 'Todos':
            df_rec = df_rec[df_rec['GM'] == gm_rec]

        if df_rec.empty:
            st.warning("No hay datos históricos para esta combinación de localidad, mes y GM. Ampliando búsqueda...")

            # Búsqueda ampliada: solo localidad
            df_rec = df[df['LOCALIDAD'] == localidad_rec].copy()

        if not df_rec.empty:
            # Calcular estadísticas por variedad
            rec_stats = df_rec.groupby('VARIEDAD').agg({
                'RENDIMIENTO': ['count', 'mean', 'std']
            }).reset_index()

            rec_stats.columns = ['Variedad', 'N_Ensayos', 'Rendimiento_Medio', 'Desv_Std']

            # Filtrar variedades con al menos 2 ensayos
            rec_stats = rec_stats[rec_stats['N_Ensayos'] >= 2]

            if not rec_stats.empty:
                # Calcular CV
                rec_stats['CV_%'] = (rec_stats['Desv_Std'] / rec_stats['Rendimiento_Medio'] * 100).round(1)

                # Score ponderado: 70% rendimiento + 30% consistencia (1/CV)
                # Normalizar rendimiento y CV
                rec_stats['Rend_Norm'] = (rec_stats['Rendimiento_Medio'] - rec_stats['Rendimiento_Medio'].min()) / (rec_stats['Rendimiento_Medio'].max() - rec_stats['Rendimiento_Medio'].min())
                rec_stats['Cons_Norm'] = 1 - ((rec_stats['CV_%'] - rec_stats['CV_%'].min()) / (rec_stats['CV_%'].max() - rec_stats['CV_%'].min()))

                rec_stats['Score'] = (0.7 * rec_stats['Rend_Norm']) + (0.3 * rec_stats['Cons_Norm'])

                # Top 5
                top_5 = rec_stats.nlargest(5, 'Score')

                st.success("✅ Recomendación generada exitosamente")

                st.subheader("Top 5 Variedades Recomendadas")

                for i, (idx, row) in enumerate(top_5.iterrows(), 1):
                    with st.expander(f"#{i} - {row['Variedad']} (Score: {row['Score']:.3f})", expanded=(i==1)):
                        col_a, col_b, col_c = st.columns(3)

                        col_a.metric("Rendimiento Esperado", f"{row['Rendimiento_Medio']:.0f} kg/ha")
                        col_b.metric("Consistencia (CV)", f"{row['CV_%']:.1f}%")
                        col_c.metric("N° Ensayos", f"{int(row['N_Ensayos'])}")

                        # Clasificar consistencia
                        if row['CV_%'] < 20:
                            consistencia_label = "🟢 ALTA"
                        elif row['CV_%'] < 25:
                            consistencia_label = "🟡 MEDIA"
                        else:
                            consistencia_label = "🔴 BAJA"

                        st.info(f"**Consistencia:** {consistencia_label}")

                        # Comparación con promedio
                        vs_prom = ((row['Rendimiento_Medio'] / df['RENDIMIENTO'].mean()) - 1) * 100
                        if vs_prom > 0:
                            st.success(f"📈 +{vs_prom:.1f}% por encima del promedio global")
                        else:
                            st.warning(f"📉 {vs_prom:.1f}% por debajo del promedio global")

                # Gráfico comparativo
                st.subheader("Comparación Visual de Top 5")

                fig_top5 = px.bar(
                    top_5,
                    x='Rendimiento_Medio',
                    y='Variedad',
                    orientation='h',
                    color='CV_%',
                    color_continuous_scale='RdYlGn_r',
                    labels={
                        'Rendimiento_Medio': 'Rendimiento Promedio (kg/ha)',
                        'Variedad': 'Variedad',
                        'CV_%': 'CV (%)'
                    },
                    text='Rendimiento_Medio'
                )
                fig_top5.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                st.plotly_chart(fig_top5, use_container_width=True)

            else:
                st.error("No hay suficientes datos para generar recomendación (se requieren al menos 2 ensayos por variedad).")
        else:
            st.error("No hay datos disponibles para esta localidad.")

    # Matriz Heatmap: Localidad x Variedad
    st.markdown("---")
    st.subheader("Matriz de Rendimiento: Localidad x Variedad")

    # Seleccionar top 15 localidades y variedades para el heatmap
    top_localidades_heat = df_filtered.groupby('LOCALIDAD')['RENDIMIENTO'].mean().nlargest(15).index.tolist()
    top_variedades_heat = df_filtered.groupby('VARIEDAD')['RENDIMIENTO'].mean().nlargest(15).index.tolist()

    df_heat = df_filtered[
        (df_filtered['LOCALIDAD'].isin(top_localidades_heat)) &
        (df_filtered['VARIEDAD'].isin(top_variedades_heat))
    ]

    pivot_heat = df_heat.pivot_table(
        values='RENDIMIENTO',
        index='LOCALIDAD',
        columns='VARIEDAD',
        aggfunc='mean'
    )

    fig_heat = px.imshow(
        pivot_heat,
        color_continuous_scale='RdYlGn',
        labels={'color': 'Rendimiento (kg/ha)'},
        aspect='auto'
    )
    fig_heat.update_layout(height=600)
    st.plotly_chart(fig_heat, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption(f"""
**Dashboard PPE RECSO Campaña 2024-25** | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')} |
Desarrollado con Streamlit + Python | Dataset: {len(df):,} ensayos
""")
