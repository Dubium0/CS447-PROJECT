import shutil
import hashlib

def check_disk_space(path : str, required_size : int)->bool:
    stat = shutil.disk_usage(path)
    free_space = stat.free
    if free_space < required_size:
        print(f"Not enough space. Required: {required_size}, Available: {free_space}")
        return False
    print(f"Enough space available: {free_space}")
    return True

    
def verify_piece(file_path :str, piece_index : int ,piece_size :int, expected_hash:bytes) -> bool:
    with open(file_path, 'rb') as f:
        f.seek(piece_index * piece_size)
        piece_data = f.read(piece_size)
        piece_hash = hashlib.sha1(piece_data).digest()
        return piece_hash == expected_hash


def verify_file_integrity(check_pieces : list[tuple[int,bytes]], piece_length : int,file_to_check_path : str):

    corrupted_pieces = []
    for tuple  in check_pieces:
        i  = tuple[0]
        expected_hash = tuple[1]
        if not verify_piece(file_to_check_path, i, piece_length, expected_hash):
            corrupted_pieces.append(i)
    return corrupted_pieces



