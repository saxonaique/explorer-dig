import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import subprocess
import threading
import sys
import os
import re
import json
import numpy as np
from pathlib import Path
from PIL import Image, ImageTk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DIG Explorer - Laboratorio Avanzado de Análisis")
        self.root.geometry("1400x900")
        
        # Estilos modernos
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#444444", foreground="white")
        style.configure("TLabelframe", background="#2b2b2b", foreground="#00cfcc")
        style.configure("TLabelframe.Label", background="#2b2b2b", foreground="#00cfcc", font=("Segoe UI", 11, "bold"))
        
        self.root.configure(bg="#2b2b2b")
        
        # Layout Principal
        left_panel = ttk.Frame(root)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        right_panel = ttk.Frame(root)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- PANEL IZQUIERDO: Inputs ---
        input_frame = ttk.LabelFrame(left_panel, text="1. Origen de Señal")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Ruta a los datos:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.file_path_var, width=30).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        ttk.Button(input_frame, text="Examinar", command=self.browse_file).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Frec. de Muestreo (Hz):").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.fs_var = tk.StringVar(value="8192")
        ttk.Entry(input_frame, textvariable=self.fs_var, width=12).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Etiqueta Interna:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.label_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.label_var, width=15).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.btn_preview = ttk.Button(input_frame, text="Visualizar Radar", command=self.do_preview)
        self.btn_preview.grid(row=4, column=0, columnspan=3, pady=10, sticky=tk.EW, padx=5)

        # Audio Automático
        self.btn_audio = ttk.Button(input_frame, text="🔊 Convertir y Escuchar a WAV", command=self.play_audio)
        self.btn_audio.grid(row=5, column=0, columnspan=3, pady=5, sticky=tk.EW, padx=5)
        self.btn_audio.state(['disabled'])

        # --- PANEL IZQUIERDO: Estadísticas Dataset ---
        stats_frame = ttk.LabelFrame(left_panel, text="2. Biografía Extraída")
        stats_frame.pack(fill=tk.X, pady=15)
        
        self.lbl_stats = ttk.Label(stats_frame, text="Carga un archivo csv/txt para\nver métricas base...", font=("Courier", 10))
        self.lbl_stats.pack(padx=10, pady=10, fill=tk.BOTH)

        self.btn_analyze = ttk.Button(left_panel, text="🚀 INICIAR ALGORITMO DIG", command=self.start_analysis)
        self.btn_analyze.pack(fill=tk.X, pady=10, ipady=5)

        # --- PANEL IZQUIERDO: Dashboard Analítico (Resultados DIG) ---
        dash_frame = ttk.LabelFrame(left_panel, text="3. Dashboard de Conclusiones DIG")
        dash_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.lbl_esi = tk.Label(dash_frame, text="Evolutionary Stability Index (ESI)\n-", font=("Segoe UI", 12, "bold"), bg="#3a3a3a", fg="white", pady=10)
        self.lbl_esi.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_sp = tk.Label(dash_frame, text="Shannon Probability (SP)\n-", font=("Segoe UI", 12, "bold"), bg="#3a3a3a", fg="white", pady=10)
        self.lbl_sp.pack(fill=tk.X, padx=10, pady=5)

        self.lbl_ks = tk.Label(dash_frame, text="Kolmogorov-Smirnov p-val\n-", font=("Segoe UI", 10), bg="#3a3a3a", fg="white", pady=5)
        self.lbl_ks.pack(fill=tk.X, padx=10, pady=0)

        self.lbl_interp = tk.Label(dash_frame, text="Esperando ejecución...", font=("Segoe UI", 11, "italic"), bg="#2b2b2b", fg="#aaaaaa", wraplength=250)
        self.lbl_interp.pack(fill=tk.X, padx=10, pady=15)

        # --- PANEL DERECHO: Pestañas Cuantitativas ---
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Previsualizador
        self.tab_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_preview, text="👁️ Raster Dominio del Tiempo")
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        self.fig.patch.set_facecolor('#2b2b2b')
        self.canvas_preview = FigureCanvasTkAgg(self.fig, master=self.tab_preview)
        self.canvas_preview.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Reporte Informe
        self.tab_plot = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_plot, text="📊 Output: Topografía Atractor")
        self.plot_label = ttk.Label(self.tab_plot, background="#1e1e1e")
        self.plot_label.pack(expand=True, fill=tk.BOTH)
        
        # Pestaña 3: Consola
        self.tab_text = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_text, text="💻 Logs Terminal")
        self.text_output = scrolledtext.ScrolledText(self.tab_text, wrap=tk.WORD, bg="#000000", fg="#00ff00", font=("Courier", 10))
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.current_signal = None
        
    def _read_data(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext in [".csv", ".txt"]:
            try: data = np.loadtxt(filepath, delimiter=",", comments="#")
            except: data = np.loadtxt(filepath, comments="#")
            if data.ndim > 1: return data[:, 0]
            else: return data
        elif ext == ".npy":
            return np.load(filepath).flatten()
        return None

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Añadir señal origen",
            filetypes=(("Señal Vector", "*.csv *.txt *.npy"), ("Todos", "*.*"))
        )
        if filepath:
            self.file_path_var.set(filepath)
            self.do_preview()
            
    def do_preview(self):
        path = self.file_path_var.get()
        if not path or not os.path.exists(path): return
            
        try: fs = float(self.fs_var.get())
        except ValueError: fs = 1000

        self.current_signal = self._read_data(path)
        if self.current_signal is None: return
            
        d = self.current_signal
        n_samps = len(d)
        dur = n_samps / fs
        
        stats_text = (
            f"Muestras Tot.: {n_samps:,}\n"
            f"Duración     : {dur:.2f} s\n"
            f"Energía Máx  : {fs/2:.1f} Hz\n"
            f"Desviación   : {np.std(d):.4g}\n"
            f"Rango V      : [{np.min(d):.3g}, {np.max(d):.3g}]"
        )
        self.lbl_stats.config(text=stats_text)
        
        # Pintar preview rápido truncando
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        limit = min(500000, len(d))
        vis_d = d[:limit]
        t = np.arange(len(vis_d)) / fs
        
        self.ax.plot(t, vis_d, color="#ff007f", linewidth=0.5, alpha=0.8)
        self.ax.set_title(f"Vista en Crudo (limitado a {limit} muestras)", color="white")
        self.ax.set_xlabel("Tiempo (s)", color="white")
        self.ax.set_ylabel("Amplitud Digital", color="white")
        self.ax.tick_params(colors="white")
        
        self.fig.tight_layout()
        self.canvas_preview.draw()
        self.notebook.select(self.tab_preview)
        self.btn_audio.state(['!disabled'])

    def play_audio(self):
        if self.current_signal is None: return
        import scipy.io.wavfile as wavfile
        try: fs = int(self.fs_var.get())
        except: fs = 8192 
        
        # Normalizado para audio sin clipping
        norm = self.current_signal / (np.max(np.abs(self.current_signal)) + 1e-9)
        audio_data = np.int16(norm * 32767)
        wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "escenario_audible_temp.wav")
        wavfile.write(wav_path, fs, audio_data)
        
        self.append_text(f"--> Pista de Sonido encapsulada en: {wav_path}\n(Mandando a SoundSystem via Aplay...)\n")
        subprocess.Popen(["aplay", "-q", wav_path], stderr=subprocess.DEVNULL)
            
    def start_analysis(self):
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error de Entrada", "Debes seleccionar un archivo previamente.")
            return

        self.btn_analyze.state(['disabled'])
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, f"{'='*40}\n  INICIANDO BÚSQUEDA DE ESTRUCTURAS\n{'='*40}\nDataset: {os.path.basename(file_path)}\n\n")
        self.notebook.select(self.tab_text)
        
        self.lbl_esi.config(text="ESI: Explorando...", bg="#3a3a3a")
        self.lbl_sp.config(text="SP: Calculando...", bg="#3a3a3a")
        self.lbl_interp.config(text="Inyectando en red neuronal base DIG...")
        
        threading.Thread(target=self.run_dig_explorer, args=(file_path,), daemon=True).start()
        
    def run_dig_explorer(self, filepath):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "dig_explorer.py")
        out_dir = os.path.join(base_dir, "salidas")
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        
        cmd = [sys.executable, script_path, filepath, "--out", out_dir]
        fs = self.fs_var.get().strip()
        if fs: cmd.extend(["--fs", fs])
        label = self.label_var.get().strip()
        if label: cmd.extend(["--label", label])
            
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=base_dir)
            output_lines = []
            
            for line in iter(process.stdout.readline, ''):
                self.root.after(0, self.append_text, line)
                output_lines.append(line)
                
            process.stdout.close()
            process.wait()

            img_path = None
            for line in reversed(output_lines):
                match = re.search(r"Figura guardada:\s*(.*\.png)", line)
                if match:
                    res = match.group(1).strip()
                    img_path = res if os.path.isabs(res) else os.path.join(base_dir, res)
                    break
                    
            if img_path and os.path.exists(img_path):
                self.root.after(0, self.show_image, img_path)
                
            self.root.after(0, self.update_dashboard, out_dir, label if label else Path(filepath).stem)

        except Exception as e:
            self.root.after(0, self.append_text, f"\nError Critico: {e}\n")
        finally:
            self.root.after(0, lambda: self.btn_analyze.state(['!disabled']))
            
    def append_text(self, text):
        self.text_output.insert(tk.END, text)
        self.text_output.see(tk.END)
        
    def show_image(self, img_path):
        try:
            img = Image.open(img_path)
            img.thumbnail((1200, 800), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)
            self.plot_label.config(image=self.current_image)
            self.notebook.select(self.tab_plot)
        except Exception as e:
            self.append_text(f"Falla Visualización: {e}\n")
            
    def update_dashboard(self, out_dir, target_label):
        diary_file = os.path.join(out_dir, "dig_diary.jsonl")
        if not os.path.exists(diary_file): return
        
        last_rec = None
        try:
            with open(diary_file, 'r') as f:
                for line in f:
                    rec = json.loads(line)
                    if rec.get("label") == target_label:
                        last_rec = rec
        except: pass
        
        if last_rec:
            esi = last_rec["ESI"]["mean"]
            sp = last_rec["SP"]["mean"]
            ksp = last_rec["KS_pval"]
            
            # Semáforo ESI: Rojo si Alto (Encuentra extrañeza repetitiva = Anomalía).
            esi_col = "#e74c3c" if esi > 1.8 else ("#f1c40f" if esi > 1.3 else "#2ecc71")
            self.lbl_esi.config(text=f"ESI Evolutivo:\n{esi:.2f}", bg=esi_col, fg=("white" if esi>1.3 else "black"))

            # Semáforo SP: Rojo si disperso, Verde si es conciso.
            sp_col = "#e74c3c" if sp > 0.6 else ("#f1c40f" if sp > 0.4 else "#2ecc71")
            self.lbl_sp.config(text=f"Certeza Espacial (SP):\n{sp:.3f}", bg=sp_col, fg=("white" if sp>0.4 else "black"))
            
            self.lbl_ks.config(text=f"KS Significancia:   {ksp:.1e}")

            if esi > 2.0: interp = "⚡ ATENCIÓN EXPLORADOR:\nLa señal tiene una estructura fortísima."
            elif esi > 1.3: interp = "🟡 Sospechoso:\nHay rastros de comportamiento organizado mixto."
            else: interp = "✅ Confirmado Estático:\nSeñal con características aleatorias/termales."
            self.lbl_interp.config(text=interp, fg=esi_col)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigGUI(root)
    root.mainloop()
