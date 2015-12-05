# test Merkle Tree
from MerkleTree import MerkleTree
from hashlib import sha256
from time import time
from pymongo import MongoClient
from datetime import datetime

# 10**4 hashes --> 0.05 - 0.06s
# 10**5 hashes --> 0.5 - 0.6s
# 10**6 hashes --> 5 - 6s
hashes = []
for i in range(10**3):
    _hash = sha256(str(i).encode())
    hashes.append(_hash.hexdigest())
start = time()
tree = MerkleTree((hashes))
root = tree.calc_root_hash()
print(time() - start)
print(root)
