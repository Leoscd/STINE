# Dashboard PPE RECSO - Campaña 2024-25
## Análisis Interactivo de Ensayos de Soja - Regiones Pampeanas

---

## Contenido del Proyecto

Este proyecto contiene un análisis exhaustivo del dataset PPE RECSO Campaña 2024-25 y los archivos necesarios para implementar un dashboard interactivo.

### Archivos Generados

#### 1. Documentación y Reportes

- **`REPORTE_COMPLETO_ANALISIS.md`** (PRINCIPAL)
  - Análisis exhaustivo de 4,751 ensayos
  - Estadísticas descriptivas completas
  - Insights de negocio y oportunidades
  - 5 propuestas de impacto con ROI calculado
  - Recomendaciones detalladas para el dashboard
  - Roadmap de implementación

- **`RESUMEN_EJECUTIVO.md`**
  - Versión resumida ejecutiva del análisis
  - Top hallazgos y métricas clave
  - Tabla comparativa de mejores/peores localidades y variedades
  - Propuestas priorizadas
  - Próximos pasos inmediatos

#### 2. Resultados de Análisis

- **`analisis_resultado.txt`**
  - Output completo del análisis estadístico
  - Estadísticas descriptivas por variable
  - Análisis de calidad de datos
  - Correlaciones y outliers
  - Análisis multivariado

- **`reporte_insights.txt`**
  - Insights de negocio detallados
  - Performance geográfica y varietal
  - Análisis temporal
  - Oportunidades y riesgos identificados
  - Recomendaciones para dashboard

#### 3. Scripts Python

- **`analisis_completo.py`**
  - Script para análisis estadístico exhaustivo
  - Genera `analisis_resultado.txt`
  - Incluye todas las métricas y estadísticas

- **`reporte_insights_dashboard.py`**
  - Script para generar insights de negocio
  - Genera `reporte_insights.txt`
  - Incluye propuestas y recomendaciones

- **`dashboard_streamlit_base.py`** (DASHBOARD INTERACTIVO)
  - Código base completo del dashboard en Streamlit
  - 5 páginas funcionales
  - Filtros globales interactivos
  - Recomendador inteligente de variedades
  - Listo para ejecutar

#### 4. Dataset Original

- **`PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv`**
  - Dataset original con 4,751 registros
  - 19 columnas de datos
  - Formato: CSV con separador punto y coma (;)

---

## Resumen de Hallazgos Principales

### Métricas Globales
- **Total de ensayos:** 4,751
- **Localidades:** 53
- **Variedades:** 126
- **Rendimiento promedio:** 3,958 kg/ha
- **Rango:** 602 - 7,545 kg/ha
- **Coeficiente de variación:** 29.4%

### Top 5 Insights

1. **Brecha Geográfica:** 3,920 kg/ha de diferencia entre mejores y peores zonas
2. **Impacto de Fecha de Siembra:** Octubre rinde 682 kg/ha más que diciembre
3. **Optimización Varietal:** Top variedades rinden 10-15% sobre promedio
4. **Correlación Altura-Rendimiento:** r = 0.391 (moderada-fuerte)
5. **Alta Variabilidad:** CV = 29.4% indica oportunidad de homogeneización

### Mejores Performers

**Top 5 Localidades:**
1. BOLIVAR: 6,096 kg/ha (+54.0%)
2. CHACABUCO: 5,832 kg/ha (+47.4%)
3. VICTORIA: 5,408 kg/ha (+36.6%)
4. CHALACEA: 5,374 kg/ha (+35.8%)
5. RAFAELA: 5,186 kg/ha (+31.0%)

**Top 5 Variedades:**
1. CZ 6423 SE: 4,555 kg/ha (CV: 17.3%)
2. BRV6424SCE: 4,532 kg/ha (CV: 20.3%)
3. NEO 70S25 CE: 4,422 kg/ha (CV: 21.6%)
4. 67K67RSF SCE: 4,379 kg/ha (CV: 18.3%)
5. 66MS01: 4,372 kg/ha (CV: 16.6%)

