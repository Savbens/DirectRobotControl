import threading
import queue
import time

class CoreController:
    def __init__(self, queue_in, queue_out, queue_cmd):
        self.queue_in = queue_in    # команды от GUI
        self.queue_out = queue_out  # данные от сети
        self.queue_cmd = queue_cmd  # команды серверу

        self.running = True

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        print("[Core] Контроллер запущен.")
        while self.running:
            try:
                while True:
                    cmd = self.queue_in.get_nowait()
                    self.handle_command(cmd)
            except queue.Empty:
                pass

            try:
                while True:
                    data = self.queue_out.get_nowait()
                    self.handle_data(data)
            except queue.Empty:
                pass

            time.sleep(0.1)

    def handle_command(self, cmd):
        print(f"[Core] Получена команда: {cmd}")
        # Просто прокидываем её в queue_cmd — сервер отправит её клиенту
        self.queue_cmd.put(cmd)

    def handle_data(self, data):
        print(f"[Core] Принятые данные: {data}")