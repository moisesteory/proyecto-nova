import os
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_NAME = "Separador de Música"


def separate_audio(input_path: str, output_dir: str):
    import soundfile as sf
    import torch
    from demucs_infer import DemucsSession

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    song_dir = out / Path(input_path).stem
    song_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    with DemucsSession(model="htdemucs", device=device) as session:
        _, stems = session.infer(input_path)
        samplerate = session.samplerate

        def to_numpy(wave):
            data = wave.detach().cpu().numpy()
            if data.ndim == 3:
                data = data[0]
            if data.ndim == 2:
                data = data.T
            return data

        vocals = to_numpy(stems["vocals"])
        instrumental = sum(to_numpy(stems[name]) for name in ("drums", "bass", "other"))

    sf.write(song_dir / "Voz.wav", vocals, samplerate, subtype="PCM_16")
    sf.write(song_dir / "Instrumental.wav", instrumental, samplerate, subtype="PCM_16")
    return song_dir


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME + " - V1")
        self.root.geometry("700x455")
        self.root.resizable(False, False)

        self.file_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(Path.home() / "Música" / "SeparadorMusica"))
        self.status_var = tk.StringVar(value="Selecciona una canción para comenzar.")
        self.progress = ttk.Progressbar(root, mode="indeterminate")

        ttk.Label(root, text="🎵 Separador de Música", font=("Segoe UI", 22, "bold")).pack(pady=(24, 4))
        ttk.Label(root, text="V1 • Voz / Instrumental", font=("Segoe UI", 11)).pack(pady=(0, 22))

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="x")

        ttk.Label(frame, text="Canción:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.file_var, width=68).grid(row=1, column=0, padx=(0, 10), pady=6)
        ttk.Button(frame, text="Examinar...", command=self.select_file).grid(row=1, column=1, pady=6)

        ttk.Label(frame, text="Carpeta de salida:").grid(row=2, column=0, sticky="w", pady=(14, 0))
        ttk.Entry(frame, textvariable=self.output_var, width=68).grid(row=3, column=0, padx=(0, 10), pady=6)
        ttk.Button(frame, text="Elegir...", command=self.select_output).grid(row=3, column=1, pady=6)

        self.start_btn = ttk.Button(root, text="▶  Separar voz e instrumental", command=self.start)
        self.start_btn.pack(pady=18)
        self.progress.pack(fill="x", padx=45, pady=4)
        ttk.Label(root, textvariable=self.status_var, wraplength=610).pack(pady=18)
        ttk.Label(root, text="Procesamiento local • La primera canción descarga el modelo de IA una sola vez.", font=("Segoe UI", 9)).pack(side="bottom", pady=14)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Selecciona una canción",
            filetypes=[("Audio", "*.mp3 *.wav *.flac *.m4a *.ogg *.aac"), ("Todos", "*.*")],
        )
        if path:
            self.file_var.set(path)
            self.status_var.set("Archivo seleccionado. Pulsa Separar.")

    def select_output(self):
        path = filedialog.askdirectory(title="Selecciona carpeta de salida")
        if path:
            self.output_var.set(path)

    def start(self):
        path = self.file_var.get().strip().strip('"')
        output = self.output_var.get().strip().strip('"')
        if not path or not os.path.isfile(path):
            messagebox.showwarning("Canción", "Selecciona un archivo de audio válido.")
            return
        if not output:
            messagebox.showwarning("Salida", "Selecciona una carpeta de salida.")
            return
        self.start_btn.config(state="disabled")
        self.progress.start(12)
        self.status_var.set("Procesando con IA... la primera vez puede tardar y descargar el modelo.")
        threading.Thread(target=self.worker, args=(path, output), daemon=True).start()

    def worker(self, path, output):
        try:
            result = separate_audio(path, output)
            self.root.after(0, self.finished, result)
        except Exception as exc:
            details = "".join(traceback.format_exception_only(type(exc), exc)).strip()
            self.root.after(0, self.failed, details)

    def finished(self, folder):
        self.progress.stop()
        self.start_btn.config(state="normal")
        self.status_var.set("¡Listo! Voz e instrumental fueron creados.")
        messagebox.showinfo("Proceso terminado", f"Archivos creados en:\n\n{folder}\n\nVoz.wav\nInstrumental.wav")

    def failed(self, details):
        self.progress.stop()
        self.start_btn.config(state="normal")
        self.status_var.set("No se pudo completar la separación.")
        messagebox.showerror("Error", "No se pudo procesar la canción.\n\n" + details)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    App(root)
    root.mainloop()
