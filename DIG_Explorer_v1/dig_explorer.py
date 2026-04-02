#!/usr/bin/env python3
"""
DIG Explorer v1.0 — Microscopio Informacional
=============================================
Arrastra cualquier señal. DIG observa sin etiquetas.
Preset v1.0 bloqueado. Sin knobs.

Uso:
    python dig_explorer.py datos.csv
    python dig_explorer.py audio.wav --label "mi_señal"
    python dig_explorer.py serie.txt --fs 250 --col 0

Formatos soportados: .csv  .wav  .txt  .npy  .npz
"""

import sys, os, json, argparse, warnings, datetime
import numpy as np
from pathlib import Path
from scipy.signal import stft
from scipy.ndimage import zoom as sp_zoom, gaussian_filter1d
from scipy.stats import ks_2samp

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════
#  PRESET v1.0 — BLOQUEADO. NO MODIFICAR.
# ══════════════════════════════════════════════════════════════════════
_PRESET = {
    "beta"        : 0.02,
    "bootstrap_k" : 20,
    "n_slots"     : 3,
    "n_train"     : 100,    # segmentos de ruido para entrenamiento
    "n_sleep"     : 40,
    "n_seeds"     : 10,
    "seg_dur"     : 4.0,    # segundos por ventana
    "grid_size"   : 16,
    "version"     : "1.0",
}
# ══════════════════════════════════════════════════════════════════════

SIZE = _PRESET["grid_size"]

# ─── Núcleo DIG ───────────────────────────────────────────────────────
def _cosine(a, b):
    a = a.flatten(); b = b.flatten()
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / n) if n > 1e-9 else 0.0

def _sig(x):
    return 1 / (1 + np.exp(-np.clip(x * 4, -10, 10)))

def _nmean(x):
    return np.mean(x) * np.ones_like(x)

def _novelty(slots, pat):
    sims = [_cosine(pat, s) for s in slots if np.std(s) > 1e-4]
    return 1 - max(sims) if sims else 1.0

def _winner(slots, pat):
    return int(np.argmax([_cosine(pat, s) for s in slots]))

