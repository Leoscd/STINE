# 📋 PLANIFICACIÓN DASHBOARD PPE RECSO 2024-25 - MEJORAS AVANZADAS

**Fecha:** 28 de Noviembre de 2025
**Proyecto:** Dashboard Interactivo PPE RECSO Campaña 2024-25
**Objetivo:** Implementar sistema avanzado de recomendación con mapas, clustering y análisis agronómico

---

## 🎯 VISIÓN GENERAL

Transformar el dashboard actual en una herramienta completa de decisión agrónoma que incluya:

- ✅ Mapas interactivos con distribución de variedades y rendimientos
- ✅ Clustering de zonas por rendimiento
- ✅ Rangos de rendimiento máximo/mínimo esperables
- ✅ Gráficos de altura de planta por escenario
- ✅ Recomendaciones de tipo de suelo
- ✅ Sugerencias de trabajos al suelo para máximo rendimiento

---

## 📊 DATOS DISPONIBLES (YA EN EL CSV)

### ✅ Datos que YA tenemos:

```
CAMPAÑA          → Campaña agrícola
GM               → Grupo de Madurez
REGION           → Región (II, III)
SUBREGION        → Subregión (1-5)
LOCALIDAD        → 53 localidades
FECHA DE SIEMBRA → Fecha de siembra
VARIEDAD         → 126 variedades
CAT              → Categoría (mayormente "T")
RENDIMIENTO      → Rendimiento en kg/ha (602-7,545)
Alt              → Altura de planta (39-240 cm, promedio 78.5)
Vuelco           → Resistencia al vuelco
P1000            → Peso de 1000 granos
IM, IT           → Índices de madurez
```

### ❌ Datos que NECESITAMOS conseguir:

```
Coordenadas GPS de localidades (53 localidades)
Tipos de suelo por localidad
Calidad de semillas (categorías y ajuste de rendimiento)
Recomendaciones agronómicas de manejo
Imágenes/iconos para visualizaciones
```

---

## 🗺️ ROADMAP DE IMPLEMENTACIÓN - 4 FASES

### **FASE 1: MEJORAS CON DATOS EXISTENTES** ⏱️ 2-3 horas
**Prioridad:** ⭐⭐⭐ ALTA | **Complejidad:** 🟢 BAJA-MEDIA

#### Objetivos:
1. Crear mapas interactivos de Argentina con rendimientos por localidad
2. Implementar clustering de zonas (K-means con 3-5 clusters)
3. Agregar gráficos comparativos de altura de planta
4. Calcular rangos de rendimiento (percentiles P10-P90)

#### Implementación:

**1.1. Mapa interactivo de rendimientos**
```python
# Usar Plotly Express con scatter_mapbox o scatter_geo
# Colorear localidades por rendimiento promedio
# Agregar tooltip con: Localidad, Rendimiento, N° ensayos
# Selector de variedad para filtrar
```

**1.2. Clustering de rendimientos**
```python
# Algoritmo: K-means con 5 clusters
# Clusters: Muy Alto, Alto, Medio, Bajo, Muy Bajo
# Visualización: Mapa con colores por cluster
# Tabla: Características de cada cluster
```

**1.3. Gráficos de altura de planta**
```python
# Gráfico de barras: Top 10 variedades por altura
# Scatter plot: Altura vs Rendimiento (correlación)
# Histograma: Distribución de alturas
# Comparador: Altura promedio por GM
```

**1.4. Rangos de rendimiento esperado**
```python
# Calcular percentiles P10, P25, P50, P75, P90
# Mostrar: "Rendimiento esperado: 3,500-4,200 kg/ha (80% confianza)"
# Gráfico de caja (boxplot) por variedad
# Identificar outliers y valores extremos
```

#### Archivos a modificar:
- `streamlit_app.py` - Agregar nueva página "🗺️ Mapas y Clustering"
- `requirements.txt` - Agregar: `scikit-learn>=1.3.0`

#### Resultado esperado:
- Nueva página en el dashboard con mapas interactivos
- Clustering automático de zonas productivas
- Visualizaciones de altura vs rendimiento
- Rangos de confianza para recomendaciones

