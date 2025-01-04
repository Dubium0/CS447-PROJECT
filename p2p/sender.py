import socket
import os

def send_file(server_ip, port=5000, file_path='file_to_send.txt'):
    if not os.path.exists(file_path):
        print(f"[!] File '{file_path}' not found.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"[+] Connected to {server_ip}:{port}")

    with open(file_path, 'rb') as f:
        while (chunk := f.read(4096)):
            client_socket.send(chunk)
            print("[*] Sending...")
    
    print("[+] File transfer complete.")
    client_socket.close()

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    file_path = input("Enter path to file: ")
    send_file(server_ip, file_path=file_path)
