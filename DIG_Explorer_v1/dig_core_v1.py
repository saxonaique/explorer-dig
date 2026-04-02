"""
DIG Core v1.0 — Dynamic Information Grounding
=============================================
Arquitectura mínima: WTA + Olvido ortogonal (Gram-Schmidt)
Preset óptimo calibrado en Exp 15: beta=0.02, bootstrap_k=20
Score benchmark S=0.6421 ± 0.0015

José María Pérez — 2026
"""

import numpy as np
from scipy.signal import stft
from scipy.ndimage import zoom as sp_zoom

# ── Constantes ──────────────────────────────────────────────────────
SIZE = 16   # resolución de la grilla de slots (16×16 = 256 píxeles)

PRESET = {
    "beta"            : 0.02,   # tasa de olvido ortogonal  ← más sensible
    "bootstrap_k"     : 20,     # pasos de período crítico por slot
    "n_slots"         : 3,      # número de territorios de memoria
    "eta"             : 0.08,   # tasa de aprendizaje Hebbian
    "decay"           : 0.0005, # decaimiento pasivo del slot
    "field_decay"     : 0.995,  # decaimiento del campo dinámico g
    "field_inhibit"   : 0.15,   # inhibición de la media del campo
    "n_sleep"         : 80,     # pasos de consolidación durante el sueño
    "version"         : "1.0",
}

# ── Primitivas matemáticas ───────────────────────────────────────────
def cosine(a, b):
    """Similitud coseno entre dos arrays."""
    a = a.flatten(); b = b.flatten()
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / n) if n > 1e-9 else 0.0

def pearson(a, b):
    """Correlación de Pearson entre dos arrays."""
    a = a.flatten() - a.mean()
    b = b.flatten() - b.mean()
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / n) if n > 1e-9 else 0.0

def _sig(x):
    return 1 / (1 + np.exp(-np.clip(x * 4, -10, 10)))

def _nmean(x):
    return np.mean(x) * np.ones_like(x)

def _laplacian(x):
    return (np.gradient(np.gradient(x, axis=0), axis=0) +
            np.gradient(np.gradient(x, axis=1), axis=1))

