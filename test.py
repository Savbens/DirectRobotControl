import socket
import threading
import time
import random

HOST = 'localhost'
PORT = 5000 

current_speed = 50.0
running = False
lock = threading.Lock()

def handle_connection(sock):
    global running, current_speed

    buffer = b''

    while True:
        # Читаем команды и сразу обрабатываем
        try:
            sock.settimeout(0.1)
            data = sock.recv(1024)
            if data:
                buffer += data
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    line = line.decode().strip()
                    print(f"[Client] Получено от Core: {line}")

                    # Примитивный разбор словаря
                    if line.startswith("{") and line.endswith("}"):
                        cmd = eval(line)
                        action = cmd.get("action")
                        if action == "start":
                            with lock:
                                running = True
                        elif action == "stop":
                            with lock:
                                running = False
                        elif action == "set_speed":
                            with lock:
                                current_speed = float(cmd.get("value", 50))

        except socket.timeout:
            pass  # просто идём дальше

        with lock:
            if running:
                base = current_speed
                noise = random.uniform(-5, 5)
                value = max(0, min(100, base + noise))
            else:
                value = 0

        msg = f"{value}\n".encode()
        sock.sendall(msg)
        print(f"[Client] Отправлено: {value:.2f}")
        time.sleep(0.5)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[Client] Подключился к {HOST}:{PORT}")

        handle_connection(s)
