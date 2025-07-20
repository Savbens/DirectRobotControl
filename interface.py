import tkinter as tk
from tkinter import ttk
import threading
import queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class RobotMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Робо-Мониторинг")
        self.geometry("800x600")

        # Очереди для взаимодействия с фоновыми потоками
        self.queue_in = queue.Queue()   # команды из GUI в контроллер
        self.queue_out = queue.Queue()  # данные из контроллера в GUI

        # Данные для графика
        self.x_data = list(range(100))
        self.y_data = [0] * 100

        # Флаг работы
        self.running = False
        self.current_speed = 50
        self.slider_value = self.current_speed

        # Настройка виджетов
        self._create_widgets()
        # Запуск метода обновления GUI
        self.after(100, self._process_queue)


    def _create_widgets(self):
        self.main_pane = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=1)

        self.left_frame = ttk.Frame(self.main_pane, width=500, height=600)
        self.main_pane.add(self.left_frame, weight=3)

        self.right_frame = ttk.Frame(self.main_pane, width=300, height=600)
        self.main_pane.add(self.right_frame, weight=1)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x_data, self.y_data)
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.log_text = tk.Text(self.left_frame, height=8)
        self.log_text.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.right_frame, text="Управление").pack(pady=(10, 5))
        self.start_button = ttk.Button(self.right_frame, text="Старт", command=self._on_start)
        self.start_button.pack(fill=tk.X, padx=10, pady=5)

        self.stop_button = ttk.Button(self.right_frame, text="Стоп", command=self._on_stop)
        self.stop_button.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.right_frame, text="Скорость мотора").pack(pady=(20, 5))
        self.speed_slider = ttk.Scale(self.right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self._on_speed_change)
        self.speed_slider.set(self.current_speed)
        self.speed_slider.pack(fill=tk.X, padx=10)

        self.speed_value_label = ttk.Label(self.right_frame, text=f"{self.current_speed:.1f}")
        self.speed_value_label.pack(pady=(5, 10))

        self.speed_slider.bind("<ButtonRelease-1>", self._on_speed_release)

    def _on_start(self):
        self.running = True
        self.log_event("Нажата кнопка Старт")

    def _on_stop(self):
        self.running = False
        self.log_event("Нажата кнопка Стоп")

    def _on_speed_change(self, val):
        self.slider_value = float(val)
        self.speed_value_label.config(text=f"{self.slider_value:.1f}")

    def _on_speed_release(self, event):
        self.current_speed = self.slider_value
        self.log_event(f"Установлена скорость: {self.current_speed:.1f}")

    def log_event(self, message: str):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def _process_queue(self):
        try:
            while True:
                data = self.queue_out.get_nowait()
                self._update_plot(data)
                self.log_event(f"Получены данные: {data}")
        except queue.Empty:
            pass
        self.after(100, self._process_queue)

    def _update_plot(self, new_value):
        self.y_data.append(new_value)
        self.y_data.pop(0)
        self.line.set_ydata(self.y_data)
        self.canvas.draw()



