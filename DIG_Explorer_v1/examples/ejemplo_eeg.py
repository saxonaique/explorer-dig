"""
ejemplo_eeg.py — DIG aplicado a EEG (PhysioNet).

Instrucciones para descargar datos reales:

    pip install wfdb
    import wfdb
    # Datos de sueño (Sleep-EDF dataset):
    record = wfdb.rdrecord("SC4001E0", pn_dir="sleep-edfx/sleep-cassette")
    signal = record.p_signal[:, 0]  # canal EEG Fpz-Cz
    np.save("eeg_sleep_SC4001.npy", signal)
    # luego: python dig_explorer.py eeg_sleep_SC4001.npy --fs 100 --label "sleep_SC4001"

    # Datos de epilepsia (CHB-MIT):
    # https://physionet.org/content/chbmit/1.0.0/

Uso (con datos propios):
    python dig_explorer.py tu_eeg.csv --fs 256 --label "sujeto_control"
    python dig_explorer.py tu_eeg.wav --label "eeg_audio_proxy"

Este ejemplo genera EEG sintético realista si no tienes datos reales:
    python ejemplo_eeg.py
"""

import numpy as np
from pathlib import Path
import subprocess, sys

sys.path.insert(0, str(Path(__file__).parent.parent))

FS_EEG = 256   # Hz — estándar EEG clínico
DUR_EEG = 120  # segundos
N_EEG   = int(FS_EEG * DUR_EEG)

def _eeg_noise(seed=0):
    """Ruido EEG 1/f con picos en bandas delta/theta/alpha/beta."""
    rng = np.random.default_rng(seed)
    t   = np.arange(N_EEG) / FS_EEG
    # 1/f background
    n   = rng.normal(0, 1, N_EEG)
    f   = np.fft.rfftfreq(N_EEG, 1/FS_EEG)
    F   = np.fft.rfft(n)
    psd = np.where(f > 0, f**(-0.8), 0)
    n   = np.real(np.fft.irfft(F * np.sqrt(psd), n=N_EEG))
    # Bandas EEG (delta 1-4Hz, theta 4-8Hz, alpha 8-13Hz, beta 13-30Hz)
    for band_f, amp, phase in [(2, 3.0, 0), (6, 2.0, 1.0),
                                (10, 4.0, 2.0), (20, 1.5, 0.5)]:
        n += amp * rng.uniform(0.7, 1.3) * np.sin(2*np.pi*band_f*t + phase)
    return n / (n.std() + 1e-9)

def _eeg_spike(seed=0, n_spikes=8):
    """EEG con spikes epileptiformes."""
    s = _eeg_noise(seed)
    rng = np.random.default_rng(seed + 100)
    t   = np.arange(N_EEG) / FS_EEG
    for _ in range(n_spikes):
        t0   = rng.uniform(5, DUR_EEG - 5)
        amp  = rng.uniform(8, 20)
        freq = rng.uniform(3, 6)
        dur  = rng.uniform(1.5, 3.0)
        env  = np.exp(-0.5 * ((t - t0) / (dur / 4))**2)
        s   += amp * env * np.sin(2*np.pi*freq*(t - t0))
    return s / (s.std() + 1e-9)

out_dir = Path("resultados_eeg"); out_dir.mkdir(exist_ok=True)

print("Generando EEG sintético realista...")
for name, gen in [("EEG_normal", _eeg_noise), ("EEG_epilepsia", _eeg_spike)]:
    sig = gen(seed=42)
    path = out_dir / f"{name}.csv"
    np.savetxt(str(path), sig, fmt="%.6f")
    print(f"  {name}: {len(sig)/FS_EEG:.0f}s  fs={FS_EEG}Hz")
    cmd = ["python", "../dig_explorer.py", str(path),
           "--fs", str(FS_EEG), "--label", name, "--out", str(out_dir)]
    subprocess.run(cmd, check=True)

print("\n✅ Resultados en resultados_eeg/")
print("   Para EEG real de PhysioNet:")
print("   pip install wfdb")
print("   python -c \"import wfdb; wfdb.dl_database('sleep-edfx', dl_dir=\'sleep_data\', records=[\'SC4001E0\'])\"\"")
