from blockcypher import embed_data
from hashlib import sha256, md5
from blockcypher import get_transaction_details
import datetime
import binascii

class MerkleTree(object):

    def __init__(self, hashes=[]):   
        self.hashes = hashes


    def calc_root_hash(self): 
        if len(self.hashes) == 0:
            return None
        hashes_on_level = [bytes(bytearray.fromhex(hash)) for hash in self.hashes]
        while len(hashes_on_level) > 1:
            n = len(hashes_on_level)
            new_hashes_on_level = []
            for current in range(0, n, 2):
                if current == n - 1:
                    new_hash = hashes_on_level[current]
                else:
                    new_hash = sha256(b"\x01" + hashes_on_level[current] + hashes_on_level[current + 1])
                    new_hash = bytes(bytearray.fromhex(new_hash.hexdigest()))
                new_hashes_on_level.append(new_hash)
            hashes_on_level = new_hashes_on_level
        root_hash = hashes_on_level[0]
        return binascii.hexlify(root_hash)