---

### **FASE 2: ENRIQUECIMIENTO CON DATOS EXTERNOS** ⏱️ 4-6 horas
**Prioridad:** ⭐⭐ MEDIA-ALTA | **Complejidad:** 🟡 MEDIA

#### Objetivos:
1. Geocodificar las 53 localidades (LAT, LON)
2. Investigar y clasificar calidades de semilla
3. Obtener datos de suelos por localidad (INTA)
4. Crear archivos lookup con datos adicionales

#### Tareas:

**2.1. Geocodificación de localidades**

Crear archivo: `localidades_gps.csv`
```csv
LOCALIDAD,LATITUD,LONGITUD,PROVINCIA
BERROTARÁN,-32.4442,-63.9661,Córdoba
BOLIVAR,-36.2333,-61.1167,Buenos Aires
...
```

Fuentes:
- Google Maps API (gratis hasta 25,000 requests/mes)
- Nominatim (OpenStreetMap, gratis)
- Manual (buscar en Google Maps)

**2.2. Calidad de semillas**

Crear archivo: `calidad_semilla.csv`
```csv
CATEGORIA,NOMBRE,AJUSTE_RENDIMIENTO_%,DESCRIPCION
F,Fiscalizada,100,Semilla de máxima calidad certificada
C1,Certificada Primera,95,Primera generación certificada
C2,Certificada Segunda,90,Segunda generación certificada
I,Identificada,85,Semilla identificada sin certificar
```

Investigar en:
- INASE (Instituto Nacional de Semillas)
- Asociación de Semilleros Argentinos
- Documentación técnica de empresas semilleras

**2.3. Tipos de suelo por localidad**

Crear archivo: `localidades_suelos.csv`
```csv
LOCALIDAD,TIPO_SUELO,TEXTURA,FERTILIDAD,DRENAJE,REGION_EDAFOLOGICA
BERROTARÁN,Molisol,Franca,Alta,Bueno,Pampa Ondulada
BOLIVAR,Molisol,Franco-limosa,Media-Alta,Moderado,Pampa Deprimida
...
```

Fuentes:
- INTA - Atlas de Suelos de Argentina
- https://inta.gob.ar/suelos
- Cartas de suelos por provincia
- Consulta con ingenieros agrónomos locales

**2.4. Integración al dashboard**

```python
# Cargar archivos adicionales
df_gps = pd.read_csv('localidades_gps.csv')
df_calidad = pd.read_csv('calidad_semilla.csv')
df_suelos = pd.read_csv('localidades_suelos.csv')

# Merge con dataframe principal
df_enriquecido = df.merge(df_gps, on='LOCALIDAD', how='left')
df_enriquecido = df_enriquecido.merge(df_suelos, on='LOCALIDAD', how='left')
```

#### Archivos a crear:
- `localidades_gps.csv` (53 localidades × 4 columnas)
- `calidad_semilla.csv` (4-5 categorías × 4 columnas)
- `localidades_suelos.csv` (53 localidades × 6 columnas)

#### Resultado esperado:
- Mapas con ubicaciones reales de localidades
- Ajuste de rendimientos por calidad de semilla
- Recomendaciones iniciales basadas en tipo de suelo

---

### **FASE 3: RECOMENDACIONES AGRONÓMICAS** ⏱️ 6-8 horas
**Prioridad:** ⭐⭐ MEDIA | **Complejidad:** 🔴 ALTA

#### Objetivos:
1. Crear motor de recomendación de suelos
2. Desarrollar base de conocimiento agronómico
3. Implementar recomendaciones de manejo del suelo
4. Sistema de reglas de decisión multi-criterio

#### Tareas:

**3.1. Motor de recomendación de suelos**

Crear archivo: `suelos_recomendaciones.csv`
```csv
TIPO_SUELO,TEXTURA,APTITUD_SOJA,AJUSTE_RENDIMIENTO_%,RIESGOS,OPORTUNIDADES
Molisol,Franca,Excelente,100,Compactación leve,Máximo potencial
Molisol,Franco-limosa,Muy Buena,95,Drenaje moderado,Alto rendimiento
Vertisol,Arcillosa,Buena,85,Encharcamiento,Requiere manejo
Entisol,Arenosa,Regular,70,Baja retención hídrica,Siembra temprana
```

