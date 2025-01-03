def read_offset(file_path, piece_index, piece_length, file_length, num_of_pieces):

    if piece_index < 0 or piece_index >= num_of_pieces:
        raise ValueError("Invalid piece index. Must be between 0 and num_of_pieces - 1.")
    
    start_offset = piece_index * piece_length

    if piece_index == num_of_pieces - 1: 
        piece_length = file_length - start_offset 
    
    with open(file_path, 'rb') as file:
        file.seek(start_offset)
        data = file.read(piece_length) 

    return data 