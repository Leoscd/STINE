#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis exhaustivo de datos PPE RECSO Campaña 2024-25
Dashboard Interactivo - Regiones Pampeanas
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de pandas para mejor visualización
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Cargar datos
print("=" * 100)
print("ANÁLISIS EXHAUSTIVO DE DATOS PPE RECSO - CAMPAÑA 2024-25")
print("REGIONES PAMPEANAS")
print("=" * 100)
print()

import os
# Usar ruta relativa para compatibilidad con Streamlit Cloud
file_path = "PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

# Si no existe, intentar con ruta absoluta (para ejecución local)
if not os.path.exists(file_path):
    file_path = "/home/leodiazdt/dashboard-ppe-2024-25/PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"

# Leer CSV con el delimitador correcto (punto y coma)
df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')

print("### 1. EXPLORACIÓN INICIAL DEL DATASET ###")
print("=" * 100)
print()

# Información básica
print(f"Dimensiones del dataset: {df.shape[0]} filas x {df.shape[1]} columnas")
print()

print("Nombres de las columnas:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
print()

print("Primeras 5 filas del dataset:")
print(df.head())
print()

print("Información de tipos de datos:")
print(df.info())
print()

print("Tipos de datos por columna:")
print(df.dtypes)
print()

# Convertir fechas a datetime
fecha_columns = ['FECHA DE SIEMBRA', 'Emergencia', 'COSECHA']
for col in fecha_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')

print("\n### 2. ANÁLISIS DE VALORES ÚNICOS POR COLUMNA ###")
print("=" * 100)
print()

for col in df.columns:
    unique_count = df[col].nunique()
    null_count = df[col].isnull().sum()
    null_pct = (null_count / len(df)) * 100

    print(f"\n{col}:")
    print(f"  - Valores únicos: {unique_count}")
    print(f"  - Valores nulos: {null_count} ({null_pct:.2f}%)")

    if unique_count <= 20:
        print(f"  - Valores: {sorted(df[col].dropna().unique())}")
    else:
        print(f"  - Primeros 10 valores: {sorted(df[col].dropna().unique())[:10]}")

print("\n\n### 3. ANÁLISIS DE CALIDAD DE DATOS ###")
print("=" * 100)
print()

print("Resumen de valores faltantes:")
missing_data = pd.DataFrame({
    'Columna': df.columns,
    'Valores_Nulos': df.isnull().sum(),
    'Porcentaje': (df.isnull().sum() / len(df)) * 100
})
missing_data = missing_data[missing_data['Valores_Nulos'] > 0].sort_values('Valores_Nulos', ascending=False)
print(missing_data)
print()

print("Duplicados en el dataset:")
duplicates = df.duplicated().sum()
print(f"  Total de filas duplicadas: {duplicates}")
print()

print("Filas con todos los valores nulos:")
all_null_rows = df.isnull().all(axis=1).sum()
print(f"  Total: {all_null_rows}")
print()

print("\n### 4. ESTADÍSTICAS DESCRIPTIVAS - VARIABLES NUMÉRICAS ###")
print("=" * 100)
print()

# Identificar columnas numéricas
numeric_columns = ['RENDIMIENTO', 'IM', 'IT', 'Alt', 'Vuelco', 'P1000']

for col in numeric_columns:
    if col in df.columns:
        # Convertir a numérico
        df[col] = pd.to_numeric(df[col], errors='coerce')

        print(f"\n{col}:")
        print(f"  Count: {df[col].count()}")
        print(f"  Media: {df[col].mean():.2f}")
        print(f"  Mediana: {df[col].median():.2f}")
        print(f"  Desviación estándar: {df[col].std():.2f}")
        print(f"  Mínimo: {df[col].min():.2f}")
        print(f"  Máximo: {df[col].max():.2f}")
        print(f"  Q1 (25%): {df[col].quantile(0.25):.2f}")
        print(f"  Q3 (75%): {df[col].quantile(0.75):.2f}")
        print(f"  IQR: {df[col].quantile(0.75) - df[col].quantile(0.25):.2f}")

print("\n\nEstadísticas generales de todas las variables numéricas:")
print(df[numeric_columns].describe())
print()

print("\n### 5. ANÁLISIS DE OUTLIERS ###")
print("=" * 100)
print()

for col in numeric_columns:
    if col in df.columns and df[col].notna().sum() > 0:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]

        print(f"\n{col}:")
        print(f"  Límite inferior: {lower_bound:.2f}")
        print(f"  Límite superior: {upper_bound:.2f}")
        print(f"  Outliers detectados: {len(outliers)}")
        if len(outliers) > 0:
            print(f"  Porcentaje de outliers: {(len(outliers) / df[col].notna().sum()) * 100:.2f}%")

