import MySQLdb
from Configs import Configs
from datetime import datetime


def __init_last_block_id():
    # TODO: check
    global __cursor
    __cursor.execute("SELECT last_block_id FROM " + __settings + ";")
    entry = __cursor.fetchone()
    if entry is None:
        return -1
    return entry["last_block_id"]

__db = MySQLdb.connect(user=Configs.user, passwd=Configs.password)
__cursor = __db.cursor()
__cursor.execute("CREATE DATABASE IF NOT EXISTS " + Configs.db_name)
__cursor.execute("USE " + Configs.db_name)
# transactions
__shop_id = "shop_id"
__block_id = "block_id"
__hash = "hash"
__date = "date"
# blocks
__root_hash = "root_hash"
__blockchain_tx_hash = "blockchain_tx_hash"
# Tables
__transactions = "transactions"
__blocks = "blocks"
__settings = "settings"
__query = "CREATE TABLE IF NOT EXISTS " + __transactions + "(" +\
          __shop_id + " INT UNSIGNED, " +\
          __hash + " CHAR(64), " +\
          __block_id + " INT UNSIGNED, " +\
          __date + " TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);"
__cursor.execute(__query)
__query = "CREATE TABLE IF NOT EXISTS " + __blocks + "(" +\
          __block_id + " INT UNSIGNED, " +\
          __root_hash + " CHAR(64), " +\
          __blockchain_tx_hash + " CHAR(64));"

__cursor.execute(__query)
__query = "CREATE TABLE IF NOT EXISTS " + __settings + "(last_block_id INT UNSIGNED);"
__cursor.execute(__query)
# init last block id from DB
__last_block_id = __init_last_block_id()


def __get_block(block_id):
    # TODO: check
    global __cursor
    __cursor.execute("SELECT " + __root_hash + "," +
                     __blockchain_tx_hash + " FROM " + __blocks +
                     " WHERE " + __block_id + " = " + str(block_id) + ";")
    result = __cursor.fetchone()
    return {"root_hash": result[0], "blockchain_tx_hash": result[1]}


def __set_last_block_id(val):
    # TODO: check
    global __last_block_id, __cursor
    if val < __last_block_id:
        raise ValueError("val should be more than" + str(__last_block_id))
    if __last_block_id == -1:
        __cursor.execute("INSERT INTO " + __settings + " VALUES (" + str(val) + ");")
    else:
        __cursor.execute("UPDATE " + __settings + " SET last_block_id = " + str(val) + ";")
    __last_block_id = val


def save_tx(shop_id, _hash):
    # TODO: check
    global __cursor
    __cursor.execute("INSERT INTO " + __transactions + " VALUES (" +
                     str(shop_id) + ", " + _hash + ", -1);")


def get_txs_for_new_block():
    # TODO: need to rewrite!!!
    global __cursor
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
    # TODO: check
    global __cursor
    __set_last_block_id(block_id)
    __cursor.execute("INSERT INTO " + __blocks + " VALUES (" +
                     block_id, ", " + root_hash + ", " + blockchain_tx_hash + ");")


def get_block_by_tx_hash(tx_hash):
    # TODO: check
    global __cursor
    __cursor.execute("SELECT " + __block_id + " FROM " + __transactions +
                     " WHERE " + __hash + " = " + tx_hash + ";")
    tx = __cursor.fetchone()
    if tx is None:
        return None
    return __get_block(tx[0])

