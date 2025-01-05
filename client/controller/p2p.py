import socket
import threading
import hashlib
import time

def read_piece(file_path, piece_index, piece_length, file_length, num_of_pieces):

    if piece_index < 0 or piece_index >= num_of_pieces:
        raise ValueError("Invalid piece index. Must be between 0 and num_of_pieces - 1.")
    
    start_offset = piece_index * piece_length

    if piece_index == num_of_pieces - 1: 
        piece_length = file_length - start_offset 
    
    with open(file_path, 'rb') as file:
        file.seek(start_offset)
        data = file.read(piece_length) 

    return data

#Sender Function
def start_listening(port, pieceLength, fileLength, numOfPieces, source_path):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Listening for connections on port {port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connected by {addr}")
        handle_client(client_socket, pieceLength, fileLength, numOfPieces, source_path)

def calculate_sha1(byte_data):
    sha1 = hashlib.sha1()  
    sha1.update(byte_data)  
    return sha1.hexdigest()  

# def start_download(peer_ip, peer_port, torrentHash, total_pieces, file_size,file_to_write):
#     create_file('received_file', file_size)
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((peer_ip, peer_port))
#     client.send(torrentHash)
#     request = client.recv(1024)
#     if(request == b"1"):
#         for i in range(total_pieces):
#             piece = bytearray()
#             download_piece(client, (i).to_bytes(4, 'big'))
#             with open('received_file', 'r+b') as f:
#                 offset = i * (file_size // total_pieces)
#                 while True:
#                     request = client.recv(1024)
#                     if(request == b'3'):
#                         # print(piece)
#                         break
#                     else:
#                         print(request)
#                         piece.extend(request)
                        
#                         f.seek(offset)
#                         f.write(request)
#                         offset += len(request)
             
#             print(calculate_sha1(piece))

def download_piece_by_piece(peer_ip, peer_port, fileToWriteOn, pieceIndex, piece_length, torrentHash):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, int(peer_port)))
    
    response = client.recv(1024)
    if response != b"1":
        print("Peer rejected request.")
        client.close()
        return None

    client.send(pieceIndex.to_bytes(4, 'big'))

    piece = bytearray()
    while True:
        chunk = client.recv(1024)
        if chunk == b'3':  # End-of-piece signal
            break
        piece.extend(chunk)

    # if calculate_sha1(piece) == piece_hash:
    with open(fileToWriteOn, 'r+b') as f:
        offset = pieceIndex * piece_length
        f.seek(offset)
        f.write(piece)
    
    print(f"Piece {pieceIndex} written to file.")

    client.close()
    print(f"Downloaded piece {pieceIndex}")
    return piece

def download_file(peer_ip, peer_port, fileToWriteOn, piece_length, numOfPieces):
    for i in range(numOfPieces):
        download_piece_by_piece(peer_ip, peer_port, fileToWriteOn, i, piece_length)


def create_file(file_name, file_size):
    with open(file_name, 'wb') as f:
        f.seek(file_size - 1)
        f.write(b'\0')  # Write a single null byte at the end to set file size
    print(f"Created empty file '{file_name}' of size {file_size} bytes.")

def download_piece(client, piece):
    client.send(piece)

def send_data_in_chunks(client_socket, data, chunk_size=1024):
    offset = 0
    total_size = len(data)

    while offset < total_size:
        # Extract a chunk of the specified size (1KB by default)
        offset_inc = min(chunk_size, total_size - offset)
        chunk = data[offset:offset + offset_inc]
        
        # Send the chunk over the socket
        client_socket.send(chunk)
        print(f"{offset}/{total_size}")
        # Move the offset forward by the chunk size
        offset = offset + offset_inc
    time.sleep(0.1)
    client_socket.send(b"3")
    print(f"Sent {total_size} bytes in chunks of {chunk_size} bytes.")

# Handle Incoming Client Connections
def handle_client(client_socket, pieceLength, fileLength, numOfPieces, source_path):

    client_socket.send(b"1")
    file_path = source_path
    
    while True:
        request = client_socket.recv(4096)
        
        if not request:
            break  
        
        piece_index = int.from_bytes(request, 'big')
        print(f"Received piece request for index: {piece_index}")
        
        # Simulate reading and sending the piece
        data = read_piece(file_path, piece_index, pieceLength, fileLength, numOfPieces)
        send_data_in_chunks(client_socket, data)



#Main Program to Run Both Simultaneously
# if __name__ == "__main__":
#    #Get these from tracker server
#    listen_port = 6881
#    peer_ip = "52.90.158.48"
#    peer_port = 6881
#    pieceLength = 262144
#    fileLength = 714084 
#    numOfPieces = 3
#    create_file("received_file", fileLength)
#    fileToWriteOn = "received_file"
#    # Start Listening in a Separate Thread
#    threading.Thread(target=start_listening, args=(listen_port, pieceLength, fileLength, numOfPieces), daemon=True).start()

#    # Run this command when torrent is added
#    #download_file(peer_ip, peer_port, fileToWriteOn, pieceLength, numOfPieces)

#    while True:
#        pass