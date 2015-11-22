from MerkleTree import MerkleTree

tree = MerkleTree((["abab", "bacd", "cd2d", "25d1", "23", "0123456789abcd" ]))
print(tree.calc_root_hash())