"""
ejemplo_gw.py — DIG aplicado a ondas gravitacionales (GWTC-3).

Reproduce los resultados del Exp 16 del paper DIG:
  GW150914 (BBH, SNR=25.1): AUC esperado ~0.999
  GW170817 (BNS, SNR=33.0): AUC esperado ~1.000

Para datos reales GWOSC:
    from gwpy.timeseries import TimeSeries
    data = TimeSeries.fetch_open_data('H1', t0-2, t0+2)
    np.savetxt('gw150914_real.csv', data.value)
    # luego: python dig_explorer.py gw150914_real.csv --fs 4096

Uso: python ejemplo_gw.py
"""

import numpy as np
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent.parent))
import subprocess

# Catálogo GWTC-3 (parámetros oficiales LVC 2021)
GWTC3 = {
    "GW150914": {"m1": 35.6, "m2": 30.6, "snr_net": 25.1, "type": "BBH"},
    "GW170817": {"m1": 1.46, "m2": 1.27, "snr_net": 33.0, "type": "BNS"},
    "GW190521": {"m1": 95.3, "m2": 69.0, "snr_net": 14.7, "type": "BBH-IMBH"},
}

FS = 4096; DUR = 60.0; N = int(FS * DUR)
M_SUN = 1.989e30; G = 6.674e-11; C = 3e8

def aligo_asd(f):
    f = np.atleast_1d(np.asarray(f, float)); asd = np.zeros_like(f)
    mask = f > 0; f0 = 215.0
    S = ((f[mask]/f0)**(-4.14) - 5*(f[mask]/f0)**(-2)
         + 111*(1-(f[mask]/f0)**2+0.5*(f[mask]/f0)**4)/(1+0.5*(f[mask]/f0)**2))
    asd[mask] = 1e-23 * np.sqrt(np.maximum(S, 1e-3))
    return asd

def make_noise(seed=0):
    rng = np.random.default_rng(seed); s = rng.normal(0, 1, N)
    freqs = np.fft.rfftfreq(N, 1/FS); asd = aligo_asd(freqs); asd[0] = 0
    s = np.real(np.fft.irfft(np.fft.rfft(s) * asd, n=N))
    return s / (np.std(s) + 1e-30)

def make_chirp(m1, m2, f_start=20.0):
    Mc_kg = (m1*m2)**(3/5) / (m1+m2)**(1/5) * M_SUN
    t = np.arange(N) / FS; tc = DUR * 0.85; tau = np.maximum(tc - t, 1e-4)
    coeff = (5/256)**(3/8) / (8*np.pi)
    f_inst = np.clip(coeff * (G*Mc_kg/C**3)**(-5/8) * tau**(-3/8), f_start, FS/2-10)
    amp = np.where(tau < 0.01, 0.0, (tau/(tc+1e-6))**(1/4)); amp /= amp.max() + 1e-30
    h = amp * np.sin(2*np.pi * np.cumsum(f_inst) / FS)
    freqs = np.fft.rfftfreq(N, 1/FS); asd = aligo_asd(freqs); asd[0] = 1e-30
    h_w = np.real(np.fft.irfft(np.fft.rfft(h) / asd, n=N))
    return h_w / (np.std(h_w) + 1e-30)

out_dir = Path("resultados_gw"); out_dir.mkdir(exist_ok=True)

for name, ev in GWTC3.items():
    print(f"\n[{name}] {ev['type']}  m1={ev['m1']} m2={ev['m2']} M☉  SNR_net={ev['snr_net']}")
    snr_h1 = ev["snr_net"] / 1.41
    f_start = 25.0 if ev["type"] == "BNS" else 20.0
    noise = make_noise(seed=0)
    chirp = make_chirp(ev["m1"], ev["m2"], f_start=f_start)
    amp   = 10 ** (snr_h1 / 20)
    signal = noise + amp * chirp
    signal /= signal.std() + 1e-9
    csv_path = out_dir / f"{name}_h1.csv"
    np.savetxt(str(csv_path), signal, fmt="%.8f")
    cmd = ["python", "../dig_explorer.py", str(csv_path),
           "--fs", str(FS), "--label", name, "--out", str(out_dir)]
    subprocess.run(cmd, check=True)

print("\n✅ Resultados guardados en resultados_gw/")
print("   Revisa los PNG y dig_diary.jsonl")
