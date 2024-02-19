import tkinter as tk
import threading
import time
import random

class ProgressBar:
    def __init__(self, root, canvas, x, y):
        # Inicialización de la barra de progreso con la ventana principal (root), el lienzo (canvas) y las coordenadas (x, y).
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.progress = 0
        self.speed = random.uniform(0.1, 0.5)  # Velocidad de actualización de la barra de progreso (aleatoria).
        self.paused = False
        self.stop_event = threading.Event()

        # Creación de la barra de progreso visual en el lienzo.
        self.bar = self.canvas.create_rectangle(
            self.x, self.y, self.x + 2, self.y + 20, fill='#add8e6'
        )

        # Creación del texto que muestra el progreso actual.
        self.label = self.canvas.create_text(
            self.x + 100, self.y + 10, text=f'{self.progress}%', fill='black'
        )

        # Botones de control: iniciar, pausar/reanudar y detener.
        self.start_button = tk.Button(root, text="Iniciar", command=self.start_progress)
        self.start_button.place(x=self.x + 200, y=self.y - 10)

        self.pause_resume_button = tk.Button(root, text="Pausar", command=self.pause_resume_progress, state=tk.DISABLED)
        self.pause_resume_button.place(x=self.x + 260, y=self.y - 10)

        self.stop_button = tk.Button(root, text="Terminar", command=self.stop_progress, state=tk.DISABLED)
        self.stop_button.place(x=self.x + 320, y=self.y - 10)

    def update_progress(self):
        # Actualización continua de la barra de progreso hasta que alcanza el 100% o se detiene.
        while self.progress < 100:
            time.sleep(self.speed)
            if not self.paused:
                self.progress += 1
                # Actualización visual de la barra y el texto.
                self.canvas.coords(self.bar, self.x, self.y, self.x + 2 * self.progress, self.y + 20)
                self.canvas.itemconfig(self.label, text=f'{self.progress}%')
                self.root.update()

            if self.stop_event.is_set():
                break

    def start_progress(self):
        # Configuración de botones y lanzamiento de hilo para la actualización de la barra de progreso.
        self.start_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.NORMAL, text="Pausar")
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()
        threading.Thread(target=self.update_progress).start()

    def pause_resume_progress(self):
        # Manejo de la pausa/reanudación de la barra de progreso.
        if self.paused:
            self.paused = False
            self.pause_resume_button.config(text="Pausar")
        else:
            self.paused = True
            self.pause_resume_button.config(text="Reanudar")

    def stop_progress(self):
        # Detener la barra de progreso y restablecer valores.
        self.start_button.config(state=tk.NORMAL)
        self.pause_resume_button.config(state=tk.DISABLED, text="Pausar")
        self.stop_button.config(state=tk.DISABLED)
        self.progress = 0
        self.paused = False
        self.stop_event.set()
        # Restablecer la posición visual de la barra y el texto.
        self.canvas.coords(self.bar, self.x, self.y, self.x, self.y + 20)
        self.canvas.itemconfig(self.label, text='0%')

class Multiprogramacion:
    def __init__(self, root):
        # Inicialización de la aplicación de multiprogramación con la ventana principal (root).
        self.root = root
        self.root.title("Multiprogramación")
        self.canvas = tk.Canvas(root, width=500, height=300)  # Ajustado el ancho y alto del canvas
        self.canvas.pack()
        self.progress_bars = []

        # Creación de múltiples barras de progreso en la aplicación.
        for i in range(5):
            bar = ProgressBar(self.root, self.canvas, 50, 40 + i * 60)  # Ajustada la posición y
            self.progress_bars.append(bar)

if __name__ == "__main__":
    # Creación de la ventana principal y la aplicación de multiprogramación.
    root = tk.Tk()
    app = Multiprogramacion(root)
    root.mainloop()
