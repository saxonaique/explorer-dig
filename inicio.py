# 1. Descomprimir
unzip DIG_Explorer_v1.zip && cd DIG_Explorer_v1

# 2. Instalar (recomendado en entorno virtual)
pip install -r requirements.txt

# 3. Test inmediato (30 segundos)
python run_demo.py

# 4. Prueba con los datos incluidos
python dig_explorer.py test_data/thermal.csv  --fs 8192 --label THERMAL
python dig_explorer.py test_data/coherent.csv --fs 8192 --label COHERENT
python dig_explorer.py test_data/pulsar.csv   --fs 8192 --label PULSAR

# 5. Conecta tus propios datos
python dig_explorer.py TU_SEÑAL.wav
python dig_explorer.py TU_SEÑAL.csv --fs 256 --label "mi_primera_observación"