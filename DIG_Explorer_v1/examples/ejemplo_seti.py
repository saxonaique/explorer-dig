"""
ejemplo_seti.py — DIG aplicado a radioastronomía / SETI.

Protocolo BL-Real-01 (Breakthrough Listen compatible):
  - Sin etiquetas, sin plantillas
  - DIG aprende el ruido del receptor
  - Detecta desviaciones estructurales

Para datos reales de Breakthrough Listen:
    # Descargar desde https://breakthroughlistenberkeley.edu/data
    # Formato: filterbank (.fil) → convertir con sigpyproc o blimpy
    pip install blimpy
    from blimpy import Waterfall
    obs = Waterfall("path/to/file.fil")
    signal = obs.data[0, 0, :]   # primer canal
    np.save("bl_signal.npy", signal)
    # luego: python dig_explorer.py bl_signal.npy --fs 3000000 --label "BL_target"

Uso (datos sintéticos):
    python ejemplo_seti.py
"""

import numpy as np
from pathlib import Path
import subprocess
from scipy.ndimage import gaussian_filter1d

FS_BL = 8192; DUR_BL = 60.0; N_BL = int(FS_BL * DUR_BL)

def _bl_noise(seed=0):
    rng = np.random.default_rng(seed); s = rng.normal(0, 1, N_BL)
    f = np.fft.rfftfreq(N_BL, 1/FS_BL); fn = np.clip(f/(FS_BL/2), 0, 1)
    H = (0.5*(1-np.cos(np.pi*np.minimum(fn/0.06, 1))) *
         0.5*(1+np.cos(np.pi*np.clip((fn-0.94)/0.06, 0, 1)))); H[0] = 0
    s = np.real(np.fft.irfft(np.fft.rfft(s)*H, n=N_BL)); return s/(s.std()+1e-9)

def _rfi_narrowband(seed=0):
    rng = np.random.default_rng(seed); t = np.arange(N_BL)/FS_BL; s = _bl_noise(seed)
    f0 = rng.uniform(600, 3400); dr = rng.uniform(-20, 20); amp = rng.uniform(2, 6)
    return (s + amp*np.sin(2*np.pi*(f0+0.5*dr*t)*t)) / 1.5

def _coherent_drifting(seed=0):
    rng = np.random.default_rng(seed); t = np.arange(N_BL)/FS_BL; s = _bl_noise(seed)
    f0 = rng.uniform(700, 3000); dr = rng.uniform(0.3, 5.0); amp = rng.uniform(3, 7)
    return (s + amp*np.sin(2*np.pi*(f0*t+0.5*dr*t**2))) / 2.0

def _pulsar(seed=0):
    rng = np.random.default_rng(seed); t = np.arange(N_BL)/FS_BL; s = _bl_noise(seed)
    period = rng.uniform(0.05, 0.35); amp = rng.uniform(2, 4); w = 0.008
    for pt in np.arange(0, DUR_BL, period):
        s += amp * np.exp(-0.5*((t-pt)/(w*period))**2)
    return s / (s.std() + 1e-9)

out_dir = Path("resultados_seti"); out_dir.mkdir(exist_ok=True)

print("Protocolo BL-Real-01 — Breakthrough Listen (simulado)")
print("Preset v1.0 sin cambios — DIG aprende ruido, observa estructura\n")
for name, gen in [("THERMAL", _bl_noise), ("RFI_NB", _rfi_narrowband),
                   ("COHERENT", _coherent_drifting), ("PULSAR", _pulsar)]:
    sig = gen(seed=42)
    path = out_dir / f"{name}.csv"
    np.savetxt(str(path), sig, fmt="%.6f")
    dig_path = Path(__file__).resolve().parent.parent / "dig_explorer.py"
    cmd = ["python", str(dig_path), str(path),
           "--fs", str(FS_BL), "--label", name, "--out", str(out_dir)]
    subprocess.run(cmd, check=True)

print("\n✅ Resultados en resultados_seti/")
print("   Esperar: THERMAL ESI~1.2  COHERENT ESI~7.5  PULSAR SP~1.0")
