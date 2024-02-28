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
                    infura_url VARCHAR(255) NOT NULL,
                    balance NUMERIC NOT NULL,
                    currency VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )

            self.postgres_connection.commit()
            cursor.close()
            print("PostgreSQL tables created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating PostgreSQL tables: {e}")

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
        

    def query_wallet_data(self):
        try:
            # PostgreSQL
            cursor = self.postgres_connection.cursor()

            cursor.execute(
                """
                SELECT * FROM wallets WHERE wallet_name = 'eth'
                """
            )

            wallet = cursor.fetchone()
            print(f"PostgreSQL wallet: {wallet}")

            cursor.close()

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
