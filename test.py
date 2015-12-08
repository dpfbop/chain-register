import db
from hashlib import sha256
from random import random
from time import time

hashes = []
shop_ids = []
# generate N transactions
# N = 10**8
# for i in range(N):
#     _hash = sha256(str(i).encode())
#     shop_ids.append(int(random()*10000))
#     hashes.append(_hash.hexdigest())
#     if i % 10**5 == 0:
#         print(i)
#         db.test_save_txs(shop_ids, hashes)
#         hashes = []
#         shop_ids = []
#         print("OK")

start = time()
_hash = sha256(str(100000000).encode())
# print(db.get_block_by_tx_hash(_hash.hexdigest()))
# db.save_tx(int(random()*10000), _hash.hexdigest())
print(time() - start)
