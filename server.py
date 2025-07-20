import socket

def network_server(queue_out, host='localhost', port=5000):
    """
    TCP-сервер для приёма данных.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)
        print(f"[Network] Сервер слушает {host}:{port}")

        conn, addr = server_sock.accept()
        print(f"[Network] Подключено: {addr}")

        with conn:
            buffer = b''
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("[Network] Клиент отключился.")
                        break
                    buffer += data

                    while b'\\n' in buffer:
                        line, buffer = buffer.split(b'\\n', 1)
                        line = line.strip()
                        if line:
                            try:
                                value = float(line.decode())
                                queue_out.put(value)
                                print(f"[Network] Принято: {value}")
                            except ValueError:
                                print(f"[Network] Ошибка разбора: {line}")

                except ConnectionResetError:
                    print("[Network] Соединение разорвано клиентом.")
                    break
                except Exception as e:
                    print(f"[Network] Ошибка: {e}")
                    break

        print("[Network] Сервер завершил работу.")