# DIG — Dynamic Information Grounding
## Microscopio Informacional v1.0

> *Arrastra cualquier señal. DIG observa sin etiquetas.*

---

## Instalación rápida

```bash
# 1. Clonar / descomprimir este paquete
# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Test inmediato (genera datos sintéticos y los analiza)
python run_demo.py
```

## Uso del Explorer (una línea)

```bash
# Cualquier señal de audio
python dig_explorer.py mi_grabacion.wav

# Serie temporal CSV (columna 0 por defecto)
python dig_explorer.py datos.csv --fs 1000

# EEG en formato numpy
python dig_explorer.py eeg_sujeto01.npy --fs 256 --label "sujeto_01"

# Datos de radioastronomía
python dig_explorer.py canal_celebes.txt --fs 250000 --label "BL_sgr"

# Especificar columna y directorio de salida
python dig_explorer.py multicanal.csv --col 2 --fs 500 --out resultados/
```

## Qué produce el Explorer

Cada ejecución genera automáticamente:

| Fichero | Descripción |
|---|---|
| `dig_explore_<label>_<ts>.png` | Figura: template + novelty series + distribución |
| `dig_diary.jsonl` | Registro JSON acumulativo de todas las observaciones |
| Terminal report | ESI, SP, KS, interpretación automática |

## Métricas explicadas

| Métrica | Fórmula | Interpretación |
|---|---|---|
| **ESI** | Var(nov_señal) / Var(nov_ruido) | >2 = atractor informacional |
| **SP** | 1 - H_norm(slot_dist) | >0.4 = territorio estable |
| **KS** | estadístico Kolmogorov-Smirnov | p<0.05 = separación significativa |

### Guía de interpretación automática

| Diagnóstico | ESI | KS p-val | Significado |
|---|---|---|---|
| ⚡ ATRACTOR FUERTE | >2.5 | <0.001 | Estructura emergente clara |
| ◆ ESTRUCTURA DÉBIL | >1.5 | <0.05 | Organización presente |
| ◎ TERRITORIO SILENCIOSO | SP>0.8 | >0.1 | El sistema lo reconoce sin marcarlo como nuevo |
| ○ RUIDO PURO | ~1 | >0.1 | Sin separación detectable |

---

## Arquitectura DIG

```
señal → STFT → log-mag → resize 16×16 → normalizar
    ↓
campo dinámico g(t)
    ↓
WTA competition ← bootstrap (período crítico)
    ↓
Hebbian update (slot ganador)
    ↓
Olvido ortogonal β (slots perdedores)  ← núcleo irreducible
    ↓
Sueño / consolidación
    ↓
novelty_score · ESI · SP · KS
```

### Preset v1.0 (BLOQUEADO — no modificar para reproducibilidad)

```python
beta            = 0.02   # tasa de olvido ortogonal
bootstrap_k     = 20     # pasos de período crítico por slot
n_slots         = 3      # territorios de memoria
n_seeds         = 10     # semillas por observación
seg_dur         = 4.0    # segundos por ventana
grid_size       = 16     # resolución SIZE×SIZE
```

---

## Experimentos realizados (Exp 1–16)

| # | Tema | Resultado clave |
|---|---|---|
| 1–6 | Estabilidad, WTA, sueño, señal, olvido, territorialidad | Núcleo estable a decay=0.995 |
| 7 | Umbral de novedad | AUC=0.667 — generalización precede diferenciación |
| **8** | **Olvido ortogonal** | IC: 0.85→0.26, AUC: 0.67→0.78 con β=0.05 |
| **9** | **6 patrones complejos** | IC=0.40 sin colapso, rec_min>0.55 |
| 10 | Ruido ambiental | Resonancia estocástica en σ≈0.05 |
| 11 | Barrido de semillas (N=50) | CV(rec_mean)<5% — resultado estable |
| **12** | **Umbral discriminación** | sim_sep=0.78 con β=0.05 vs 0.36 sin olvido |
| **13** | **Curva de aprendizaje** | 3 fases: bootstrap → crisis t=70 → plateau t=125 |
| **14** | **Ablación** | Núcleo mínimo: WTA + olvido ortogonal |
| **15** | **Calibración** | Preset óptimo S=0.6421±0.0015 |
| **16** | **Ondas gravitacionales** | GW150914 AUC=0.9994, GW170817 AUC=1.000 |
| **17** | **Radioastronomía BL** | COHERENT ESI=2.39, PULSAR SP=0.996 |

## Cinco leyes emergentes

| Ley | Enunciado |
|---|---|
| **L1** | Detectabilidad ∝ distancia inter-atractor |
| **L2** | La identidad emerge por sustracción, no por adición |
| **L3** | Resolución discriminativa ∝ presión de olvido |
| **L4** | El aprendizaje es disruptivo-convergente: crisis → plateau |
| **L5** | Ruido bajo diferencia; ruido alto borra |

---

## Formatos de datos soportados

| Extensión | Descripción | Notas |
|---|---|---|
| `.wav` | Audio PCM | Se detecta fs automáticamente |
| `.csv` | Serie temporal texto | `--col N` para columna, `--fs N` para frecuencia |
| `.txt` | Números en texto | Igual que CSV |
| `.npy` | Array numpy 1D | Requiere `--fs N` |
| `.npz` | Array numpy comprimido | Usa el primer key |

## Dependencias

```
numpy>=1.24
scipy>=1.11
scikit-learn>=1.3
plotly>=5.18
kaleido>=0.2.1    # para exportar PNG
```

---

*DIG Explorer v1.0 — José María Pérez, Andalucía, España — 2026*
*Preset v1.0 calibrado sobre 3500+ ejecuciones experimentales*