---

## Cómo Usar el Dashboard Interactivo

### Requisitos Previos

```bash
# Python 3.8 o superior
python --version

# Pip (gestor de paquetes)
pip --version
```

### Instalación

1. **Instalar dependencias:**

```bash
pip install streamlit pandas numpy plotly
```

O usando el archivo requirements.txt (crear uno):

```bash
# Crear requirements.txt con:
echo "streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0" > requirements.txt

# Instalar
pip install -r requirements.txt
```

2. **Verificar que el dataset está en la ubicación correcta:**

```bash
ls "/home/leodiazdt/dashboard-ppe-2024-25/PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"
```

### Ejecución del Dashboard

1. **Navegar al directorio:**

```bash
cd /home/leodiazdt/dashboard-ppe-2024-25
```

2. **Ejecutar Streamlit:**

```bash
streamlit run dashboard_streamlit_base.py
```

3. **Abrir en navegador:**

El dashboard se abrirá automáticamente en `http://localhost:8501`

Si no se abre automáticamente, copia y pega la URL en tu navegador.

### Uso del Dashboard

#### Página 1: Vista General
- Visualiza KPIs principales (rendimiento promedio, total ensayos, etc.)
- Explora top localidades y variedades
- Revisa distribución de rendimientos

#### Página 2: Análisis Geográfico
- Tabla comparativa de todas las localidades
- Gráficos por región y subregión
- Scatter plot: rendimiento vs cantidad de ensayos

#### Página 3: Análisis Varietal
- Tabla de variedades con métricas de rendimiento y consistencia
- Gráfico de burbujas: rendimiento vs CV
- Comparador lado a lado de hasta 4 variedades

#### Página 4: Análisis Temporal
- Rendimiento por mes de siembra (Octubre, Noviembre, Diciembre)
- Box plots comparativos por mes
- Análisis de días de ciclo del cultivo

#### Página 5: Recomendador Inteligente
- **Input:** Selecciona localidad, mes de siembra, grupo de madurez
- **Output:** Top 5 variedades recomendadas con rendimiento esperado
- Matriz heatmap: localidad x variedad

#### Filtros Globales (Sidebar)

Todos los filtros afectan a todas las páginas simultáneamente:
- Región
- Subregión
- Localidad
- Variedad
- Mes de siembra
- Rango de rendimiento (slider)

**Botón "Reset Filtros"** para volver al estado original.

---

## Propuestas de Impacto (Resumen)

### PROPUESTA 1: Optimización Varietal Regionalizada
- **Impacto:** +403 kg/ha (+10.2%)
- **Beneficio:** $141,000/ha
- **Prioridad:** ALTA | Plazo: 1 campaña

### PROPUESTA 2: Adelantamiento de Fechas de Siembra
- **Impacto:** +682 kg/ha
- **Beneficio:** $238,700/ha
- **Prioridad:** ALTA | Plazo: 2-3 campañas

### PROPUESTA 3: Rescate de Zonas de Bajo Rendimiento
- **Impacto:** +690 kg/ha en 5 localidades críticas
- **Beneficio:** $241,372/ha
- **Prioridad:** MEDIA-ALTA | Plazo: 2-4 campañas

### PROPUESTA 4: Monitoreo de Consistencia Varietal
- **Impacto:** Reducción 20-30% de variabilidad
- **Prioridad:** MEDIA | Plazo: 1 campaña

### PROPUESTA 5: Plataforma Digital de Recomendación
- **Impacto:** +5-8% rendimiento promedio
- **Prioridad:** MEDIA-ALTA | Plazo: 6-12 meses

**ROI Esperado:** 965% - 2,545% en 1-2 campañas

---

## Próximos Pasos Recomendados

### Corto Plazo (1-3 meses)
1. Validar análisis con equipo técnico
2. Implementar dashboard (usar `dashboard_streamlit_base.py`)
3. Crear matriz de recomendación varietal por zona

