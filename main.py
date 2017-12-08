import hashlib as hasher
import random, string, pickle

class Block:
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()

	def hash_block(self):
		sha = hasher.sha256()
		sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
		return sha.hexdigest()


class Node(Block):
	def __init__(self, index, timestamp, data, previous_hash):
		self.proof_key = ""
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()


	def hash_block(self):
		sha = hasher.sha256()
		i = 1
		hash = ""
		while "000000" not in hash:
			print("Attempt {}".format(i))
			key = ''.join(
				random.choice(string.ascii_lowercase) for _ in range(random.randint(0,32)))
			print("    Key: {}".format(key))
			sha.update(str(hash).encode('utf-8') + key.encode('utf-8'))
			hash = sha.hexdigest()
			i += 1
		self.proof_key = key
		return hash

import datetime as date

def create_genesis_block():
	return Block(0, date.datetime.now(), "Genesis Block", 0)

def next_block(last_block, data: str):
	this_index = last_block.index + 1
	this_timestamp = date.datetime.now()
	this_data = data
	this_hash = last_block.hash

	return Block(this_index, this_timestamp, this_data, this_hash)

def next_node(last_node, data: str):
	this_index = last_node.index + 1
	this_timestamp = date.datetime.now()
	this_data = data
	this_hash = last_node.hash

	return Node(this_index, this_timestamp, this_data, this_hash)

def new_blockchain():
	blockchain = [create_genesis_block()]
	previous_block = blockchain[0]

	while len(blockchain) < 4:
		editor = input("Who is this editor? ")

		block_to_add = next_block(previous_block, editor)
		blockchain.append(block_to_add)
		previous_block = block_to_add

		print("Block for {} has been added".format(editor))
		print("    Hash: {}".format(block_to_add.hash))
	return blockchain


if __name__ == "__main__":
	chains = [create_genesis_block()]
	previous_node = chains[0]

	while(1):
		blockchain = new_blockchain()

		node_to_add = next_node(previous_node, pickle.dumps(blockchain))
		chains.append(node_to_add)
		previous_node = node_to_add

		print("Added node {} after finding key '{}'".format(len(chains)-1, node_to_add.proof_key))
		print("    Hash: {}".format(node_to_add.hash))






