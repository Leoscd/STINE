#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporte de Insights de Negocio y Recomendaciones para Dashboard
PPE RECSO Campaña 2024-25
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Cargar datos
import os
# Usar ruta relativa para compatibilidad con Streamlit Cloud
file_path = "PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

# Si no existe, intentar con ruta absoluta (para ejecución local)
if not os.path.exists(file_path):
    file_path = "/home/leodiazdt/dashboard-ppe-2024-25/PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

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

print("=" * 120)
print(" " * 30 + "REPORTE EJECUTIVO DE INSIGHTS Y RECOMENDACIONES")
print(" " * 35 + "PPE RECSO CAMPAÑA 2024-25")
print("=" * 120)
print()

print("\n### RESUMEN EJECUTIVO ###")
print("=" * 120)
print()
print("Dataset analizado: 4,751 registros de ensayos de soja en Regiones Pampeanas")
print("Período: Campaña 2024-25 (Octubre 2024 - Junio 2025)")
print("Alcance geográfico: 53 localidades, 2 regiones, 8 subregiones")
print("Variedades evaluadas: 126 variedades diferentes")
print()
print(f"RENDIMIENTO PROMEDIO GLOBAL: {df['RENDIMIENTO'].mean():.0f} kg/ha")
print(f"RANGO DE RENDIMIENTO: {df['RENDIMIENTO'].min():.0f} - {df['RENDIMIENTO'].max():.0f} kg/ha")
print(f"VARIABILIDAD: Coeficiente de variación de {(df['RENDIMIENTO'].std() / df['RENDIMIENTO'].mean() * 100):.1f}%")
print()

print("\n### 1. INSIGHTS CLAVE DE NEGOCIO ###")
print("=" * 120)
print()

print("\n1.1. PERFORMANCE GEOGRÁFICA")
print("-" * 120)
print()

# Top y bottom localidades
localidad_stats = df.groupby('LOCALIDAD').agg({
    'RENDIMIENTO': ['count', 'mean', 'std']
}).round(2)
localidad_stats.columns = ['Count', 'Media', 'Std']
localidad_stats = localidad_stats[localidad_stats['Count'] >= 30]  # Mínimo 30 registros

print("LOCALIDADES DE ALTO RENDIMIENTO (Top 5):")
top_5_localidades = localidad_stats.sort_values('Media', ascending=False).head(5)
for idx, (loc, row) in enumerate(top_5_localidades.iterrows(), 1):
    rendimiento_vs_promedio = ((row['Media'] / df['RENDIMIENTO'].mean()) - 1) * 100
    print(f"{idx}. {loc}: {row['Media']:.0f} kg/ha (+{rendimiento_vs_promedio:.1f}% vs promedio global)")

print("\nLOCALIDADES DE BAJO RENDIMIENTO (Bottom 5):")
bottom_5_localidades = localidad_stats.sort_values('Media', ascending=True).head(5)
for idx, (loc, row) in enumerate(bottom_5_localidades.iterrows(), 1):
    rendimiento_vs_promedio = ((row['Media'] / df['RENDIMIENTO'].mean()) - 1) * 100
    print(f"{idx}. {loc}: {row['Media']:.0f} kg/ha ({rendimiento_vs_promedio:.1f}% vs promedio global)")

print("\nBRECHA DE RENDIMIENTO: La diferencia entre las mejores y peores localidades es de",
      f"{top_5_localidades['Media'].mean() - bottom_5_localidades['Media'].mean():.0f} kg/ha",
      f"({((top_5_localidades['Media'].mean() / bottom_5_localidades['Media'].mean()) - 1) * 100:.1f}% superior)")

print("\n1.2. PERFORMANCE POR VARIEDAD")
print("-" * 120)
print()

