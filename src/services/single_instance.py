from PySide6.QtCore import QSharedMemory
from PySide6.QtNetwork import QLocalServer, QLocalSocket


class SingleInstance:
    def __init__(self, key: str, on_second_instance=None):
        self.key = key
        self.on_second_instance = on_second_instance
        self.shared_memory = QSharedMemory(key)
        self.server = None

        self.is_running = not self.shared_memory.create(1)

        if self.is_running:
            self._notify_running_instance()
        else:
            self._start_local_server()

    def release(self):
        if self.server is not None:
            self.server.close()
            QLocalServer.removeServer(self.key)
            self.server = None

        if self.shared_memory.isAttached():
            self.shared_memory.detach()

    def _notify_running_instance(self):
        socket = QLocalSocket()
        socket.connectToServer(self.key)
        if socket.waitForConnected(500):
            socket.write(b"show")
            socket.waitForBytesWritten(500)
            socket.disconnectFromServer()

    def _start_local_server(self):
        QLocalServer.removeServer(self.key)
        self.server = QLocalServer()
        if not self.server.listen(self.key):
            QLocalServer.removeServer(self.key)
            if not self.server.listen(self.key):
                raise RuntimeError(
                    f"No se pudo iniciar el servidor local de instancia unica: {self.key}"
                )
        self.server.newConnection.connect(self._handle_new_connection)

    def _handle_new_connection(self):
        socket = self.server.nextPendingConnection()
        if socket.waitForReadyRead(500):
            if socket.readAll() == b"show" and self.on_second_instance:
                self.on_second_instance()
        socket.disconnectFromServer()
