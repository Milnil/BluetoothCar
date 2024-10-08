import socket
import time

server_addr = 'D8:3A:DD:F8:70:E3'  # Make sure this is your Raspberry Pi's Bluetooth address
server_port = 1
buf_size = 1024

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((server_addr, server_port))
print("Connected to the Raspberry Pi")

try:
    for i in range(10):  # Send 10 messages
        message = f"PC {i}\r\n"
        sock.send(message.encode('utf-8'))
        print(f"Sent: {message.strip()}")
        
        data = sock.recv(buf_size)
        print(f"Received: {data.decode('utf-8').strip()}")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    sock.close()
    print("Disconnected")
    print("All done.")