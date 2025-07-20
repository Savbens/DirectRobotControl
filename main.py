from interface import RobotMonitorApp
from server import network_server
import threading

if __name__ == '__main__':
    app = RobotMonitorApp()

    server_thread = threading.Thread(target=network_server, args=(app.queue_out,), daemon=True)
    server_thread.start()

    app.mainloop()