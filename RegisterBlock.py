from flask import Flask
from ChainRegister import ChainRegister
from threading import Lock, Thread
import db

def run_register():
    # Thread with register
    with Lock():
        register = ChainRegister()
        new_block_id, txs_hashes = db.get_txs_for_new_block()
        # print(txs_hashes)
        register.register_block(new_block_id, txs_hashes)

if __name__=="__main__":
    run_register()
