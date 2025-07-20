from interface import RobotMonitorApp
from server import network_server
from core_controller import CoreController
import threading
import queue

if __name__ == '__main__':
    app = RobotMonitorApp()


    queue_cmd = queue.Queue()


    core = CoreController(app.queue_in, app.queue_out, queue_cmd)
    core.start()

    # Запускаем сервер
    server_thread = threading.Thread(
        target=network_server,
        args=(app.queue_out, queue_cmd),
        daemon=True
    )
    server_thread.start()

    app.mainloop()