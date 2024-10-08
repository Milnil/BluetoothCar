import socket
import threading
import signal
import time

server_port = 1
buf_size = 1024
client_sock = None
server_sock = None
exit_event = threading.Event()

def handler(signum, frame):
    exit_event.set()

signal.signal(signal.SIGINT, handler)

def start_server():
    global server_sock
    global client_sock
    global exit_event

    server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server_sock.bind(("", server_port))
    server_sock.listen(1)
    print("Waiting for connection...")

    client_sock, address = server_sock.accept()
    print(f"Accepted connection from {address}")

    while not exit_event.is_set():
        try:
            data = client_sock.recv(buf_size)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            
            # Echo the received data back to the client
            client_sock.send(data)
        except socket.error:
            break

    print("Disconnected")

server_thread = threading.Thread(target=start_server)
server_thread.start()

try:
    while not exit_event.is_set():
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by user")

exit_event.set()
if client_sock:
    client_sock.close()
if server_sock:
    server_sock.close()
print("All done.")