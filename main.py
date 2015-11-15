from blockcypher import embed_data
from blockcypher import get_transaction_details


class ChainRegister:

    def __init__(self, key="478e16e4aeee8e5aa9e5c9a1f6c978fe"):
        self.key = key

    def register_purchase(self, data):
        return embed_data(to_embed=data, api_key=self.key, data_is_hex=False)
        
# print(get_transaction_details('9e200a1dbd89392abb429978e7c569d8a76f74195c15fa04d62666f7f6bbaa74'))