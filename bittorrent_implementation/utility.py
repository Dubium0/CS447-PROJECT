from enum import Enum

class Result(Enum):
    SUCCESS = 1
    FAILURE = 0


def split_bytes(data, length): 
    for i in range(0, len(data), length): 
        yield  int.from_bytes(data[i:i + length], byteorder= 'big')