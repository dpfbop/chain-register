from blockcypher import embed_data
from hashlib import md5
from blockcypher import get_transaction_details


class ChainRegister:
    def __init__(self, salt, token="478e16e4aeee8e5aa9e5c9a1f6c978fe"):
        '''
        :param salt: secret word
        :param key: API key for blockcypher
        :return: hash of transaction
        '''
        self.key = token
        self.salt = salt

    def salt_to_num(self):
        return int(md5(self.salt.encode("utf-8")).hexdigest(), 16) % 10**9

    def register_purchase(self, id, amount, price):
        numSalt = self.salt_to_num()
        n1 = str(hex(int(id) ^ numSalt))
        n2 = str(hex(int(amount) ^ numSalt))
        n3 = str(hex(int(price) ^ numSalt))
        data = n1 + 'bbbb' + n2 + 'bbbb' + n3
        return embed_data(to_embed=data, api_key=self.key, data_is_hex=False)['hash']

    def decode_hash(self, mHash):
        print(mHash)
        nums = mHash.split('bbbb')
        print(nums)
        if len(nums) != 3:
            return -1
        numSalt = self.salt_to_num()
        id = int(nums[0], 16) ^ numSalt
        amount = int(nums[1], 16) ^ numSalt
        price = int(nums[2], 16) ^ numSalt
        return id, amount, price

    def get_data_from_tx(self, txs):
        print(txs)
        transaction = get_transaction_details(txs)
        for x in transaction['outputs']:
            if x['script_type'] == 'null-data':
                print(x)
                return x['data_string'], transaction['received']

    def get_transaction(self, tx_hash):
        print(tx_hash)
        data, mTime = self.get_data_from_tx(tx_hash)
        record = self.decode_hash(data)
        return {'product_id': record[0],
                         'amount': record[1],
                                   'price': record[2],
                                            'date': mTime.strftime('%c')}

    def get_page_with_transactions(self, txs):
        transactions = [self.get_transaction(tx['hash']) for tx in txs]
        return {'count': len(transactions), 'transactions': transactions}