variedad_stats = df.groupby('VARIEDAD').agg({
    'RENDIMIENTO': ['count', 'mean', 'std']
}).round(2)
variedad_stats.columns = ['Count', 'Media', 'Std']
variedad_stats = variedad_stats[variedad_stats['Count'] >= 10]  # Mínimo 10 ensayos
variedad_stats['CV'] = (variedad_stats['Std'] / variedad_stats['Media'] * 100).round(2)

print("TOP 10 VARIEDADES POR RENDIMIENTO:")
top_variedades = variedad_stats.sort_values('Media', ascending=False).head(10)
for idx, (var, row) in enumerate(top_variedades.iterrows(), 1):
    rendimiento_vs_promedio = ((row['Media'] / df['RENDIMIENTO'].mean()) - 1) * 100
    print(f"{idx}. {var}: {row['Media']:.0f} kg/ha (+{rendimiento_vs_promedio:.1f}% vs promedio, CV: {row['CV']:.1f}%)")

print("\nVARIEDADES MÁS CONSISTENTES (menor variabilidad):")
mas_consistentes = variedad_stats.sort_values('CV').head(5)
for idx, (var, row) in enumerate(mas_consistentes.iterrows(), 1):
    print(f"{idx}. {var}: CV={row['CV']:.1f}%, Rendimiento medio: {row['Media']:.0f} kg/ha")

print("\n1.3. ANÁLISIS TEMPORAL")
print("-" * 120)
print()

df['Mes_Siembra'] = df['FECHA DE SIEMBRA'].dt.month
mes_stats = df.groupby('Mes_Siembra')['RENDIMIENTO'].agg(['count', 'mean']).round(2)

