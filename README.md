# Explorex DIG (Dynamic Information Grounding)
## Microscopio Informacional v1.0

> *Arrastra cualquier señal. DIG observa sin etiquetas.*

**Explorex DIG** es un microscopio informacional diseñado para analizar series temporales complejas mediante un proceso de *Dynamic Information Grounding* (Cimentación Dinámica de la Información). A diferencia de los modelos supervisados tradicionales que requieren grandes cantidades de datos etiquetados, DIG funciona observando la señal subyacente e identificando atractores informacionales y estructuras emergentes de manera autónoma, aplicando conceptos como el "período crítico" (bootstrap), el "olvido ortogonal" y fases de "sueño/consolidación".

Este repositorio contiene la versión estable **v1.0** y todas las herramientas de comando (CLI) y ventanas (GUI) necesarias para explorar conjuntos de datos de diversa índole, como ondas gravitacionales (LIGO), radiotelescopios (SETI), electroencefalogramas, audios complejos y más.

---

## 🚀 Inicio Rápido e Instalación

Para utilizar el sistema de forma local:

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/saxonaique/explorer-dig.git
   cd explorer-dig
   ```

2. **Instala las dependencias necesarias:**
   Se recomienda usar un entorno virtual o Anaconda (Python 3.8+).
   ```bash
   cd DIG_Explorer_v1
   pip install -r requirements.txt
   ```

3. **Ejecuta la Demostración:**
   Evalúa el funcionamiento de la red localmente en cuestión de segundos:
   ```bash
   python run_demo.py
   ```
   También puedes lanzar la Interfaz Gráfica (GUI):
   ```bash
   python gui_dig.py
   ```

---

## 🔍 Uso del Explorador en Terminal (`dig_explorer.py`)

Dentro de la subcarpeta `DIG_Explorer_v1`, tienes acceso directo al explorador de terminal, con la capacidad de leer casi cualquier formato en una sola línea:

```bash
# Analizar señal de audio (.wav - frecuencia detectada automáticamente)
python dig_explorer.py mi_grabacion.wav

# Serie temporal CSV (.csv - indicando frecuencia a 1000 Hz)
python dig_explorer.py datos.csv --fs 1000

# Archivo de Numpy puro (.npy)
python dig_explorer.py eeg_sujeto01.npy --fs 256 --label "sujeto_01"

# Datos de texto listado (Ej. radioastronomía)
python dig_explorer.py canal_celebes.txt --fs 250000 --label "BL_sgr"

# Elegir específicamente la columna de un CSV y el directorio de salida
python dig_explorer.py multicanal.csv --col 2 --fs 500 --out resultados/
```

### ¿Qué produce el Analyzer?
Cada ejecución genera automáticamente un set de resultados en tu carpeta de salidas (ej. `/salidas`):
- `dig_explore_<etiqueta>_<fecha>.png`: Representación visual integral con el template adquirido, la serie en el tiempo, y su distribución estadística.
- `dig_diary.jsonl`: Un registro JSONL acumulativo que opera a modo de "Diario" (Diary) de tus pruebas.
- **Reporte completo en el Terminal:** Un output comprensivo mostrando métricas matemáticas (ESI, SP, KS) evaluando si lo observado es un "Atractor Fuerte", "Estructura Débil", "Ruido", etc.

---

## 🧬 Arquitectura e Interpretación Matemáticas

El ciclo mental del módulo motor **dig_core_v1** fluye de la siguiente manera:
1. `señal → STFT → log-mags → escalar a 16x16 → normalizar`
2. **Bootstrap**: Período crítico de competencia "Winner-takes-all" (WTA).
3. **Consolidación Mínima**: Update Hebbiano en el atractor ganador.
4. **Olvido Ortogonal (β)**: Tasa de decaimiento en atractores no ganadores (fuerza olvido del ruido).
5. Se produce salida sobre la "Novedad" de la serie comparándola con una distribución de Poisson.

*Nota: La calibración de las constantes de la **v1.0** se encuentra **BLOQUEADA** para garantizar la reproducibilidad de resultados.*

| **Métrica** | **Fórmula Simplificada** | **Interpretación del Motor** |
| :--- | :--- | :--- |
| **ESI** | $Var(nov\_es)/Var(nov\_bg)$ | `> 2.5` ⚡ Atractor Fuerte <br> `> 1.5` ◆ Estructura Débil |
| **SP** | $1 - Norm(slot\_dist)$ | `> 0.8` ◎ Territorio Estable |
| **KS** | $P-Value (Kolmogorov)$ | `< 0.05` Diferenciación Significativa |

---

## 📂 Estructura del Proyecto

* `/DIG_Explorer_v1`: Núcleo de la herramienta. Contiene entre otros:
   * `dig_core_v1.py` - Algoritmo base de Cimentación.
   * `gui_dig.py` - Interfaz principal interactiva.
   * `run_demo.py` y archivos de ejemplos rápidos.
* `/DIG_Explorer_v1/examples`: Archivos en script de exploradores de ejemplos complejos prediseñados pre-etiquetados (SETI, ECG, Ondas Gravitacionales, etc).
* `/DIG_Explorer_v1/salidas`: Registros resultantes e historial dinámico.

---

> *DIG Explorer v1.0 — Creado y calibrado en Andalucía, España, por José María Pérez, 2026.*
