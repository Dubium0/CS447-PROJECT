import socket
import os

def create_file(file_size=1024):
    with open('received_file2', 'wb') as f:
        f.seek(file_size - 1)
        f.write(b'\0')

    bytes_received = 0
    with open('received_file2', 'r+b') as f:
        while bytes_received < file_size:
            data = b'AAA'
            if not data:
                break
            f.write(data)
            bytes_received += len(data)
            print(f"[*] Receiving... {bytes_received}/{file_size} bytes")
    
    print("[+] File transfer complete.")

if __name__ == "__main__":
    create_file()