# ── Selección del ganador (WTA) ──────────────────────────────────────
def select_winner(inp, slots, t, boot_total, boot_k, rng, epsilon=0.0):
    """
    Selecciona el slot ganador.
    - Durante el período crítico (t < boot_total): rotación forzada.
    - Después: WTA puro por similitud coseno.
    - epsilon > 0: exploración estocástica (no usar en producción).
    """
    K = len(slots)
    if t < boot_total:
        return (t // boot_k) % K
    if epsilon > 0 and rng.random() < epsilon:
        return int(rng.integers(K))
    return int(np.argmax([cosine(inp, s) for s in slots]))

# ── Paso de entrenamiento ────────────────────────────────────────────
def train_step(g, slots, inp, winner, beta=None):
    """
    Actualiza el campo dinámico y los slots.
    - Ganador: aprendizaje Hebbian.
    - Perdedores: olvido ortogonal (proyección Gram-Schmidt).
    """
    if beta is None:
        beta = PRESET["beta"]
    eta   = PRESET["eta"]
    decay = PRESET["decay"]

    # Actualización Hebbian del ganador
    sl = slots[winner]
    slots[winner] = np.clip(
        (1 - decay) * sl + eta * (inp - sl), -1, 1)

    # Olvido ortogonal para todos los perdedores
    if beta > 0:
        sw  = slots[winner]
        sw2 = float(np.dot(sw.flatten(), sw.flatten())) + 1e-9
        for k in range(len(slots)):
            if k != winner and np.abs(slots[k]).max() > 0.01:
                proj = float(np.dot(slots[k].flatten(), sw.flatten())) / sw2
                slots[k] = np.clip(slots[k] - beta * proj * sw, -1, 1)

    # Campo dinámico
    drive = 0.08 * _sig(inp * slots[winner] * 4) * (slots[winner] - inp)
    g = np.clip(
        PRESET["field_decay"] * inp
        - PRESET["field_inhibit"] * _nmean(inp)
        + drive, -1, 1)
    return g, slots

# ── Paso de sueño (consolidación) ───────────────────────────────────
def sleep_step(g, slots, ms, k):
    """
    Consolidación durante el sueño.
    Reactiva el slot k sobre el campo sin nueva entrada.
    """
    sl  = slots[k]
    slN = sl / (np.abs(sl).max() + 1e-9)
    ms  = 0.9 * ms + 0.1 * slN
    g   = np.clip(g + 0.30 * slN, -1, 1)
    g   = np.clip(
        0.993 * g
        - 0.15 * _nmean(g)
        + 0.06 * _sig(g * slN * 3) * (slN - g), -1, 1)
    return g, slots, ms

# ── Conversión señal → patrón DIG ───────────────────────────────────
def signal_to_pattern(segment, fs, fmin_frac=0.02, fmax_frac=0.48):
    """
    Convierte un segmento de señal 1D a un patrón DIG (SIZE×SIZE).
    Usa STFT → log-magnitud → recorte de banda → resize.
    """
    N       = len(segment)
    nperseg = max(32, min(256, N // 32))
    noverlap= int(nperseg * 0.75)
    f, _, Zxx = stft(segment, fs=fs, nperseg=nperseg, noverlap=noverlap,
                     window="hann", boundary=None, padded=False)
    mag   = np.abs(Zxx)
    fmask = (f > fs * fmin_frac) & (f < fs * fmax_frac)
    mag   = mag[fmask, :] if fmask.sum() > 1 else np.abs(Zxx)
    mag   = np.log1p(mag * 1000)
    scale = (SIZE / mag.shape[0], SIZE / mag.shape[1])
    pat   = sp_zoom(mag, scale, order=1)
    pat  -= pat.mean()
    pat  /= (pat.std() + 1e-8)
    return np.clip(pat, -3, 3) / 3.0

# ── Métricas DIG ────────────────────────────────────────────────────
def novelty_score(slots, pat):
    """Novedad: 1 - max_cosine(pat, slot_k). Mayor = más novedoso."""
    sims = [cosine(pat, s) for s in slots if np.std(s) > 1e-4]
    return 1 - max(sims) if sims else 1.0

def slot_winner(slots, pat):
    """Slot con mayor similitud al patrón."""
    return int(np.argmax([cosine(pat, s) for s in slots]))

def compute_ic(slots):
    """
    Índice de correlación (IC) entre slots.
    IC ≈ 0  → slots ortogonales (buena diferenciación).
    IC ≈ 1  → slots colineales (colapso de representación).
    """
    K  = len(slots)
    cs = []
    for i in range(K):
        for j in range(i + 1, K):
            if np.std(slots[i]) > 1e-4 and np.std(slots[j]) > 1e-4:
                cs.append(abs(pearson(slots[i], slots[j])))
    return float(np.mean(cs)) if cs else 0.0

def compute_recovery(slots, patterns):
    """
    Tasa de recuperación: fracción de patrones correctamente asignados
    al slot que los representa mejor.
    """
    if not patterns:
        return 0.0
    correct = sum(
        1 for p in patterns
        if slot_winner(slots, p) == np.argmax([cosine(p, s) for s in slots])
    )
    return correct / len(patterns)

def benchmark_score(rec_mean, rec_min, auc, ic):
    """
    Score compuesto S del benchmark DIG (Exp 15).
    Umbral operativo: S >= 0.60.
    """
    return 0.30 * rec_mean + 0.25 * rec_min + 0.25 * auc + 0.20 * (1 - ic)

# ── Pipeline completo (entrenamiento + evaluación) ──────────────────
def run_dig(patterns_dict, n_slots=3, beta=None, seed=42,
            n_train=360, n_sleep=80, bootstrap_per_slot=20):
    """
    Entrena DIG sobre un diccionario de patrones y evalúa recuperación.

    Parámetros:
        patterns_dict : dict {nombre: [array 16×16, ...]}
        n_slots       : número de slots de memoria
        beta          : tasa de olvido ortogonal (None = PRESET)
        seed          : semilla aleatoria
        n_train       : pasos de entrenamiento
        n_sleep       : pasos de sueño
        bootstrap_per_slot : pasos de período crítico por slot

    Devuelve:
        dict con slots, IC, AUC, rec, dominant
    """
    if beta is None:
        beta = PRESET["beta"]
    rng   = np.random.default_rng(seed)
    K     = n_slots
    g     = rng.normal(0, 0.08, (SIZE, SIZE))
    g     = np.clip(g, -1, 1)
    slots = [np.zeros((SIZE, SIZE)) for _ in range(K)]
    ms    = np.zeros((SIZE, SIZE))
    boot_total = bootstrap_per_slot * K

    # Aplanar todos los patrones para el bucle de entrenamiento
    all_pats   = []
    all_labels = []
    for name, plist in patterns_dict.items():
        for p in plist:
            all_pats.append(p)
            all_labels.append(name)
    all_pats   = np.array(all_pats)
    all_labels = np.array(all_labels)

    # Barajar y repetir hasta n_train
    idx = np.tile(np.arange(len(all_pats)), (n_train // len(all_pats) + 2))
    rng.shuffle(idx)
    idx = idx[:n_train]

    for t, i in enumerate(idx):
        inp = np.clip(g + 0.35 * all_pats[i], -1, 1)
        w   = select_winner(inp, slots, t, boot_total,
                            bootstrap_per_slot, rng)
        g, slots = train_step(g, slots, inp, w, beta)

    # Sueño
    for t in range(n_sleep):
        g, slots, ms = sleep_step(g, slots, ms, t % K)

    # Evaluación
    ic  = compute_ic(slots)
    rec = {}
    for name, plist in patterns_dict.items():
        sc = [novelty_score(slots, p) for p in plist]
        rec[name] = float(np.mean(sc))

    # Slot dominante por clase
    dominant = {}
    for name, plist in patterns_dict.items():
        winners = [slot_winner(slots, p) for p in plist]
        from collections import Counter
        dominant[name] = int(Counter(winners).most_common(1)[0][0])

    # AUC approximado (novedad inter-clase)
    try:
        from sklearn.metrics import roc_auc_score
        all_names = list(patterns_dict.keys())
        if len(all_names) >= 2:
            ref_sc  = [novelty_score(slots, p)
                       for p in patterns_dict[all_names[0]]]
            test_sc = [novelty_score(slots, p)
                       for p in patterns_dict[all_names[1]]]
            y_t = [0] * len(ref_sc) + [1] * len(test_sc)
            y_s = ref_sc + test_sc
            auc = float(roc_auc_score(y_t, y_s))
        else:
            auc = 0.5
    except Exception:
        auc = 0.5

    return {
        "slots"   : slots,
        "g"       : g,
        "IC"      : ic,
        "AUC"     : auc,
        "rec"     : rec,
        "dominant": dominant,
    }
