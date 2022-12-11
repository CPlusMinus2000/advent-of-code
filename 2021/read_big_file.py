
# This file is so fat

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


with open('memo.txt') as f:
    i = 0
    for piece in read_in_chunks(f):
        print(piece)
        i += 1

        if i > 1000:
            break