print("\n\n### 6. ANÁLISIS DE DIMENSIONES CATEGÓRICAS ###")
print("=" * 100)
print()

categorical_columns = ['CAMPAÑA', 'GM', 'REGION', 'SUBREGION', 'LOCALIDAD',
                       'CódECR', 'TRAT', 'VARIEDAD', 'CAT', 'Sig']

for col in categorical_columns:
    if col in df.columns:
        print(f"\n{col}:")
        value_counts = df[col].value_counts()
        print(f"  Total de categorías: {len(value_counts)}")
        print(f"  Distribución (top 10):")
        print(value_counts.head(10))

print("\n\n### 7. ANÁLISIS POR LOCALIDAD ###")
print("=" * 100)
print()

if 'LOCALIDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    localidad_stats = df.groupby('LOCALIDAD')['RENDIMIENTO'].agg([
        ('Count', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Std', 'std')
    ]).round(2).sort_values('Media', ascending=False)

    print("Rendimiento por Localidad:")
    print(localidad_stats)
    print()

print("\n### 8. ANÁLISIS POR VARIEDAD ###")
print("=" * 100)
print()

if 'VARIEDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    variedad_stats = df.groupby('VARIEDAD')['RENDIMIENTO'].agg([
        ('Count', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Std', 'std')
    ]).round(2).sort_values('Media', ascending=False)

    print("Rendimiento por Variedad (Top 15):")
    print(variedad_stats.head(15))
    print()

print("\n### 9. ANÁLISIS POR REGIÓN Y SUBREGIÓN ###")
print("=" * 100)
print()

