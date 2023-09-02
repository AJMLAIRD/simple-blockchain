import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain.

        :param proof: Proof of work for the new block
        :param previous_hash: Hash of the previous block
        :return: New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined block.

        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: Amount
        :return: Index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Hash a block using SHA-256.

        :param block: Block
        :return: Hash
        """
        # Ensure the dictionary is ordered to have consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

# Instantiate the blockchain
blockchain = Blockchain()

# Create some example transactions
blockchain.new_transaction("Alice", "Bob", 2.5)
blockchain.new_transaction("Bob", "Charlie", 1.0)
blockchain.new_transaction("Charlie", "David", 0.5)

# Mine a new block
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = Blockchain.proof_of_work(last_proof)
blockchain.new_transaction(sender="0", recipient="Miner", amount=1)
block = blockchain.new_block(proof)

# Print the blockchain
print("Blockchain:")
print(json.dumps(blockchain.chain, indent=2))