**3.2. Recomendaciones de manejo**

Crear archivo: `manejo_suelos.csv`
```csv
TIPO_SUELO,TRABAJO,DESCRIPCION,MOMENTO,COSTO_RELATIVO,BENEFICIO_ESPERADO
Molisol Franco,Siembra Directa,Sin labranza conservando rastrojo,Pre-siembra,Bajo,+5-10% rendimiento
Molisol Franco,Fertilización NPK,150N-50P-0K kg/ha,Siembra,Medio,+15-20% rendimiento
Vertisol Arcilloso,Subsolado,Romper capa compactada 40cm,Verano previo,Alto,+10-15% rendimiento
Vertisol Arcilloso,Sistematización,Mejorar drenaje superficial,Una vez,Muy Alto,+20-30% rendimiento
Entisol Arenoso,Cultivo cobertura,Vicia/centeno para materia orgánica,Invierno previo,Bajo,+8-12% rendimiento
```

**3.3. Base de conocimiento - Reglas de decisión**

Crear archivo: `reglas_agronomicas.py`
```python
def recomendar_suelo_variedad(tipo_suelo, gm, fecha_siembra, rendimiento_objetivo):
    """
    Motor de recomendación basado en reglas
    """
    recomendaciones = []

    # Regla 1: Suelo franco + siembra temprana
    if tipo_suelo == 'Franco' and fecha_siembra.month == 10:
        recomendaciones.append({
            'tipo': 'EXCELENTE',
            'mensaje': 'Combinación óptima: suelo franco + siembra octubre',
            'rendimiento_esperado': (4500, 5200),
            'confianza': 'ALTA'
        })

    # Regla 2: Suelo arcilloso + siembra tardía
    elif tipo_suelo == 'Arcilloso' and fecha_siembra.month >= 12:
        recomendaciones.append({
            'tipo': 'PRECAUCIÓN',
            'mensaje': 'Riesgo de encharcamiento en siembra tardía',
            'rendimiento_esperado': (3000, 3800),
            'confianza': 'MEDIA',
            'accion': 'Considerar sistematización o variedades tolerantes'
        })

    # ... más reglas

    return recomendaciones
```

**3.4. Integración al dashboard - Nueva página "🎯 Recomendador Avanzado"**

```python
# Inputs del usuario
col1, col2, col3, col4 = st.columns(4)

localidad = col1.selectbox("Localidad", localidades)
variedad = col2.selectbox("Variedad", variedades)
fecha_siembra = col3.date_input("Fecha de Siembra")
rendimiento_obj = col4.number_input("Rendimiento Objetivo (kg/ha)", min_value=2000, max_value=7000, value=4000)

if st.button("🚀 Generar Recomendación Completa"):
    # Obtener tipo de suelo de la localidad
    tipo_suelo = df_suelos[df_suelos['LOCALIDAD']==localidad]['TIPO_SUELO'].values[0]

    # Ejecutar motor de recomendación
    recomendaciones = recomendar_suelo_variedad(tipo_suelo, gm, fecha_siembra, rendimiento_obj)

    # Mostrar resultados
    st.success(f"✅ Recomendación generada para {localidad}")

    # KPIs
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Tipo de Suelo", tipo_suelo)
    col_b.metric("Rendimiento Esperado", f"{recomendaciones[0]['rendimiento_esperado'][0]}-{recomendaciones[0]['rendimiento_esperado'][1]} kg/ha")
    col_c.metric("Nivel de Confianza", recomendaciones[0]['confianza'])

    # Recomendaciones específicas
    st.subheader("📋 Recomendaciones de Manejo")
    trabajos = df_manejo[df_manejo['TIPO_SUELO']==tipo_suelo]
    for idx, trabajo in trabajos.iterrows():
        with st.expander(f"{trabajo['TRABAJO']} - Beneficio: {trabajo['BENEFICIO_ESPERADO']}"):
            st.write(f"**Descripción:** {trabajo['DESCRIPCION']}")
            st.write(f"**Momento:** {trabajo['MOMENTO']}")
            st.write(f"**Costo Relativo:** {trabajo['COSTO_RELATIVO']}")
```