def _train(noise_pats, seed=0):
    beta   = _PRESET["beta"]
    boot_k = _PRESET["bootstrap_k"]
    K      = _PRESET["n_slots"]
    rng    = np.random.default_rng(seed)
    g      = rng.normal(0, 0.08, (SIZE, SIZE)); g = np.clip(g, -1, 1)
    slots  = [np.zeros((SIZE, SIZE)) for _ in range(K)]
    B      = boot_k * K
    for t, p in enumerate(noise_pats):
        inp = np.clip(g + 0.30 * p, -1, 1)
        w   = (t // boot_k) % K if t < B else int(np.argmax([_cosine(inp, s) for s in slots]))
        sl  = slots[w]
        slots[w] = np.clip((1 - 0.0005) * sl + 0.08 * (inp - sl), -1, 1)
        if beta > 0:
            sw  = slots[w]; sw2 = np.dot(sw.flatten(), sw.flatten()) + 1e-9
            for k in range(K):
                if k != w and np.abs(slots[k]).max() > 0.01:
                    proj = np.dot(slots[k].flatten(), sw.flatten()) / sw2
                    slots[k] = np.clip(slots[k] - beta * proj * sw, -1, 1)
        drive = 0.08 * _sig(inp * slots[w] * 4) * (slots[w] - inp)
        g = np.clip(0.995 * inp - 0.15 * _nmean(inp) + drive, -1, 1)
    for t in range(_PRESET["n_sleep"]):
        k = t % K; sl = slots[k]; slN = sl / (np.abs(sl).max() + 1e-9)
        g = np.clip(0.993 * g - 0.12 * _nmean(g), -1, 1)
    return slots

# ─── Conversión señal → patrón ────────────────────────────────────────
def _to_pat(segment, fs):
    nperseg  = max(32, min(256, len(segment) // 32))
    noverlap = int(nperseg * 0.75)
    f, _, Zxx = stft(segment, fs=fs, nperseg=nperseg, noverlap=noverlap,
                     window="hann", boundary=None, padded=False)
    mag   = np.abs(Zxx)
    fmask = (f > fs * 0.02) & (f < fs * 0.48)
    mag   = mag[fmask, :]
    if mag.shape[0] < 2 or mag.shape[1] < 2:
        mag = np.abs(Zxx)
    mag = np.log1p(mag * 1000)
    scale = (SIZE / mag.shape[0], SIZE / mag.shape[1])
    pat   = sp_zoom(mag, scale, order=1)
    pat  -= pat.mean(); pat /= (pat.std() + 1e-8)
    return np.clip(pat, -3, 3) / 3.0

def _segment(signal, fs, dur):
    n   = int(fs * dur)
    segs = []
    for i in range(0, len(signal) - n + 1, n // 2):   # 50% overlap
        seg = signal[i:i + n]
        if len(seg) == n:
            seg = seg / (np.std(seg) + 1e-30)
            segs.append(seg)
    return segs

# ─── Loader universal ─────────────────────────────────────────────────
def load_signal(path, col=0, fs_default=None):
    path = Path(path)
    ext  = path.suffix.lower()
    if ext == ".wav":
        from scipy.io import wavfile
        fs, data = wavfile.read(str(path))
        if data.ndim > 1: data = data[:, 0]
        signal = data.astype(float) / (np.abs(data).max() + 1e-9)
    elif ext == ".npy":
        signal = np.load(str(path)).astype(float).flatten()
        fs = fs_default or 1000
    elif ext == ".npz":
        d = np.load(str(path))
        key = list(d.keys())[0]
        signal = d[key].astype(float).flatten()
        fs = fs_default or 1000
    elif ext in (".csv", ".txt"):
        try:
            data = np.loadtxt(str(path), delimiter=",", comments="#")
        except Exception:
            data = np.loadtxt(str(path), comments="#")
        if data.ndim > 1:
            signal = data[:, min(col, data.shape[1]-1)].astype(float)
        else:
            signal = data.astype(float)
        signal = signal - np.nanmean(signal)
        signal = signal / (np.std(signal) + 1e-9)
        fs = fs_default or 1000
    else:
        raise ValueError(f"Formato no soportado: {ext}. Usa .csv .wav .txt .npy .npz")
    return signal, int(fs)

# ─── Motor de observación ─────────────────────────────────────────────
def observe(signal, fs, label="señal", n_noise_seg=None):
    dur   = _PRESET["seg_dur"]
    segs  = _segment(signal, fs, dur)
    if len(segs) < 10:
        dur = len(signal) / (fs * 8)
        segs = _segment(signal, fs, dur)
    if len(segs) < 4:
        print("  ⚠️  Señal demasiado corta. Mínimo recomendado: 30 segundos.")
        segs = [_to_pat(signal, fs)] * 20   # modo emergencia

    pats = [_to_pat(s, fs) for s in segs]
    N    = len(pats)
    n_tr = min(_PRESET["n_train"], N // 3)

    rng  = np.random.default_rng(42)
    idx_tr = rng.choice(N, n_tr, replace=False)
    idx_te = np.array([i for i in range(N) if i not in set(idx_tr)])

    train_pats = [pats[i] for i in idx_tr]
    test_pats  = [pats[i] for i in idx_te]

    # Ruido sintético local (estimado del percentil bajo de la señal)
    noise_floor = np.percentile([np.std(s) for s in segs], 25)
    def local_noise(seed):
        rng2 = np.random.default_rng(seed + 1000)
        s = rng2.normal(0, noise_floor if noise_floor > 0 else 1.0,
                        int(fs * dur))
        return _to_pat(s, fs)
    noise_ref = [local_noise(i) for i in range(40)]

    # Correr N_SEEDS semillas
    all_nov_sig   = []; all_nov_noise = []; all_slots_list = []
    all_sw_sig    = []; esi_vals = []; sp_vals = []

    for seed in range(_PRESET["n_seeds"]):
        slots = _train(train_pats, seed=seed)
        n_sc  = [_novelty(slots, p) for p in noise_ref]
        s_sc  = [_novelty(slots, p) for p in test_pats]
        sw    = [_winner(slots, p)  for p in test_pats]

        esi = float(np.var(s_sc) / (np.var(n_sc) + 1e-9))
        counts = np.bincount(sw, minlength=3) / max(len(sw), 1)
        counts = np.maximum(counts, 1e-9)
        H  = -np.sum(counts * np.log(counts))
        sp = float(1 - H / np.log(3))

        all_nov_sig.extend(s_sc)
        all_nov_noise.extend(n_sc)
        all_slots_list.append(slots)
        all_sw_sig.extend(sw)
        esi_vals.append(esi)
        sp_vals.append(sp)

    # Estadísticos globales
    ks_stat, ks_p = ks_2samp(all_nov_noise, all_nov_sig)

    result = {
        "label"      : label,
        "timestamp"  : datetime.datetime.now().isoformat(),
        "n_segments" : N,
        "n_train"    : n_tr,
        "n_test"     : len(test_pats),
        "fs"         : fs,
        "preset"     : _PRESET["version"],
        "nov_signal" : {"mean": float(np.mean(all_nov_sig)),
                        "std" : float(np.std(all_nov_sig)),
                        "p25" : float(np.percentile(all_nov_sig, 25)),
                        "p75" : float(np.percentile(all_nov_sig, 75))},
        "nov_noise"  : {"mean": float(np.mean(all_nov_noise)),
                        "std" : float(np.std(all_nov_noise))},
        "ESI"        : {"mean": float(np.mean(esi_vals)),
                        "std" : float(np.std(esi_vals))},
        "SP"         : {"mean": float(np.mean(sp_vals)),
                        "std" : float(np.std(sp_vals))},
        "KS_stat"    : float(ks_stat),
        "KS_pval"    : float(ks_p),
        "slot_dist"  : [int(x) for x in np.bincount(all_sw_sig, minlength=3)],
        "slots"      : all_slots_list[-1],   # última semilla para visualización
        "pats_sample": pats[:min(60, N)],
        "nov_series" : all_nov_sig[:len(test_pats)],  # primera semilla
    }
    return result

# ─── Interpretación automática ────────────────────────────────────────
def interpret(r):
    esi = r["ESI"]["mean"]
    sp  = r["SP"]["mean"]
    ks  = r["KS_pval"]
    nov = r["nov_signal"]["mean"]

    lines = []
    if esi > 2.5 and ks < 0.001:
        lines.append("⚡ ATRACTOR INFORMACIONAL FUERTE — estructura emergente clara")
    elif esi > 1.5 and ks < 0.05:
        lines.append("◆  ESTRUCTURA DÉBIL — organización presente, no dominante")
    elif sp > 0.8 and esi < 1.3:
        lines.append("◎  TERRITORIO SILENCIOSO — el sistema lo reconoce sin marcarlo como novedoso")
        lines.append("   (similar al pulsar: identidad sin novedad)")
    elif ks > 0.1:
        lines.append("○  RUIDO PURO — sin separación estadística detectable")
    else:
        lines.append("?  RÉGIMEN MIXTO — exploración adicional recomendada")

    if sp > 0.7:
        lines.append(f"   → Territorio estable: SP={sp:.3f} — la señal ocupa siempre el mismo slot")
    if esi > 2:
        lines.append(f"   → ESI={esi:.2f}: variabilidad informacional {esi:.1f}× mayor que ruido")
    if ks < 0.001:
        lines.append(f"   → Separación de distribuciones perfectamente significativa (KS p={ks:.1e})")

    return lines

# ─── Figura ──────────────────────────────────────────────────────────
def make_figure(r, out_path):
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        print("  [info] plotly no disponible — omitiendo figura")
        return

    slots  = r["slots"]
    nov_ts = r["nov_series"]
    sd_sig = r["nov_signal"]
    sd_noi = r["nov_noise"]

    fig = make_subplots(rows=2, cols=3,
        subplot_titles=[
            "Slot 0 (territorio A)",
            "Slot 1 (territorio B)",
            "Slot 2 (territorio C)",
            "Novelty score — serie temporal",
            "Distribución: señal vs ruido",
            "Métricas DIG",
        ],
        vertical_spacing=0.18, horizontal_spacing=0.10)

    SLOT_COLS = ["#4e79a7", "#e15759", "#59a14f"]
    for ki, (slot, col) in enumerate(zip(slots, SLOT_COLS)):
        fig.add_trace(go.Heatmap(
            z=slot, colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
            showscale=False, colorbar=None,
        ), row=1, col=ki+1)
        fig.update_xaxes(showticklabels=False, row=1, col=ki+1)
        fig.update_yaxes(showticklabels=False, row=1, col=ki+1)

    # Novelty series
    t_ax = np.arange(len(nov_ts))
    fig.add_trace(go.Scatter(
        x=t_ax, y=nov_ts, mode="lines",
        line=dict(color="#4e79a7", width=2),
        fill="tozeroy", fillcolor="rgba(78,121,167,0.15)",
        name="novelty", showlegend=False
    ), row=2, col=1)
    fig.add_hline(y=sd_noi["mean"], line_dash="dot", line_color="#aaa",
                  annotation_text="noise floor", annotation_font_size=9, row=2, col=1)
    fig.update_xaxes(title_text="Segmento #", row=2, col=1)
    fig.update_yaxes(title_text="Novelty", range=[0, 1.05], row=2, col=1)

    # Histogramas
    bins = np.linspace(0, 1, 28)
    for scores, nm, col, op in [
        (r.get("_noise_sc", []), "Ruido ref.", "#78909c", 0.6),
        (nov_ts, r["label"][:12], "#4e79a7", 0.8),
    ]:
        if not scores: continue
        cnt, ed = np.histogram(scores, bins=bins)
        fig.add_trace(go.Bar(
            x=(ed[:-1]+ed[1:])/2, y=cnt/max(cnt.max(),1),
            name=nm, marker_color=col, opacity=op,
            width=(ed[1]-ed[0])*0.85, showlegend=True
        ), row=2, col=2)
    fig.update_xaxes(title_text="Novelty score", row=2, col=2)
    fig.update_yaxes(title_text="Norm.", range=[0,1.2], row=2, col=2)

    # Métricas DIG
    metrics  = ["ESI", "SP", "KS"]
    values   = [r["ESI"]["mean"], r["SP"]["mean"], min(r["KS_stat"]*5, 1.0)]
    thresholds = [2.0, 0.4, 0.5]
    m_cols   = ["#59a14f" if v>t else "#f28e2b"
                for v,t in zip(values, thresholds)]
    fig.add_trace(go.Bar(
        x=metrics, y=values,
        marker_color=m_cols, marker_line_color="white", marker_line_width=1,
        text=[f"{r['ESI']['mean']:.2f}", f"{r['SP']['mean']:.3f}",
              f"{r['KS_stat']:.3f}"],
        textposition="outside", textfont_size=11, showlegend=False
    ), row=2, col=3)
    for thresh, xi in zip([2.0, 0.4, 0.5], [0,1,2]):
        fig.add_shape(type="line", x0=xi-0.4, x1=xi+0.4,
                      y0=thresh, y1=thresh,
                      line=dict(color="#aaa", dash="dot", width=1.5),
                      row=2, col=3)
    fig.update_xaxes(title_text="Metric", row=2, col=3)
    fig.update_yaxes(title_text="Value", range=[0, max(r["ESI"]["mean"]*1.2, 2.8)], row=2, col=3)

    esi_m = r["ESI"]["mean"]; sp_m = r["SP"]["mean"]; ks_p = r["KS_pval"]
    interp_short = interpret(r)[0] if interpret(r) else "?"
    fig.update_layout(
        title=dict(text=(
            f"DIG Explorer v1.0 — {r['label']}<br>"
            f"<span style='font-size:13px;font-weight:normal'>"
            f"{interp_short} | "
            f"ESI={esi_m:.2f}  SP={sp_m:.3f}  KS_p={ks_p:.2e} | "
            f"N={r['n_segments']} seg | preset v{r['preset']} locked"
            f"</span>"
        )),
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.06,
                    xanchor="center", x=0.5, font=dict(size=11)),
        font=dict(size=13), height=620
    )
    fig.write_image(str(out_path))
    print(f"  📊 Figura guardada: {out_path}")

# ─── CLI ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="DIG Explorer v1.0 — microscopio informacional")
    parser.add_argument("file",          help="señal de entrada (.csv .wav .txt .npy .npz)")
    parser.add_argument("--fs",  type=int,   default=None,  help="frecuencia de muestreo Hz")
    parser.add_argument("--col", type=int,   default=0,     help="columna CSV (default 0)")
    parser.add_argument("--label",           default=None,  help="nombre de la señal")
    parser.add_argument("--out",             default=".",   help="directorio de salida")
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║        DIG Explorer v1.0 — microscopio informacional ║")
    print("║        preset v1.0 — BLOQUEADO                       ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    path  = Path(args.file)
    label = args.label or path.stem
    out_d = Path(args.out)
    out_d.mkdir(parents=True, exist_ok=True)

    print(f"  📂 Cargando: {path.name}")
    signal, fs = load_signal(str(path), col=args.col, fs_default=args.fs)
    dur_s = len(signal) / fs
    print(f"  ✅  Señal cargada: {len(signal):,} muestras  {dur_s:.1f}s  fs={fs} Hz")
    print(f"  🔬 Observando con {_PRESET['n_seeds']} semillas...")
    print()

    result = observe(signal, fs, label=label)

    # ── Report terminal ───────────────────────────────────────────────
    print(f"{'═'*56}")
    print(f"  DIG REPORT — {label}")
    print(f"  {result['timestamp'][:19]}  |  preset v{result['preset']}")
    print(f"{'═'*56}")
    print(f"  Segmentos   : {result['n_segments']}  (train={result['n_train']}  test={result['n_test']})")
    print(f"  Slot dist.  : {result['slot_dist']}  (A={result['slot_dist'][0]}, B={result['slot_dist'][1]}, C={result['slot_dist'][2]})")
    print()
    print(f"  nov_señal   : {result['nov_signal']['mean']:.4f} ± {result['nov_signal']['std']:.4f}")
    print(f"  nov_ruido   : {result['nov_noise']['mean']:.4f} ± {result['nov_noise']['std']:.4f}")
    print()
    print(f"  ESI  = {result['ESI']['mean']:.4f} ± {result['ESI']['std']:.4f}")
    print(f"  SP   = {result['SP']['mean']:.4f} ± {result['SP']['std']:.4f}")
    print(f"  KS   = {result['KS_stat']:.4f}   p={result['KS_pval']:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    for line in interpret(result):
        print(f"  {line}")
    print(f"{'═'*56}")

    # ── Guardar figura ─────────────────────────────────────────────────
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"dig_explore_{label}_{ts}"
    make_figure(result, out_d / f"{stem}.png")

    # ── Diary (JSON log acumulativo) ──────────────────────────────────
    diary_path = out_d / "dig_diary.jsonl"
    log_entry  = {k: v for k, v in result.items()
                  if k not in ("slots", "pats_sample", "nov_series")}
    with open(diary_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"  📓 Diario actualizado: {diary_path}")
    print()

if __name__ == "__main__":
    main()
