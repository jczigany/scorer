import socketserver
import threading

class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class NagybetusHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.current_thread().getName()}'
        print(f'Connected: {client}')
        while True:
            data = self.rfile.readline()
            if not data:
                break
            self.wfile.write(data.decode('utf-8').upper().encode('utf-8'))
        print(f'Closed: {client}')


with MyTCPServer(('', 59898), NagybetusHandler) as server:
    print('A Nagybetűs szerver fut...')
    server.serve_forever()