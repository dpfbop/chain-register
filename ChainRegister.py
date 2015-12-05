from blockcypher import embed_data
from blockcypher import get_transaction_details
from MerkleTree import MerkleTree
import db


class ChainRegister(object):
    def __init__(self, token="478e16e4aeee8e5aa9e5c9a1f6c978fe"):
        self.key = token

    def register_block(self, new_block_id: int, txs_hashes: list):
        # saving root_hash in blockchain
        if len(txs_hashes) == 0:
            return None
        tree = MerkleTree(txs_hashes)
        root_hash = tree.calc_root_hash()
        blockchain_tx_hash = None
        try:
            blockchain_tx_hash = embed_data(to_embed=root_hash, api_key=self.key)['hash']
            db.save_block(new_block_id, root_hash, blockchain_tx_hash, txs_hashes)
        except:
            print("Connection Error")
        finally:
            return blockchain_tx_hash

    @staticmethod
    def get_data_from_tx(txs):
        transaction = get_transaction_details(txs)
        for x in transaction['outputs']:
            if x['script_type'] == 'null-data':
                print(x)
                return x['data_string'], transaction['received']
