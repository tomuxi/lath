'''Class Chunk with primitive FIFO kind of byte buffer operations

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-11'''

class Chunk:
    '''Simple FIFO buffer'''
    def __init__(self):
        self.data = b""

    def push(self, data: bytes):
        '''Append data to buffer'''
        self.data += data

    def pop(self, separator: bytes):
        '''Take data from the front of the buffer until separator'''
        front, *tail = self.data.split(separator, maxsplit=1)
        if not tail:
            return None

        self.data = separator.join(tail)
        return front

    def pop_all(self):
        '''Take all data from the buffer'''
        remaining = self.data
        self.data = b""
        return remaining
