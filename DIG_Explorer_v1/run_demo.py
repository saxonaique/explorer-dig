"""
run_demo.py — Demostración inmediata del DIG Explorer.
No necesita datos externos. Genera señales sintéticas y observa.

Uso:  python run_demo.py
"""

import subprocess, sys, numpy as np, os

print("=" * 56)
print("  DIG Explorer v1.0 — Demo rápido")
print("=" * 56)

fs = 8192
dur = 60.0
N = int(fs * dur)
t = np.arange(N) / fs

print("\n[1/3] Generando señal THERMAL (ruido puro)...")
rng = np.random.default_rng(0)
noise = rng.normal(0, 1, N)
# Color con filtro
freqs = np.fft.rfftfreq(N, 1/fs)
fn = np.clip(freqs / (fs/2), 0, 1)
H  = 0.5*(1-np.cos(np.pi*np.minimum(fn/0.06, 1))) * \
     0.5*(1+np.cos(np.pi*np.clip((fn-0.94)/0.06, 0, 1)))
H[0] = 0
noise_c = np.real(np.fft.irfft(np.fft.rfft(noise)*H, n=N))
noise_c /= noise_c.std() + 1e-9
np.savetxt("demo_thermal.csv", noise_c, fmt="%.6f")

print("[2/3] Generando señal COHERENT (tono derivante)...")
f0 = 1200.0; dr = 2.5; amp = 5.0
sig = noise_c + amp * np.sin(2*np.pi*(f0*t + 0.5*dr*t**2))
sig /= sig.std() + 1e-9
np.savetxt("demo_coherent.csv", sig, fmt="%.6f")

print("[3/3] Ejecutando DIG Explorer...\n")

for fname, label in [("demo_thermal.csv", "THERMAL"), ("demo_coherent.csv", "COHERENT")]:
    print(f"  {'─'*50}")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(base_dir, "dig_explorer.py"), fname,
           "--fs", str(fs), "--label", label]
    subprocess.run(cmd, check=True)

print("\n✅ Demo completado.")
print("   Revisa los PNG generados para ver los territorios.")
print("   El diario se ha guardado en dig_diary.jsonl")