#### Archivos a crear:
- `suelos_recomendaciones.csv`
- `manejo_suelos.csv`
- `reglas_agronomicas.py`

#### Resultado esperado:
- Recomendaciones personalizadas de suelo por localidad
- Sugerencias específicas de trabajos al suelo
- Estimación de costos y beneficios
- Motor de reglas agronómicas funcional

---

### **FASE 4: VISUALIZACIONES AVANZADAS** ⏱️ 3-4 horas
**Prioridad:** ⭐ MEDIA-BAJA | **Complejidad:** 🟡 MEDIA

#### Objetivos:
1. Crear visualizaciones de altura de planta
2. Agregar iconografía y símbolos
3. Implementar simulador de escenarios
4. Comparador lado a lado

#### Tareas:

**4.1. Gráficos de siluetas de plantas**

Crear función para generar imágenes:
```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generar_silueta_planta(altura_cm, rendimiento):
    """
    Genera imagen de silueta de planta soja con altura proporcional
    """
    fig, ax = plt.subplots(figsize=(3, 6))

    # Tallo (línea vertical)
    ax.plot([0.5, 0.5], [0, altura_cm], color='green', linewidth=3)

    # Hojas (óvalos)
    n_hojas = int(altura_cm / 10)
    for i in range(n_hojas):
        y = (i+1) * 10
        # Hoja izquierda
        ax.add_patch(patches.Ellipse((0.3, y), 0.3, 0.8, color='darkgreen'))
        # Hoja derecha
        ax.add_patch(patches.Ellipse((0.7, y), 0.3, 0.8, color='darkgreen'))

    # Vainas (rectángulos en la parte superior)
    if rendimiento > 4000:
        n_vainas = 15
    elif rendimiento > 3500:
        n_vainas = 10
    else:
        n_vainas = 5

    for i in range(n_vainas):
        y = altura_cm - (i * 3)
        ax.add_patch(patches.Rectangle((0.4, y), 0.2, 0.5, color='brown'))

    # Configuración
    ax.set_xlim(0, 1)
    ax.set_ylim(0, altura_cm + 10)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.title(f"Altura: {altura_cm} cm\nRendimiento: {rendimiento} kg/ha", fontsize=10)

    return fig
```

**4.2. Iconografía**

Crear diccionario de íconos:
```python
ICONOS_SUELO = {
    'Franco': '🌾',
    'Arcilloso': '🧱',
    'Arenoso': '🏜️',
    'Limoso': '💧'
}

ICONOS_CALIDAD = {
    'Fiscalizada': '⭐⭐⭐',
    'Certificada Primera': '⭐⭐',
    'Certificada Segunda': '⭐',
    'Identificada': '○'
}

ICONOS_RIESGO = {
    'BAJO': '🟢',
    'MEDIO': '🟡',
    'ALTO': '🔴'
}
```

**4.3. Simulador de escenarios**

