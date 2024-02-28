import os
from web3 import Web3
import psycopg2
from database import Database

db = Database()

class Payment:
        
    def __init__(self):
        self.web3 = self.connect_to_blockchain()
        self.transactions = []

    def connect_to_blockchain(self):
        return Web3(Web3.HTTPProvider("http://localhost:8545"))

    def create_transaction(self, recipient_address, amount):
        connected_to_blockchain = self.web3.isConnected()
        if connected_to_blockchain:
            transaction = {
                'to': recipient_address,
                'value': amount,
                'gas': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.web3.eth.default_account)
            }
            return transaction
        else:
            return None

    def monitor_transaction_status(self, transaction_hash):
        transaction_receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
        if transaction_receipt:
            return 'Confirmed' if transaction_receipt['status'] == 1 else 'Failed'
        else:
            return 'Pending'

    def generate_transaction(self, recipient_address, amount):
        return self.create_transaction(recipient_address, amount)

    def sign_transaction(self, transaction, private_key):
        signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key)
        return signed_transaction

    def submit_transaction(self, signed_transaction):
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return transaction_hash.hex()

    def store_transaction_details(self, transaction_hash, transaction_status):
        try:
            postgres_connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            postgres_cursor = postgres_connection.cursor()
            postgres_cursor.execute("INSERT INTO transactions (hash, status) VALUES (%s, %s)", (transaction_hash, transaction_status))
            postgres_connection.commit()
            print("Transaction details stored in PostgreSQL successfully!")
        except psycopg2.Error as e:
            print("Error storing transaction details in PostgreSQL:", e)

    def initiate_transaction(self, recipient_address, amount, private_key):
        transaction = self.create_transaction(recipient_address, amount)
        if transaction:
            signed_transaction = self.sign_transaction(transaction, private_key)
            transaction_hash = self.submit_transaction(signed_transaction)
            transaction_status = self.monitor_transaction_status(transaction_hash)
            self.store_transaction_details(transaction_hash, transaction_status)
            if transaction_status == 'Failed':
                print('Transaction failed.')
            print('Transaction status:', transaction_status)
        else:
            print('Failed to create transaction. Blockchain might not be reachable.')

if __name__ == '__main__':
    Payment().initiate_transaction('0x627306090abaB3A6e1400e9')
