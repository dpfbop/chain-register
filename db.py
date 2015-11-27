from pymongo import MongoClient
from datetime import datetime


def __init_last_block_id():
    entry = __settings.find_one()
    if entry is None:
        return -1
    return entry["last_block_id"]

__mongo = MongoClient()
__db = __mongo.chainregister_database
__transactions = __db.transactions
__blocks = __db.blocks
__settings = __db.settings
__blocks.drop()
__transactions.drop()
__settings.drop()
__last_block_id = __init_last_block_id()


def __get_block(block_id):
    global __blocks
    return __blocks.find({"block_id": block_id})


def __set_last_block_id(val):
    global __last_block_id, __settings
    if val < __last_block_id:
        raise ValueError("val should be more than" + str(__last_block_id))
    if __last_block_id == -1:
        __settings.insert({"last_block_id": val})
    else:
        __settings.update_one({"last_block_id": __last_block_id},
                              {"$set": {"last_block_id": val}})
    __last_block_id = val


def save_tx(shop_id, hash):
    global __transactions
    __transactions.insert({'shop_id': shop_id, 'hash': hash, "block": -1,
                           "date": datetime.utcnow()})


def get_txs_for_new_block():
    global __transactions, __last_block_id
    result = []
    need_to_be_updated_ids = []
    new_block_id = __last_block_id + 1
    for tx in __transactions.find({"block": new_block_id}):
        # find txs which were taken, but block with them wasn't saved
        result.append(tx["hash"])
    for tx in __transactions.find({"block": -1}):
        # find new txs
        result.append(tx["hash"])
        need_to_be_updated_ids.append(tx["_id"])
    __transactions.update_many({"_id": {"$in": need_to_be_updated_ids}},
                               {"$set": {"block": new_block_id}})
    return new_block_id, result


def save_block(block_id, root_hash, blockchain_tx_hash, txs):
    global __blocks
    __set_last_block_id(block_id)
    __blocks.insert({"block_id": block_id, "root_hash": root_hash,
                     "blockchain_tx_hash": blockchain_tx_hash, "txs": txs})


def get_block_by_tx_hash(tx_hash):
    tx = __transactions.find_one({"hash": tx_hash})
    if tx is None:
        return None
    block_id = tx["block"]
    block = __blocks.find_one({"block_id": block_id})
    return block

