import socket
import threading
import select
import sys
import time
import getopt

LISTENING_ADDR = '127.0.0.1'
LISTENING_PORT = 700
PASS = ''
BUFLEN = 4096 * 4
TIMEOUT = 60
DEFAULT_HOST = '127.0.0.1:111'
RESPONSE = 'HTTP/1.1 101 <b><i><font color="blue">DOTYCAT.COM</font></b> Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: foo\r\n\r\n'

SOCKS_VERSION = 5

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.running = False
        self.host = host
        self.port = port
        self.threads = []
        self.threadsLock = threading.Lock()
        self.logLock = threading.Lock()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.settimeout(2)
            soc.bind((self.host, int(self.port)))
            soc.listen(5)
            self.running = True

            while self.running:
                try:
                    client_socket, addr = soc.accept()
                    client_socket.setblocking(1)
                    conn = ConnectionHandler(client_socket, self, addr)
                    conn.start()
                    self.addConn(conn)
                except socket.timeout:
                    continue
                except Exception as e:
                    self.printLog(f"Server error: {e}")

    def printLog(self, log):
        with self.logLock:
            print(log)

    def addConn(self, conn):
        with self.threadsLock:
            if self.running:
                self.threads.append(conn)

    def removeConn(self, conn):
        with self.threadsLock:
            self.threads.remove(conn)

    def close(self):
        self.running = False
        with self.threadsLock:
            for conn in list(self.threads):
                conn.close()

class ConnectionHandler(threading.Thread):
    def __init__(self, socClient, server, addr):
        super().__init__()
        self.clientClosed = False
        self.targetClosed = True
        self.client = socClient
        self.client_buffer = b''
        self.server = server
        self.log = f'Connection: {addr}'

    def close(self):
        if not self.clientClosed:
            try:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            except Exception as e:
                self.server.printLog(f"Error closing client: {e}")
            finally:
                self.clientClosed = True

        if not self.targetClosed:
            try:
                self.target.shutdown(socket.SHUT_RDWR)
                self.target.close()
            except Exception as e:
                self.server.printLog(f"Error closing target: {e}")
            finally:
                self.targetClosed = True

    def run(self):
        try:
            self.client_buffer = self.client.recv(BUFLEN)
            
            if self.client_buffer[0] == SOCKS_VERSION:
                self.handle_socks5()
            else:
                self.handle_http()
        except Exception as e:
            self.log += f' - error: {e}'
            self.server.printLog(self.log)
        finally:
            self.close()
            self.server.removeConn(self)

    def handle_http(self):
        self.client_buffer = self.client_buffer.decode('utf-8')
        hostPort = self.findHeader(self.client_buffer, 'X-Real-Host')

        if not hostPort:
            hostPort = DEFAULT_HOST

        split = self.findHeader(self.client_buffer, 'X-Split')

        if split:
            self.client.recv(BUFLEN)

        passwd = self.findHeader(self.client_buffer, 'X-Pass')

        if len(PASS) != 0 and passwd != PASS:
            self.client.sendall(b'HTTP/1.1 400 WrongPass!\r\n\r\n')
        elif len(PASS) != 0 or hostPort.startswith('127.0.0.1') or hostPort.startswith('localhost'):
            self.method_CONNECT(hostPort)
        else:
            self.client.sendall(b'HTTP/1.1 403 Forbidden!\r\n\r\n')

    def handle_socks5(self): 
        self.client.sendall(b"\x05\x00")  # Version 5, No Authentication Required
 
        version, cmd, _, address_type = self.client.recv(4)
        if cmd != 1:  # Only CONNECT command is supported
            self.close()
            return
 
        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.client.recv(4))
        elif address_type == 3:  # Domain name
            domain_length = self.client.recv(1)[0]
            address = self.client.recv(domain_length).decode('utf-8')
        else:
            self.close()
            return
        port = int.from_bytes(self.client.recv(2), 'big')

        self.log += f' - SOCKS5 CONNECT {address}:{port}'
        self.connect_target(f"{address}:{port}")
        self.client.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00") 
        self.client_buffer = b''
        self.server.printLog(self.log)
        self.doCONNECT()

    def findHeader(self, headers, header_name):
        headers = headers.split('\r\n')
        for header in headers:
            if header.startswith(header_name + ': '):
                return header[len(header_name) + 2:]
        return ''

    def connect_target(self, host):
        try:
            host, port = (host.split(':') + [443])[:2]
            port = int(port)
            addr_info = socket.getaddrinfo(host, port)[0]
            self.target = socket.socket(addr_info[0], addr_info[1], addr_info[2])
            self.target.connect(addr_info[4])
            self.targetClosed = False
        except Exception as e:
            self.server.printLog(f"Error connecting to target {host}:{port} - {e}")
            self.client.sendall(b'HTTP/1.1 502 Bad Gateway\r\n\r\n')
            self.close()

    def method_CONNECT(self, path):
        self.log += f' - CONNECT {path}'
        self.connect_target(path)
        self.client.sendall(RESPONSE.encode('utf-8'))
        self.client_buffer = b''
        self.server.printLog(self.log)
        self.doCONNECT()

    def doCONNECT(self):
        socs = [self.client, self.target]
        count = 0
        while True:
            count += 1
            recv, _, err = select.select(socs, [], socs, 3)
            if err:
                break
            if recv:
                for s in recv:
                    try:
                        data = s.recv(BUFLEN)
                        if not data:
                            break
                        if s is self.target:
                            self.client.send(data)
                        else:
                            while data:
                                sent = self.target.send(data)
                                data = data[sent:]
                        count = 0
                    except Exception as e:
                        self.server.printLog(f"Data transfer error: {e}")
                        break
            if count >= TIMEOUT:
                break

def print_usage():
    print('Usage: proxy.py -p <port>')
    print('       proxy.py -b <bindAddr> -p <port>')
    print('       proxy.py -b 0.0.0.0 -p 80')

def parse_args(argv):
    global LISTENING_ADDR, LISTENING_PORT
    try:
        opts, _ = getopt.getopt(argv, "hb:p:", ["bind=", "port="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-b", "--bind"):
            LISTENING_ADDR = arg
        elif opt in ("-p", "--port"):
            LISTENING_PORT = int(arg)

def main():
    print("\n:-------PythonProxy-------:\n")
    print(f"Listening addr: {LISTENING_ADDR}")
    print(f"Listening port: {LISTENING_PORT}\n")
    print(":-------------------------:\n")
    server = Server(LISTENING_ADDR, LISTENING_PORT)
    server.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print('Stopping...')
        server.close()

if __name__ == '__main__':
    parse_args(sys.argv[1:])
    main()