```python
st.header("🎮 Simulador de Escenarios")

# Escenario base
col_base, col_sim = st.columns(2)

with col_base:
    st.subheader("📊 Escenario Base")
    loc_base = st.selectbox("Localidad Base", localidades, key='base')
    var_base = st.selectbox("Variedad Base", variedades, key='var_base')
    fecha_base = st.date_input("Fecha Base", key='fecha_base')

with col_sim:
    st.subheader("🔄 Escenario Alternativo")
    loc_sim = st.selectbox("Localidad Alternativa", localidades, key='sim')
    var_sim = st.selectbox("Variedad Alternativa", variedades, key='var_sim')
    fecha_sim = st.date_input("Fecha Alternativa", key='fecha_sim')

if st.button("⚖️ Comparar Escenarios"):
    # Calcular rendimientos esperados
    rend_base = calcular_rendimiento_esperado(loc_base, var_base, fecha_base)
    rend_sim = calcular_rendimiento_esperado(loc_sim, var_sim, fecha_sim)

    # Comparación visual
    col_res1, col_res2, col_res3 = st.columns(3)

    col_res1.metric("Escenario Base", f"{rend_base[1]:.0f} kg/ha")
    col_res2.metric("Escenario Alternativo", f"{rend_sim[1]:.0f} kg/ha",
                    delta=f"{rend_sim[1]-rend_base[1]:.0f} kg/ha")
    col_res3.metric("Diferencia %", f"{((rend_sim[1]/rend_base[1])-1)*100:.1f}%")

    # Gráfico comparativo
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Base', x=['Mínimo', 'Esperado', 'Máximo'],
                         y=[rend_base[0], rend_base[1], rend_base[2]]))
    fig.add_trace(go.Bar(name='Alternativo', x=['Mínimo', 'Esperado', 'Máximo'],
                         y=[rend_sim[0], rend_sim[1], rend_sim[2]]))
    st.plotly_chart(fig)
```

**4.4. Comparador lado a lado**

```python
# Layout de comparación
tab_comp1, tab_comp2, tab_comp3 = st.tabs(["📊 Rendimientos", "🌱 Características", "💰 Económico"])

with tab_comp1:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Escenario Base")
        # Gráficos del escenario base

    with col_right:
        st.markdown("### Escenario Alternativo")
        # Gráficos del escenario alternativo

# Similar para otras tabs
```

#### Archivos a crear:
- `utils_visualizaciones.py` - Funciones de gráficos
- `/assets/iconos/` - Carpeta con imágenes (opcional)

#### Resultado esperado:
- Visualizaciones dinámicas de altura de planta
- Interfaz rica con iconos y símbolos
- Simulador interactivo de escenarios
- Comparaciones lado a lado

---

## 🛠️ DEPENDENCIAS ADICIONALES

### requirements.txt actualizado:
```txt
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
python-dateutil>=2.8.0
scikit-learn>=1.3.0          # NUEVO - Para clustering
folium>=0.14.0                # NUEVO - Mapas alternativos (opcional)
streamlit-folium>=0.15.0      # NUEVO - Integración folium
matplotlib>=3.7.0             # NUEVO - Gráficos de siluetas
pillow>=10.0.0                # NUEVO - Manipulación de imágenes
```

---

## 📁 ESTRUCTURA DE ARCHIVOS FINAL

