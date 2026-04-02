import os
import wfdb
import numpy as np
from gwpy.timeseries import TimeSeries
from pathlib import Path

out_dir = Path("datasets_reales")
out_dir.mkdir(exist_ok=True)

print("Descargando Dataset 1: MIT-BIH Arrhythmia Database (ECG Real) desde PhysioNet...")
try:
    # Record 208 contiene multiples latidos irregulares (contracciones ventriculares prematuras)
    record = wfdb.rdrecord('208', sampto=36000, pn_dir='mitdb')  # ~100 segundos
    ecg_signal = record.p_signal[:, 0]  # Tomar el canal primario MLII
    ecg_path = out_dir / "ecg_arritmia_mitdb_208.csv"
    np.savetxt(str(ecg_path), ecg_signal, fmt="%.6f")
    print(f"  ✅ Guardado: {ecg_path} (Info: Frecuencia de Muestreo fs=360 Hz)")
except Exception as e:
    print(f"  ❌ Error descargando ECG: {e}")

print("\nDescargando Dataset 2: Onda Gravitacional GW150914 (Observatorio LIGO H1)...")
try:
    # GW150914 time: 1126259462 GPS
    t0 = 1126259462
    data = TimeSeries.fetch_open_data('H1', t0 - 30, t0 + 10) 
    gw_path = out_dir / "gw150914_ligo.csv"
    np.savetxt(str(gw_path), data.value, fmt="%.8e")
    print(f"  ✅ Guardado: {gw_path} (Info: Frecuencia de Muestreo fs=4096 Hz)")
except Exception as e:
    print(f"  ❌ Error descargando GW150914: {e}")

print("\n¡Descargas completadas! Listos para ser importados en tu GUI.")
