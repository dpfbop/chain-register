from blockcypher import embed_data
from hashlib import sha256, md5
from blockcypher import get_transaction_details


class ChainRegister:

    def __init__(self, salt="hack4people", token="478e16e4aeee8e5aa9e5c9a1f6c978fe"):
        '''
        :param salt: secret word
        :param key: API key for blockcypher
        :return: hash of transaction
        '''
        self.key = token
        self.salt = salt

    def salt_to_num(self):
        return int(md5(self.salt.encode("urf-8")).hexdigest()) % 10**9

    def register_purchase(self, id, amount, price):
        numSalt = self.salt_to_num
        n1 = str((int(id) ^ numSalt).decode('hex'))
        n2 = str((int(amount) ^ numSalt).decode('hex'))
        n3 = str((int(price) ^ numSalt).decode('hex'))
        data = 'bbbb' + n1 + 'bb' + n2 + 'bb' + n3
        print(data)
        return embed_data(to_embed=data, api_key=self.key, data_is_hex=False)

    def decode_hash(self, hash):
        data = hash[4:]
        nums = data.split('bb')
        if len(nums) != 3:
            return -1
        numSalt = self.salt_to_num()
        id = int(nums[0], 16) ^ numSalt
        amount = int(nums[1], 16) ^ numSalt
        price = int(nums[2], 16) ^ numSalt
        return id, amount, price


# print(get_transaction_details('9e200a1dbd89392abb429978e7c569d8a76f74195c15fa04d62666f7f6bbaa74'))
