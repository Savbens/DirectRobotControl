import socket
import time
import random

HOST = 'localhost'  # Адрес сервера (где запущен network_server)
PORT = 5000         # Порт сервера

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[Client] Подключаюсь к {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("[Client] Подключение установлено!")

        try:
            while True:
                # Генерируем случайное число
                value = random.uniform(0, 100)

                # Отправляем число и перевод строки
                msg = f"{value}\\n".encode()
                s.sendall(msg)

                print(f"[Client] Отправлено: {value:.2f}")

                # Ждём 0.5 секунды
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\\n[Client] Остановлено пользователем.")

        except Exception as e:
            print(f"[Client] Ошибка: {e}")

        finally:
            print("[Client] Закрытие соединения.")

if __name__ == '__main__':
    run_client()
