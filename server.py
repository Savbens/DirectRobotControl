import socket
import threading

def network_server(queue_out, queue_cmd, host='localhost', port=5000):
    """
    TCP-сервер:
      - Принимает данные от клиента (test.py) и кладёт их в queue_out.
      - Берёт команды из queue_cmd и отправляет их обратно клиенту.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)
        print(f"[Server] Сервер слушает {host}:{port}")

        conn, addr = server_sock.accept()
        print(f"[Server] Подключено клиентом: {addr}")

        with conn:
            # Два потока:
            # 1 — читает данные от клиента
            # 2 — шлёт команды клиенту

            def reader():
                buffer = b''
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("[Server] Клиент отключился.")
                        break

                    buffer += data
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        try:
                            value = float(line.decode())
                            queue_out.put(value)
                            print(f"[Server] Принято от клиента: {value:.2f}")
                        except ValueError:
                            print(f"[Server] Ошибка разбора: {line}")

            def writer():
                while True:
                    cmd = queue_cmd.get()
                    msg = f"{cmd}\n".encode()
                    try:
                        conn.sendall(msg)
                        print(f"[Server] Отправлено клиенту: {cmd}")
                    except Exception as e:
                        print(f"[Server] Ошибка отправки: {e}")
                        break

            t_reader = threading.Thread(target=reader, daemon=True)
            t_writer = threading.Thread(target=writer, daemon=True)

            t_reader.start()
            t_writer.start()

            t_reader.join()
            t_writer.join()

    print("[Server] Соединение закрыто.")