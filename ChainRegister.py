from blockcypher import embed_data
from blockcypher import get_transaction_details


class ChainRegister(object):
    def __init__(self, token="478e16e4aeee8e5aa9e5c9a1f6c978fe"):
        self.key = token

    def register_purchase(self, id, amount, price):
        data = ""
        return embed_data(to_embed=data, api_key=self.key, data_is_hex=False)['hash']

    @staticmethod
    def get_data_from_tx(txs):
        transaction = get_transaction_details(txs)
        for x in transaction['outputs']:
            if x['script_type'] == 'null-data':
                print(x)
                return x['data_string'], transaction['received']

