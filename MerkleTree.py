from blockcypher import embed_data
from hashlib import sha256, md5
from blockcypher import get_transaction_details
import datetime

class MerkleTree(object):

    def __init__(self, hashes=[]):   
        self.hashes = hashes


    def calc_root_hash(self): 
        size = len(self.hashes)
        if size == 0:
            return None

        hashes_on_level = [bytes(bytearray.fromhex(hash)) for hash in self.hashes]
        

        while len(hashes_on_level) > 1:
            n = len(hashes_on_level)
            print(n)
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
        return root_hash
            

    def register_purchase(self, id, amount, price):
        numSalt = self.salt_to_num()
        n1 = str(hex(int(id) ^ numSalt))
        n2 = str(hex(int(amount) ^ numSalt))
        n3 = str(hex(int(price) ^ numSalt))
        data = 'bbbb' + n1 + 'bb' + n2 + 'bb' + n3
        return embed_data(to_embed=data, api_key=self.key, data_is_hex=False)['hash']


    def get_transaction(self, tx_hash):
        print(tx_hash)
        data, mTime = self.get_data_from_tx(tx_hash)
        record = self.decode_hash(data)
        return {'id': record[0],
                         'amount': record[1],
                                   'price': record[2],
                                            'date': mTime.strftime('%c')}

    def get_page_with_transactions(self, txs):
        return {'transactions': [self.get_transaction(tx['hash']) for tx in txs]}