if 'REGION' in df.columns and 'RENDIMIENTO' in df.columns:
    region_stats = df.groupby('REGION')['RENDIMIENTO'].agg([
        ('Count', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2).sort_values('Media', ascending=False)

    print("Rendimiento por Región:")
    print(region_stats)
    print()

if 'SUBREGION' in df.columns and 'RENDIMIENTO' in df.columns:
    subregion_stats = df.groupby('SUBREGION')['RENDIMIENTO'].agg([
        ('Count', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2).sort_values('Media', ascending=False)

    print("Rendimiento por Subregión:")
    print(subregion_stats)
    print()

print("\n### 10. ANÁLISIS DE CORRELACIONES ###")
print("=" * 100)
print()

# Matriz de correlación
numeric_df = df[numeric_columns].select_dtypes(include=[np.number])
if not numeric_df.empty:
    print("Matriz de correlación entre variables numéricas:")
    correlation_matrix = numeric_df.corr()
    print(correlation_matrix)
    print()

    print("\nCorrelaciones más fuertes con RENDIMIENTO:")
    if 'RENDIMIENTO' in correlation_matrix.columns:
        correlations = correlation_matrix['RENDIMIENTO'].sort_values(ascending=False)
        print(correlations)
        print()

print("\n### 11. ANÁLISIS TEMPORAL ###")
print("=" * 100)
print()

if 'FECHA DE SIEMBRA' in df.columns:
    df['Mes_Siembra'] = df['FECHA DE SIEMBRA'].dt.month
    df['Año_Siembra'] = df['FECHA DE SIEMBRA'].dt.year

    print("Distribución de siembras por mes:")
    print(df['Mes_Siembra'].value_counts().sort_index())
    print()

    if 'RENDIMIENTO' in df.columns:
        mes_rendimiento = df.groupby('Mes_Siembra')['RENDIMIENTO'].agg([
            'count', 'mean', 'median'
        ]).round(2)
        print("\nRendimiento promedio por mes de siembra:")
        print(mes_rendimiento)
        print()

if 'COSECHA' in df.columns:
    df['Mes_Cosecha'] = df['COSECHA'].dt.month

    print("Distribución de cosechas por mes:")
    print(df['Mes_Cosecha'].value_counts().sort_index())
    print()

# Calcular días entre siembra y cosecha
if 'FECHA DE SIEMBRA' in df.columns and 'COSECHA' in df.columns:
    df['Dias_Ciclo'] = (df['COSECHA'] - df['FECHA DE SIEMBRA']).dt.days

    print("\nCiclo del cultivo (días entre siembra y cosecha):")
    print(f"  Media: {df['Dias_Ciclo'].mean():.1f} días")
    print(f"  Mediana: {df['Dias_Ciclo'].median():.1f} días")
    print(f"  Mínimo: {df['Dias_Ciclo'].min():.1f} días")
    print(f"  Máximo: {df['Dias_Ciclo'].max():.1f} días")
    print()

print("\n### 12. ANÁLISIS DE SIGNIFICANCIA (Sig) ###")
print("=" * 100)
print()

if 'Sig' in df.columns and 'RENDIMIENTO' in df.columns:
    sig_stats = df.groupby('Sig')['RENDIMIENTO'].agg([
        ('Count', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median')
    ]).round(2)

    print("Rendimiento por nivel de Significancia:")
    print(sig_stats)
    print()

print("\n### 13. ANÁLISIS MULTIVARIADO ###")
print("=" * 100)
print()

# Análisis por LOCALIDAD y VARIEDAD
if 'LOCALIDAD' in df.columns and 'VARIEDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    pivot_table = df.pivot_table(
        values='RENDIMIENTO',
        index='LOCALIDAD',
        columns='VARIEDAD',
        aggfunc='mean'
    ).round(2)

    print("Rendimiento promedio por Localidad y Variedad (primeras 10 localidades y variedades):")
    print(pivot_table.iloc[:10, :10])
    print()

# Top combinaciones
if 'LOCALIDAD' in df.columns and 'VARIEDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    top_combinations = df.groupby(['LOCALIDAD', 'VARIEDAD'])['RENDIMIENTO'].agg([
        'count', 'mean'
    ]).round(2).sort_values('mean', ascending=False).head(20)

    print("\nTop 20 combinaciones Localidad-Variedad con mejor rendimiento:")
    print(top_combinations)
    print()

print("\n### 14. RESUMEN DE MÉTRICAS CLAVE ###")
print("=" * 100)
print()

print(f"Total de registros: {len(df)}")
print(f"Total de localidades: {df['LOCALIDAD'].nunique() if 'LOCALIDAD' in df.columns else 'N/A'}")
print(f"Total de variedades: {df['VARIEDAD'].nunique() if 'VARIEDAD' in df.columns else 'N/A'}")
print(f"Total de regiones: {df['REGION'].nunique() if 'REGION' in df.columns else 'N/A'}")
print(f"Total de subregiones: {df['SUBREGION'].nunique() if 'SUBREGION' in df.columns else 'N/A'}")
print()

if 'RENDIMIENTO' in df.columns:
    print(f"Rendimiento promedio global: {df['RENDIMIENTO'].mean():.2f}")
    print(f"Rendimiento mediano global: {df['RENDIMIENTO'].median():.2f}")
    print(f"Rendimiento mínimo: {df['RENDIMIENTO'].min():.2f}")
    print(f"Rendimiento máximo: {df['RENDIMIENTO'].max():.2f}")
    print(f"Coeficiente de variación: {(df['RENDIMIENTO'].std() / df['RENDIMIENTO'].mean() * 100):.2f}%")
    print()

print("\n### 15. IDENTIFICACIÓN DE MEJORES Y PEORES PERFORMERS ###")
print("=" * 100)
print()

# Mejores localidades
if 'LOCALIDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    print("Top 10 Localidades con mejor rendimiento promedio:")
    top_localidades = df.groupby('LOCALIDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'std']
    }).round(2)
    top_localidades.columns = ['Count', 'Media_Rendimiento', 'Std']
    top_localidades = top_localidades[top_localidades['Count'] >= 5]  # Al menos 5 registros
    print(top_localidades.sort_values('Media_Rendimiento', ascending=False).head(10))
    print()

    print("Bottom 10 Localidades con peor rendimiento promedio:")
    print(top_localidades.sort_values('Media_Rendimiento', ascending=True).head(10))
    print()

# Mejores variedades
if 'VARIEDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    print("Top 10 Variedades con mejor rendimiento promedio:")
    top_variedades = df.groupby('VARIEDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'std']
    }).round(2)
    top_variedades.columns = ['Count', 'Media_Rendimiento', 'Std']
    top_variedades = top_variedades[top_variedades['Count'] >= 5]
    print(top_variedades.sort_values('Media_Rendimiento', ascending=False).head(10))
    print()

print("\n### 16. ANÁLISIS DE CONSISTENCIA ###")
print("=" * 100)
print()

# Variedades más consistentes (menor desviación estándar)
if 'VARIEDAD' in df.columns and 'RENDIMIENTO' in df.columns:
    consistencia = df.groupby('VARIEDAD').agg({
        'RENDIMIENTO': ['count', 'mean', 'std']
    }).round(2)
    consistencia.columns = ['Count', 'Media', 'Std']
    consistencia = consistencia[consistencia['Count'] >= 10]
    consistencia['CV'] = (consistencia['Std'] / consistencia['Media'] * 100).round(2)

    print("Variedades más consistentes (menor coeficiente de variación):")
    print(consistencia.sort_values('CV').head(10))
    print()

print("\n" + "=" * 100)
print("ANÁLISIS COMPLETADO")
print("=" * 100)