```
dashboard-ppe-2024-25/
├── streamlit_app.py                    # Dashboard principal (modificado)
├── dashboard_streamlit_base.py         # Backup original
├── requirements.txt                    # Dependencias actualizadas
├── claude.md                           # Este documento
├── README.md
├── REPORTE_COMPLETO_ANALISIS.md
├── RESUMEN_EJECUTIVO.md
│
├── data/                               # NUEVA CARPETA - Datos
│   ├── PPE RECSO CAMPAÑA 2024-25 Regiones Pampeanas 2.csv
│   ├── localidades_gps.csv            # NUEVO - Fase 2
│   ├── calidad_semilla.csv            # NUEVO - Fase 2
│   ├── localidades_suelos.csv         # NUEVO - Fase 2
│   ├── suelos_recomendaciones.csv     # NUEVO - Fase 3
│   └── manejo_suelos.csv              # NUEVO - Fase 3
│
├── utils/                              # NUEVA CARPETA - Utilidades
│   ├── reglas_agronomicas.py          # NUEVO - Fase 3
│   ├── utils_visualizaciones.py       # NUEVO - Fase 4
│   └── clustering.py                  # NUEVO - Fase 1
│
├── assets/                             # NUEVA CARPETA - Imágenes/iconos
│   ├── iconos/
│   │   ├── suelo_franco.png
│   │   ├── suelo_arcilloso.png
│   │   └── suelo_arenoso.png
│   └── logos/
│       └── ppe_logo.png
│
└── .streamlit/
    └── config.toml
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### FASE 1: Datos Existentes (2-3 horas)
- [ ] Agregar scikit-learn a requirements.txt
- [ ] Implementar clustering K-means en nueva página
- [ ] Crear mapas interactivos con Plotly
- [ ] Agregar gráficos de altura de planta
- [ ] Calcular rangos de rendimiento (P10-P90)
- [ ] Agregar nueva página "🗺️ Mapas y Clustering"
- [ ] Probar localmente
- [ ] Deploy a Streamlit Cloud
- [ ] Verificar funcionamiento en producción

### FASE 2: Enriquecimiento (4-6 horas)
- [ ] Geocodificar 53 localidades (crear localidades_gps.csv)
- [ ] Investigar categorías de calidad semilla (crear calidad_semilla.csv)
- [ ] Consultar datos INTA de suelos (crear localidades_suelos.csv)
- [ ] Integrar archivos CSV al dashboard
- [ ] Actualizar mapas con coordenadas GPS reales
- [ ] Agregar filtros por tipo de suelo
- [ ] Probar localmente
- [ ] Subir archivos CSV al repositorio
- [ ] Deploy a Streamlit Cloud
- [ ] Verificar funcionamiento en producción

### FASE 3: Recomendaciones (6-8 horas)
- [ ] Crear suelos_recomendaciones.csv
- [ ] Crear manejo_suelos.csv
- [ ] Desarrollar reglas_agronomicas.py
- [ ] Implementar motor de recomendación
- [ ] Crear nueva página "🎯 Recomendador Avanzado"
- [ ] Integrar recomendaciones de manejo
- [ ] Agregar cálculo de costos/beneficios
- [ ] Probar escenarios diversos
- [ ] Deploy a Streamlit Cloud
- [ ] Verificar funcionamiento en producción

### FASE 4: Visualizaciones (3-4 horas)
- [ ] Crear utils_visualizaciones.py
- [ ] Implementar función generar_silueta_planta()
- [ ] Agregar iconografía (emojis o imágenes)
- [ ] Crear simulador de escenarios
- [ ] Implementar comparador lado a lado
- [ ] Diseñar layout responsive
- [ ] Probar en diferentes resoluciones
- [ ] Deploy a Streamlit Cloud
- [ ] Verificar funcionamiento en producción

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

### Para continuar por la tarde:

1. **Revisar este documento** y familiarizarse con el plan
2. **Decidir qué fase empezar** (recomiendo FASE 1)
3. **Preparar entorno:**
   ```bash
   cd ~/dashboard-ppe-2024-25
   # Verificar que todo esté actualizado
   git pull origin main
   ```
4. **Instalar dependencias adicionales:**
   ```bash
   pip install scikit-learn matplotlib
   ```
5. **Comenzar implementación** de la fase elegida

---

## 📞 CONTACTO Y SOPORTE

- **Repositorio GitHub:** https://github.com/Leoscd/STINE
- **Dashboard en producción:** https://rfcbthquch3uyt7hq3zs4f.streamlit.app/
- **Archivos locales:** `/home/leodiazdt/dashboard-ppe-2024-25/`

---

## 💡 NOTAS IMPORTANTES

### Compatibilidad Streamlit Cloud:
- ✅ Todo es compatible y funcionará correctamente
- ✅ Límite de memoria: 1GB (suficiente)
- ✅ Archivos estáticos: Sin límite
- ⚠️ Evitar procesamiento muy pesado (> 30 segundos)

### Mejores Prácticas:
- Usar `@st.cache_data` para funciones de carga de datos
- Optimizar imágenes (< 500KB cada una)
- Mantener archivos CSV limpios y bien documentados
- Comentar código complejo
- Hacer commits frecuentes al repositorio

### Recursos Útiles:
- **INTA Suelos:** https://inta.gob.ar/suelos
- **INASE:** https://www.inase.gob.ar/
- **Plotly Maps:** https://plotly.com/python/maps/
- **Streamlit Docs:** https://docs.streamlit.io/
- **scikit-learn Clustering:** https://scikit-learn.org/stable/modules/clustering.html

---

**Documento creado:** 28/11/2025
**Última actualización:** 28/11/2025
**Versión:** 1.0

🌾 Generated with Claude Code
