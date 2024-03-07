import os
import psycopg2
import dotenv

class Database:
    def __init__(self):
        self.postgres_connection = None

    def connect_to_postgresql(self):
        try:
            # Load environment variables from .env file
            dotenv.load_dotenv()

            # Get PostgreSQL connection details from environment variables
            host = os.environ.get("POSTGRES_HOST")
            port = os.environ.get("POSTGRES_PORT")
            database = os.environ.get("POSTGRES_DATABASE")
            user = os.environ.get("POSTGRES_USER")
            password = os.environ.get("POSTGRES_PASSWORD")

            # Connect to PostgreSQL
            self.postgres_connection = psycopg2.connect(
                host=host, port=port, database=database, user=user, password=password
            )
            print("Successfully connected to PostgreSQL database.")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def create_postgresql_tables(self):
        try:
            cursor = self.postgres_connection.cursor()

            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL                
                )
                """
            )

            # Create transactions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    sender_address VARCHAR(255) NOT NULL,
                    receiver_address VARCHAR(255) NOT NULL,
                    amount NUMERIC NOT NULL,
                    hash VARCHAR(255) NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    ciphertext VARCHAR(255) NOT NULL,
                    nonce VARCHAR(255) NOT NULL,
                    tag VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )

            # Create wallets table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    id SERIAL PRIMARY KEY,
                    wallet_name VARCHAR(255) NOT NULL,
                    private_key VARCHAR(255) NOT NULL,
                    wallet_address VARCHAR(255) NOT NULL,
                    nft_collection VARCHAR(255) NOT NULL,
                    infura_url VARCHAR(255) NOT NULL,
                    balance NUMERIC NOT NULL,
                    currency VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )

            # Create NFTs table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS nfts (
                id SERIAL PRIMARY KEY,
                collection_name VARCHAR(255) NOT NULL,
                collection_description VARCHAR(255) NOT NULL
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
            )

            # Create Royalty Wallets table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS royalty_wallets (
                id SERIAL PRIMARY KEY,
                wallet_name VARCHAR(255) NOT NULL,
                wallet_address VARCHAR(255) NOT NULL,
                nft_collection VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
            )

            self.postgres_connection.commit()
            cursor.close()
            print("PostgreSQL tables created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating PostgreSQL tables: {e}")

    def store_user_credentials(self, username, password):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                """,
                (username, password)
            )
            self.postgres_connection.commit()
            cursor.close()
            print("User credentials inserted successfully.")
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False

    def store_nft_collection_info(self, collection_name, collection_description):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                INSERT INTO nfts (collection_name, collection_description)
                VALUES (%s, %s)
                """,
                (collection_name, collection_description)
            )
            self.postgres_connection.commit()
            cursor.close()
            print("NFT collection info stored successfully.")
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        
    def store_royalty_wallets(self, current_collection, wallet):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                INSERT INTO royalty_wallets (wallet_name, nft_collection, wallet_address)
                VALUES (%s, %s, %s)
                """,
                ('eth', current_collection, wallet)
            )
            self.postgres_connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False


    def query_nft_collection_info(self, nft_collection_name):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM nfts WHERE collection_name = %s
                """,
                (nft_collection_name)
            )
            nfts = cursor.fetchall()
            cursor.close()
            return nfts
        except Exception as e:
            print(f"Error querying data: {e}")
            return False
        
    def query_royalty_wallets(self):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM royalty_wallets
                """
            )
            wallets = cursor.fetchall()
            cursor.close()
            return wallets
        except Exception as e:
            print(f"Error querying data: {e}")
            return False

    def insert_wallet_data(self, wallet):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()

            if wallet:
                cursor.execute(
                    """
                    INSERT INTO wallets (wallet_name, private_key, wallet_address, infura_url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (wallet['wallet_name'], wallet['private_key'], wallet['wallet_address'], wallet['infura_url'])
                )

            self.postgres_connection.commit()
            cursor.close()

            print("Wallet inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")


    async def query_wallet_info(self, nft_collection_name):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()

            cursor.execute(
                """
                SELECT * FROM wallets WHERE nft_collection = %s
                """,
                (nft_collection_name,)
            )

            wallets = cursor.fetchall()
            cursor.close()
            return wallets
        except Exception as e:
            print(f"Error querying data: {e}")



    def insert_transaction(self, transaction):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()

            if transaction:
                cursor.execute(
                    """
                    INSERT INTO transactions (sender_address, receiver_address, amount, ciphertext, nonce, tag)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (transaction['sender_address'], transaction['receiver_address'], transaction['amount'], transaction['ciphertext'], transaction['nonce'], transaction['tag'])
                )
            self.postgres_connection.commit()
            cursor.close()
            print("Transaction inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def get_transactions(self, wallet_address):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM transactions receiver_address = %s
                """,
                (wallet_address)
            )
            transactions = cursor.fetchall()
            print(f"PostgreSQL transactions: {transactions}")
            cursor.close()
            return transactions
        except Exception as e:
            print(f"Error querying data: {e}")
            return None
   

    def close_connections(self):
        try:
            # Close the PostgreSQL connection
            if self.postgres_connection:
                self.postgres_connection.close()

        except Exception as e:
            print(f"Error closing connection: {e}")
   
if __name__ == "__main__":
    try:
        database = Database()
        database.connect_to_postgresql()
        database.create_postgresql_tables()
    finally:
        database.close_connections()