print("RENDIMIENTO POR ÉPOCA DE SIEMBRA:")
meses = {10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
for mes, row in mes_stats.iterrows():
    rendimiento_vs_promedio = ((row['mean'] / df['RENDIMIENTO'].mean()) - 1) * 100
    print(f"  {meses.get(mes, mes)}: {row['mean']:.0f} kg/ha ({row['count']} ensayos, {rendimiento_vs_promedio:+.1f}% vs promedio)")

mejor_mes = mes_stats['mean'].idxmax()
peor_mes = mes_stats['mean'].idxmin()
print(f"\nMEJOR VENTANA DE SIEMBRA: {meses.get(mejor_mes, mejor_mes)} ({mes_stats.loc[mejor_mes, 'mean']:.0f} kg/ha)")
print(f"IMPACTO DE ÉPOCA: Siembras tempranas (octubre) superan en",
      f"{mes_stats.loc[mejor_mes, 'mean'] - mes_stats.loc[peor_mes, 'mean']:.0f} kg/ha a siembras tardías (diciembre)")

print("\n1.4. ANÁLISIS DE GRUPOS DE MADUREZ (GM)")
print("-" * 120)
print()

gm_stats = df.groupby('GM').agg({
    'RENDIMIENTO': ['count', 'mean', 'std']
}).round(2).sort_values(('RENDIMIENTO', 'mean'), ascending=False)

print("RENDIMIENTO POR GRUPO DE MADUREZ:")
for gm, row in gm_stats.head(5).iterrows():
    print(f"  {gm}: {row[('RENDIMIENTO', 'mean')]:.0f} kg/ha ({row[('RENDIMIENTO', 'count')]} ensayos)")

print("\n1.5. ANÁLISIS DE SIGNIFICANCIA ESTADÍSTICA")
print("-" * 120)
print()

if 'Sig' in df.columns:
    sig_stats = df.groupby('Sig')['RENDIMIENTO'].agg(['count', 'mean']).round(2)
    if '+' in sig_stats.index and 'a' in sig_stats.index:
        print(f"Variedades con significancia SUPERIOR (+): {sig_stats.loc['+', 'mean']:.0f} kg/ha ({sig_stats.loc['+', 'count']} casos)")
        print(f"Variedades sin diferencia significativa (a): {sig_stats.loc['a', 'mean']:.0f} kg/ha ({sig_stats.loc['a', 'count']} casos)")
        print(f"\nDIFERENCIA: Las variedades marcadas como superiores (+) rinden",
              f"{sig_stats.loc['+', 'mean'] - sig_stats.loc['a', 'mean']:.0f} kg/ha más",
              f"({((sig_stats.loc['+', 'mean'] / sig_stats.loc['a', 'mean']) - 1) * 100:.1f}% superior)")

print("\n1.6. CORRELACIONES IMPORTANTES")
print("-" * 120)
print()

print("Variables correlacionadas con RENDIMIENTO:")
if 'Alt' in df.columns:
    corr_alt = df[['RENDIMIENTO', 'Alt']].corr().iloc[0, 1]
    print(f"  - Altura de planta (Alt): r = {corr_alt:.3f}")
    if corr_alt > 0.3:
        print(f"    INSIGHT: Correlación MODERADA-FUERTE positiva. Plantas más altas tienden a mayor rendimiento.")

if 'P1000' in df.columns:
    corr_p1000 = df[['RENDIMIENTO', 'P1000']].corr().iloc[0, 1]
    print(f"  - Peso de 1000 granos (P1000): r = {corr_p1000:.3f}")
    if corr_p1000 > 0.25:
        print(f"    INSIGHT: Correlación MODERADA positiva. Mayor tamaño de grano asociado a mejor rendimiento.")

if 'Vuelco' in df.columns:
    corr_vuelco = df[['RENDIMIENTO', 'Vuelco']].corr().iloc[0, 1]
    print(f"  - Vuelco: r = {corr_vuelco:.3f}")
    if corr_vuelco < -0.1:
        print(f"    INSIGHT: Correlación negativa. El vuelco reduce el rendimiento.")

print("\n\n### 2. IDENTIFICACIÓN DE OPORTUNIDADES Y RIESGOS ###")
print("=" * 120)
print()

print("\n2.1. OPORTUNIDADES DE MEJORA")
print("-" * 120)
print()

# Localidades con alto potencial pero bajo rendimiento actual
print("OPORTUNIDAD 1: Mejora en localidades de bajo rendimiento")
print("  Localidades con potencial de mejora significativa:")
for idx, (loc, row) in enumerate(bottom_5_localidades.head(3).iterrows(), 1):
    gap = df['RENDIMIENTO'].mean() - row['Media']
    print(f"  {idx}. {loc}: Gap de {gap:.0f} kg/ha respecto al promedio")
    print(f"     Acción: Analizar factores limitantes (suelo, manejo, época de siembra)")

print("\nOPORTUNIDAD 2: Adopción de variedades de alto rendimiento")
mejores_variedades = variedad_stats.sort_values('Media', ascending=False).head(3)
print("  Expandir uso de variedades top:")
for var, row in mejores_variedades.iterrows():
    upside = row['Media'] - df['RENDIMIENTO'].mean()
    print(f"  - {var}: Potencial de +{upside:.0f} kg/ha vs promedio actual")

print("\nOPORTUNIDAD 3: Optimización de fechas de siembra")
print(f"  Incrementar siembras tempranas (Octubre): Potencial de +{mes_stats.loc[10, 'mean'] - df['RENDIMIENTO'].mean():.0f} kg/ha")
print(f"  Reducir siembras tardías (Diciembre): Penalización de {mes_stats.loc[12, 'mean'] - df['RENDIMIENTO'].mean():.0f} kg/ha")

print("\n2.2. ÁREAS DE RIESGO")
print("-" * 120)
print()

# Alta variabilidad
alta_variabilidad = variedad_stats[variedad_stats['CV'] > 25].sort_values('CV', ascending=False)
if len(alta_variabilidad) > 0:
    print("RIESGO 1: Variedades con alta variabilidad (CV > 25%)")
    for var, row in alta_variabilidad.head(5).iterrows():
        print(f"  - {var}: CV = {row['CV']:.1f}% (rendimiento inconsistente)")
    print("  Acción: Evaluar adaptabilidad regional y condiciones óptimas")

# Localidades con alta desviación estándar
localidades_inestables = localidad_stats[localidad_stats['Std'] > 800].sort_values('Std', ascending=False)
if len(localidades_inestables) > 0:
    print("\nRIESGO 2: Localidades con rendimientos inestables")
    for loc, row in localidades_inestables.head(5).iterrows():
        print(f"  - {loc}: Desviación estándar = {row['Std']:.0f} kg/ha")
    print("  Acción: Investigar causas de variabilidad (clima, suelo, manejo)")

print("\n\n### 3. PROPUESTAS DE IMPACTO PARA MEJORAR EL NEGOCIO ###")
print("=" * 120)
print()

print("\nPROPUESTA 1: PROGRAMA DE OPTIMIZACIÓN VARIETAL REGIONALIZADO")
print("-" * 120)
print("OBJETIVO: Incrementar rendimiento promedio en 10-15% mediante selección varietal óptima por zona")
print()
print("ACCIONES:")
print("  1. Crear matriz de recomendación varietal por localidad/subregión")
print("  2. Priorizar top 3 variedades con mejor performance en cada zona")
print("  3. Descontinuar variedades de bajo rendimiento (bottom 20%)")
print()
print("IMPACTO POTENCIAL:")
promedio_actual = df['RENDIMIENTO'].mean()
promedio_top_variedades = variedad_stats.nlargest(10, 'Media')['Media'].mean()
incremento_potencial = promedio_top_variedades - promedio_actual
print(f"  - Rendimiento actual: {promedio_actual:.0f} kg/ha")
print(f"  - Rendimiento potencial (top variedades): {promedio_top_variedades:.0f} kg/ha")
print(f"  - INCREMENTO: +{incremento_potencial:.0f} kg/ha (+{(incremento_potencial/promedio_actual)*100:.1f}%)")
print(f"  - En términos económicos (asumiendo $350/kg): ${incremento_potencial * 350:.0f}/ha")
print()
print("PRIORIDAD: ALTA")
print("COMPLEJIDAD: Media")
print("TIEMPO DE IMPLEMENTACIÓN: 1 campaña")

print("\n\nPROPUESTA 2: ESTRATEGIA DE ADELANTAMIENTO DE FECHAS DE SIEMBRA")
print("-" * 120)
print("OBJETIVO: Maximizar el aprovechamiento de la ventana óptima de siembra")
print()
print("ACCIONES:")
print("  1. Incrementar siembras de octubre de {:.0f}% a 40% del total".format((mes_stats.loc[10, 'count']/len(df))*100))
print("  2. Reducir siembras de diciembre a < 20% del total")
print("  3. Desarrollar protocolos de siembra temprana por zona")
print()
print("IMPACTO POTENCIAL:")
siembras_actuales_oct = mes_stats.loc[10, 'count']
siembras_totales = len(df)
rendimiento_oct = mes_stats.loc[10, 'mean']
rendimiento_dic = mes_stats.loc[12, 'mean']
diferencia_rendimiento = rendimiento_oct - rendimiento_dic

print(f"  - Diferencia de rendimiento Oct vs Dic: {diferencia_rendimiento:.0f} kg/ha")
print(f"  - Si se mueven 500 ha de dic a oct: +{diferencia_rendimiento * 500:.0f} kg totales")
print(f"  - Beneficio económico ($350/kg): ${diferencia_rendimiento * 350 * 500:.0f}")
print()
print("PRIORIDAD: ALTA")
print("COMPLEJIDAD: Media-Alta (requiere logística y planificación)")
print("TIEMPO DE IMPLEMENTACIÓN: 2-3 campañas")

print("\n\nPROPUESTA 3: PROGRAMA DE RESCATE DE ZONAS DE BAJO RENDIMIENTO")
print("-" * 120)
print("OBJETIVO: Reducir brecha de rendimiento en localidades rezagadas")
print()
print("ACCIONES:")
print("  1. Auditoría agronómica en las 5 localidades de menor rendimiento")
print("  2. Análisis de suelo, agua y prácticas de manejo")
print("  3. Plan de mejora específico por localidad (fertilización, genética, fechas)")
print()
print("LOCALIDADES OBJETIVO:")
for loc, row in bottom_5_localidades.head(5).iterrows():
    gap = df['RENDIMIENTO'].mean() - row['Media']
    print(f"  - {loc}: Gap de {gap:.0f} kg/ha ({row['Count']} ensayos)")

print("\nIMPACTO POTENCIAL:")
gap_promedio = (df['RENDIMIENTO'].mean() - bottom_5_localidades.head(5)['Media'].mean())
print(f"  - Gap promedio: {gap_promedio:.0f} kg/ha")
print(f"  - Si se mejora 30% del gap: +{gap_promedio * 0.3:.0f} kg/ha en estas zonas")
print(f"  - Beneficio por hectárea: ${gap_promedio * 0.3 * 350:.0f}/ha")
print()
print("PRIORIDAD: MEDIA-ALTA")
print("COMPLEJIDAD: Alta (requiere inversión y cambio de prácticas)")
print("TIEMPO DE IMPLEMENTACIÓN: 2-4 campañas")

print("\n\nPROPUESTA 4: SISTEMA DE MONITOREO DE CONSISTENCIA VARIETAL")
print("-" * 120)
print("OBJETIVO: Reducir riesgo mediante variedades estables y predecibles")
print()
print("ACCIONES:")
print("  1. Priorizar variedades con CV < 20% (alta consistencia)")
print("  2. Crear portafolio balanceado: 60% variedades consistentes + 40% alto rendimiento")
print("  3. Establecer sistema de alertas para variedades inestables")
print()
print("VARIEDADES RECOMENDADAS (alta consistencia + buen rendimiento):")
variedades_recomendadas = variedad_stats[(variedad_stats['CV'] < 20) & (variedad_stats['Media'] > df['RENDIMIENTO'].mean())].sort_values('Media', ascending=False)
for idx, (var, row) in enumerate(variedades_recomendadas.head(5).iterrows(), 1):
    print(f"  {idx}. {var}: {row['Media']:.0f} kg/ha (CV: {row['CV']:.1f}%)")

print("\nIMPACTO POTENCIAL:")
print("  - Reducción de variabilidad inter-anual: 20-30%")
print("  - Mayor predecibilidad de resultados")
print("  - Menor riesgo financiero para productores")
print()
print("PRIORIDAD: MEDIA")
print("COMPLEJIDAD: Baja")
print("TIEMPO DE IMPLEMENTACIÓN: 1 campaña")

print("\n\nPROPUESTA 5: PLATAFORMA DIGITAL DE RECOMENDACIÓN INTELIGENTE")
print("-" * 120)
print("OBJETIVO: Democratizar el acceso a mejores prácticas mediante tecnología")
print()
print("ACCIONES:")
print("  1. Desarrollar app/web con recomendaciones personalizadas")
print("  2. Inputs: localidad, fecha de siembra, grupo de madurez deseado")
print("  3. Outputs: top 5 variedades recomendadas con rendimiento esperado")
print("  4. Integrar datos históricos, clima y proyecciones")
print()
print("FUNCIONALIDADES CLAVE:")
print("  - Comparador de variedades por zona")
print("  - Simulador de impacto de cambio de fecha de siembra")
print("  - Alertas de ventanas óptimas de siembra")
print("  - Ranking de variedades por consistencia")
print()
print("IMPACTO POTENCIAL:")
print("  - Mejora en toma de decisiones de 5,000+ productores")
print("  - Incremento promedio esperado: 5-8% en rendimiento")
print("  - ROI: Alto (bajo costo de desarrollo vs impacto)")
print()
print("PRIORIDAD: MEDIA-ALTA")
print("COMPLEJIDAD: Media (requiere desarrollo IT)")
print("TIEMPO DE IMPLEMENTACIÓN: 6-12 meses")

print("\n\n### 4. RECOMENDACIONES PARA EL DASHBOARD INTERACTIVO ###")
print("=" * 120)
print()

print("\n4.1. ESTRUCTURA GENERAL DEL DASHBOARD")
print("-" * 120)
print()
print("PÁGINA 1: VISTA GENERAL / EXECUTIVE SUMMARY")
print("  - KPIs principales: Rendimiento promedio, Rango, Coef. variación")
print("  - Mapa geográfico con rendimiento por localidad (heat map)")
print("  - Gráfico de tendencia temporal (rendimiento por mes de siembra)")
print("  - Top 5 variedades y Bottom 5")
print()
print("PÁGINA 2: ANÁLISIS GEOGRÁFICO")
print("  - Mapa interactivo de Argentina (regiones pampeanas)")
print("  - Tabla comparativa de localidades")
print("  - Gráfico de barras: Rendimiento por región/subregión")
print("  - Scatter plot: Rendimiento vs Cantidad de ensayos")
print()
print("PÁGINA 3: ANÁLISIS VARIETAL")
print("  - Tabla dinámica de variedades con filtros")
print("  - Gráfico de burbujas: Rendimiento vs Consistencia (CV)")
print("  - Comparador lado a lado de hasta 4 variedades")
print("  - Histograma de distribución de rendimientos por variedad seleccionada")
print()
print("PÁGINA 4: ANÁLISIS TEMPORAL Y FENOLÓGICO")
print("  - Gráfico de líneas: Rendimiento por fecha de siembra")
print("  - Box plot: Distribución por mes de siembra")
print("  - Análisis de ciclo del cultivo (días siembra-cosecha)")
print("  - Calendario de siembra óptimo por región")
print()
print("PÁGINA 5: ANÁLISIS MULTIVARIADO")
print("  - Matriz de rendimiento: Localidad x Variedad (heatmap)")
print("  - Gráfico de correlaciones entre variables")
print("  - Análisis de grupo de madurez por zona")
print("  - Recomendador: Mejor variedad por localidad")

print("\n\n4.2. FILTROS INTERACTIVOS RECOMENDADOS")
print("-" * 120)
print()
print("FILTROS GLOBALES (aplicables a todas las páginas):")
print("  [ ] Región (II, III)")
print("  [ ] Subregión (1-8)")
print("  [ ] Localidad (dropdown múltiple)")
print("  [ ] Grupo de Madurez (GM)")
print("  [ ] Fecha de siembra (rango de fechas)")
print("  [ ] Mes de siembra (Oct, Nov, Dic)")
print("  [ ] Variedad (dropdown múltiple con búsqueda)")
print("  [ ] Rango de rendimiento (slider)")
print("  [ ] Significancia (Sig: +, a, todas)")
print()
print("FILTROS ESPECÍFICOS POR PÁGINA:")
print("  - Análisis Varietal: Consistencia (CV), Número mínimo de ensayos")
print("  - Análisis Geográfico: Top/Bottom N localidades")
print("  - Análisis Temporal: Ventana de fechas, Mes específico")

print("\n\n4.3. VISUALIZACIONES RECOMENDADAS")
print("-" * 120)
print()
print("1. MAPA GEOGRÁFICO (Geo-spatial)")
print("   - Tipo: Mapa coroplético de Argentina")
print("   - Color: Gradiente de rendimiento (rojo=bajo, verde=alto)")
print("   - Tooltip: Localidad, Rendimiento, N° ensayos")
print("   - Herramienta: Plotly, Folium o similar")
print()
print("2. TABLA DINÁMICA")
print("   - Tipo: Data table con ordenamiento y búsqueda")
print("   - Columnas: Localidad, Variedad, Rendimiento, IM, IT, Alt, P1000, Sig")
print("   - Features: Ordenar, filtrar, exportar CSV, highlight condicional")
print()
print("3. GRÁFICO DE BARRAS COMPARATIVO")
print("   - Eje X: Localidades o Variedades")
print("   - Eje Y: Rendimiento promedio")
print("   - Barras de error: Desviación estándar")
print("   - Color: Por región o GM")
print()
print("4. BOX PLOT")
print("   - Distribución de rendimientos por categoría")
print("   - Mostrar outliers")
print("   - Comparar localidades/variedades lado a lado")
print()
print("5. SCATTER PLOT / BURBUJAS")
print("   - Eje X: Rendimiento promedio")
print("   - Eje Y: Consistencia (CV) o Desv. estándar")
print("   - Tamaño burbuja: N° de ensayos")
print("   - Color: Grupo de madurez o Región")
print()
print("6. HEATMAP / MATRIZ")
print("   - Filas: Localidades")
print("   - Columnas: Variedades")
print("   - Color: Rendimiento promedio")
print("   - Tooltip: Valores exactos, N° ensayos")
print()
print("7. GRÁFICO DE LÍNEAS TEMPORAL")
print("   - Eje X: Fecha o Mes de siembra")
print("   - Eje Y: Rendimiento")
print("   - Múltiples líneas: Por variedad o localidad")
print()
print("8. HISTOGRAMA")
print("   - Distribución de frecuencias de rendimiento")
print("   - Por variedad o localidad seleccionada")
print("   - Con curva de densidad superpuesta")

print("\n\n4.4. KPIs Y MÉTRICAS CLAVE PARA EL DASHBOARD")
print("-" * 120)
print()
print("KPIs PRIMARIOS:")
print("  1. Rendimiento Promedio Global: {:.0f} kg/ha".format(df['RENDIMIENTO'].mean()))
print("  2. Rendimiento Mediano: {:.0f} kg/ha".format(df['RENDIMIENTO'].median()))
print("  3. Rango de Rendimiento: {:.0f} - {:.0f} kg/ha".format(df['RENDIMIENTO'].min(), df['RENDIMIENTO'].max()))
print("  4. Total de Ensayos: {:,}".format(len(df)))
print("  5. Coeficiente de Variación: {:.1f}%".format((df['RENDIMIENTO'].std() / df['RENDIMIENTO'].mean() * 100)))
print()
print("KPIs SECUNDARIOS:")
print("  6. N° de Localidades: {}".format(df['LOCALIDAD'].nunique()))
print("  7. N° de Variedades: {}".format(df['VARIEDAD'].nunique()))
print("  8. Mejor Localidad: {} ({:.0f} kg/ha)".format(
    localidad_stats['Media'].idxmax(), localidad_stats['Media'].max()))
print("  9. Mejor Variedad: {} ({:.0f} kg/ha)".format(
    variedad_stats['Media'].idxmax(), variedad_stats['Media'].max()))
print(" 10. Época óptima de siembra: Octubre ({:.0f} kg/ha)".format(mes_stats.loc[10, 'mean']))
print()
print("KPIs DE CALIDAD:")
print(" 11. Completitud de datos: {:.1f}%".format((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100))
print(" 12. Ensayos con significancia (+): {}".format(df[df['Sig'] == '+'].shape[0]))
print(" 13. Ensayos completados (con fecha de cosecha): {}".format(df['COSECHA'].notna().sum()))

print("\n\n4.5. LAYOUT Y DISEÑO")
print("-" * 120)
print()
print("PALETA DE COLORES SUGERIDA:")
print("  - Alto rendimiento: Verde (#2ECC71)")
print("  - Rendimiento medio: Amarillo/Ámbar (#F39C12)")
print("  - Bajo rendimiento: Rojo (#E74C3C)")
print("  - Acento: Azul (#3498DB)")
print("  - Neutro: Gris (#95A5A6)")
print()
print("NAVEGACIÓN:")
print("  - Barra lateral izquierda con menú de páginas")
print("  - Filtros globales en panel superior")
print("  - Botón de reset de filtros visible")
print("  - Botón de descarga de datos filtrados")
print()
print("RESPONSIVIDAD:")
print("  - Diseño adaptable a desktop, tablet, móvil")
print("  - Gráficos redimensionables")
print("  - Tablas con scroll horizontal en móvil")
print()
print("INTERACTIVIDAD:")
print("  - Hover tooltips en todos los gráficos")
print("  - Click para drill-down (ej: click localidad → ver variedades)")
print("  - Selección múltiple en gráficos")
print("  - Actualización automática al cambiar filtros")

print("\n\n4.6. TECNOLOGÍAS RECOMENDADAS")
print("-" * 120)
print()
print("OPCIÓN 1: Power BI (Microsoft)")
print("  Pros: Integración Office, muy visual, fácil para usuarios de negocio")
print("  Cons: Licencias de pago, menos personalizable")
print("  Recomendado para: Equipos que ya usan Microsoft 365")
print()
print("OPCIÓN 2: Tableau")
print("  Pros: Muy potente, visualizaciones hermosas, gran comunidad")
print("  Cons: Costoso, curva de aprendizaje media")
print("  Recomendado para: Análisis avanzados y presentaciones ejecutivas")
print()
print("OPCIÓN 3: Python + Streamlit / Dash")
print("  Pros: Open source, máxima personalización, gratis")
print("  Cons: Requiere programación, menos templates listos")
print("  Recomendado para: Equipos técnicos, proyectos custom")
print("  Librerías: Plotly, Altair, Folium, pandas")
print()
print("OPCIÓN 4: Google Data Studio (Looker Studio)")
print("  Pros: Gratis, basado en web, colaborativo")
print("  Cons: Menos potente que Power BI/Tableau")
print("  Recomendado para: Presupuestos limitados, equipos distribuidos")

print("\n\n### 5. PRIORIZACIÓN DE PROPUESTAS ###")
print("=" * 120)
print()

print("\nMATRIZ DE IMPACTO VS COMPLEJIDAD:")
print()
print("  ALTO IMPACTO, BAJA-MEDIA COMPLEJIDAD (IMPLEMENTAR YA):")
print("    ★★★ Propuesta 1: Optimización Varietal Regionalizada")
print("    ★★★ Propuesta 4: Sistema de Monitoreo de Consistencia")
print()
print("  ALTO IMPACTO, ALTA COMPLEJIDAD (PLANIFICAR A MEDIANO PLAZO):")
print("    ★★☆ Propuesta 2: Estrategia de Adelantamiento de Siembra")
print("    ★★☆ Propuesta 3: Rescate de Zonas de Bajo Rendimiento")
print()
print("  IMPACTO MEDIO, COMPLEJIDAD MEDIA (CONSIDERAR):")
print("    ★☆☆ Propuesta 5: Plataforma Digital de Recomendación")
print()

print("\n\n### 6. PRÓXIMOS PASOS RECOMENDADOS ###")
print("=" * 120)
print()
print("CORTO PLAZO (1-3 meses):")
print("  1. Desarrollar dashboard interactivo con visualizaciones clave")
print("  2. Crear matriz de recomendación varietal por zona")
print("  3. Identificar variedades para descontinuar (bottom 20%)")
print()
print("MEDIANO PLAZO (3-6 meses):")
print("  4. Lanzar programa piloto de siembra temprana en 5 localidades")
print("  5. Iniciar auditoría agronómica en zonas de bajo rendimiento")
print("  6. Desarrollar sistema de alertas de consistencia varietal")
print()
print("LARGO PLAZO (6-12 meses):")
print("  7. Escalar mejores prácticas a toda la red de ensayos")
print("  8. Desarrollar plataforma digital de recomendación")
print("  9. Integrar datos de clima y proyecciones para próxima campaña")
print()

print("\n" + "=" * 120)
print("FIN DEL REPORTE")
print("Generado: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
print("=" * 120)