### Mediano Plazo (3-6 meses)
4. Lanzar programa piloto de siembra temprana
5. Auditoría agronómica en zonas rezagadas
6. Sistema de alertas de consistencia varietal

### Largo Plazo (6-12 meses)
7. Escalar mejores prácticas
8. Desarrollar plataforma digital avanzada
9. Integrar datos de clima y modelos predictivos

---

## Personalización del Dashboard

### Modificar Filtros

Editar `dashboard_streamlit_base.py` en la sección "SIDEBAR - FILTROS GLOBALES" (línea ~70):

```python
# Agregar nuevo filtro
nuevo_filtro = st.sidebar.selectbox("Nuevo Filtro", opciones)
```

### Agregar Nueva Página

```python
# En la definición de tabs (línea ~250)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Vista General",
    "🗺️ Análisis Geográfico",
    "🧬 Análisis Varietal",
    "📅 Análisis Temporal",
    "🎯 Recomendador",
    "📈 Nueva Página"  # NUEVA
])

# Luego agregar contenido
with tab6:
    st.header("Nueva Página")
    # ... tu código aquí
```

### Cambiar Colores

Buscar en el código la paleta de colores (líneas ~320, ~410, etc.):

```python
color_continuous_scale='RdYlGn'  # Rojo-Amarillo-Verde
# Cambiar por:
color_continuous_scale='Viridis'  # u otras: 'Blues', 'Reds', 'Greens'
```

### Agregar Nuevas Visualizaciones

```python
# Ejemplo: agregar gráfico de dispersión
import plotly.express as px

fig = px.scatter(
    df_filtered,
    x='Alt',
    y='RENDIMIENTO',
    color='VARIEDAD',
    trendline='ols'
)
st.plotly_chart(fig, use_container_width=True)
```

---

## Deploy en la Nube (Opcional)

### Opción 1: Streamlit Cloud (GRATUITO)

1. Subir proyecto a GitHub
2. Ir a https://share.streamlit.io
3. Conectar repositorio GitHub
4. Deploy automático

### Opción 2: Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create nombre-dashboard-ppe

# Deploy
git push heroku main
```

### Opción 3: AWS / Google Cloud

Consultar documentación de Streamlit para deploy en:
- AWS EC2
- Google Cloud Run
- Azure App Service

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Error: "File not found" al cargar CSV

Verificar ruta del archivo en `dashboard_streamlit_base.py` línea ~45:

```python
file_path = "/home/leodiazdt/dashboard-ppe-2024-25/PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv"
```

Cambiar por la ruta correcta de tu sistema.

### Dashboard muy lento

- Reducir cantidad de datos mostrados en tablas (usar paginación)
- Agregar más `@st.cache_data` decorators
- Filtrar datos antes de graficar

### Gráficos no se ven correctamente

- Actualizar Plotly: `pip install --upgrade plotly`
- Verificar versión de navegador (usar Chrome/Firefox actualizado)

---

## Contacto y Soporte

Para preguntas técnicas sobre el dashboard:
- Revisar documentación de Streamlit: https://docs.streamlit.io
- Revisar documentación de Plotly: https://plotly.com/python/

Para preguntas sobre el análisis:
- Consultar `REPORTE_COMPLETO_ANALISIS.md`
- Consultar `RESUMEN_EJECUTIVO.md`

---

## Licencia

Este proyecto es de uso interno para análisis de datos PPE RECSO.

---

## Changelog

**Versión 1.0 (2025-11-28)**
- Análisis inicial completo de 4,751 ensayos
- 5 propuestas de impacto identificadas
- Dashboard interactivo con 5 páginas funcionales
- Recomendador inteligente de variedades
- Documentación completa

---

**Generado el:** 2025-11-28
**Analista:** Claude (Anthropic)
**Dataset:** PPE RECSO Campaña 2024-25 - Regiones Pampeanas
