import socket

HOST = "192.168.72.176"  # Standard loopback interface address (localhost)
PORT = 8081  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("Waiting for connection")
        conn, addr = s.accept()
        with conn:
            print(f"\nConnected by {addr}")
            print("ESP32 Message: ")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # conn.sendall(data)
                print(f"%s" % data.decode("utf-8"), end='')
                data_send = bytes(input("ESP32 Command: "), "utf-8")
                conn.sendall(data_send)