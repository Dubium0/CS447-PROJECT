import socket

def receive_file(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Listening for file transfer on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"[+] Connection from {addr}")

    with open('received_file', 'wb') as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)
            print("[*] Receiving...")
    
    print("[+] File transfer complete.")
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    receive_file()
