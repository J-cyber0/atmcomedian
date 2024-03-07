import os
import logging
import asyncpg
import dotenv
import asyncio

class Database:
    def __init__(self):
        self.postgres_connection = None

    async def connect_to_postgresql(self):
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
            self.postgres_connection = await asyncpg.connect(
                host=host, port=port, database=database, user=user, password=password
            )
            print("Successfully connected to PostgreSQL database.")
        except asyncpg.PostgresError as e:
            logging.error(f"\nError connecting to PostgreSQL database: {e}")

    async def create_postgresql_tables(self):
        try:
            if self.postgres_connection:
                # Create users table
                await self.postgres_connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL                
                    )
                    """
                )

                # Create transactions table
                await self.postgres_connection.execute(
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
                await self.postgres_connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS wallets (
                        id SERIAL PRIMARY KEY,
                        wallet_name VARCHAR(255) NOT NULL,
                        private_key VARCHAR(255) NOT NULL,
                        wallet_address VARCHAR(255) NOT NULL,
                        nft_collection VARCHAR(255) NOT NULL,
                        balance NUMERIC NOT NULL,
                        currency VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                    """
                )

                # Create NFTs table
                await self.postgres_connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS nfts (
                    id SERIAL PRIMARY KEY,
                    collection_name VARCHAR(255) NOT NULL,
                    collection_description VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
                )

                # Create Royalty Wallets table
                await self.postgres_connection.execute(
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

                print("PostgreSQL tables created successfully.")
            else:
                print("PostgreSQL connection is not established.")
        except asyncpg.PostgresError as e:
            logging.error(f"\nError creating PostgreSQL tables: {e}")

    async def store_user_credentials(self, username, password):
        try:
            # PostgreSQL
            await self.postgres_connection.execute(
                """
                INSERT INTO users (username, password)
                VALUES ($1, $2)
                """,
                username, password
            )
            print("User credentials inserted successfully.")
            return True
        except Exception as e:
            logging.error(f"\nError inserting data: {e}")
            return False

    async def store_nft_collection_info(self, collection_name, collection_description):
        try:
            # PostgreSQL
            await self.postgres_connection.execute(
                """
                INSERT INTO nfts (collection_name, collection_description)
                VALUES ($1, $2)
                """,
                collection_name, collection_description
            )
            print("NFT collection info stored successfully.")
            return True
        except Exception as e:
            logging.error(f"\nError inserting data: {e}")
            return False
        
    async def store_royalty_wallets(self, current_collection, wallet):
        try:
            # PostgreSQL
            await self.postgres_connection.execute(
                """
                INSERT INTO royalty_wallets (wallet_name, nft_collection, wallet_address)
                VALUES ('eth', $1, $2)
                """,
                current_collection, wallet
            )
            return True
        except Exception as e:
            logging.error(f"\nError inserting data: {e}")
            return False

    async def query_nft_collection_info(self, nft_collection_name):
        try:
            # PostgreSQL
            return await self.postgres_connection.fetch(
                """
                SELECT * FROM nfts WHERE collection_name = $1
                """,
                nft_collection_name
            )
        except Exception as e:
            logging.error(f"\nError querying data: {e}")
            return False
        
    async def query_royalty_wallets(self):
        try:
            # PostgreSQL
            return await self.postgres_connection.fetch(
                """
                SELECT * FROM royalty_wallets
                """
            )
        except Exception as e:
            logging.error(f"\nError querying data: {e}")
            return False

    async def insert_wallet_data(self, wallet):
        try:
            # Check if the database connection is properly initialized
            if self.postgres_connection is None:
                logging.error("Database connection is not initialized.")
                return
            
            # PostgreSQL
            if wallet:
                await self.postgres_connection.execute(
                    """
                    INSERT INTO wallets (wallet_name, private_key, wallet_address)
                    VALUES ($1, $2, $3)
                    """,
                    wallet['wallet_name'], wallet['private_key'], wallet['wallet_address']
                )
            print("Wallet inserted successfully.")
        except Exception as e:
            logging.error(f"\nError inserting data: {e}")

    async def query_wallet_info(self, nft_collection_name):
        try:
            # PostgreSQL
            return await self.postgres_connection.fetch(
                """
                SELECT * FROM wallets WHERE nft_collection = $1
                """,
                nft_collection_name
            )
        except Exception as e:
            logging.error(f"\nError querying data: {e}")

    async def insert_transaction(self, transaction):
        try:
            # PostgreSQL
            if transaction:
                await self.postgres_connection.execute(
                    """
                    INSERT INTO transactions (sender_address, receiver_address, amount, ciphertext, nonce, tag)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    transaction['sender_address'], transaction['receiver_address'], transaction['amount'], transaction['ciphertext'], transaction['nonce'], transaction['tag']
                )
            print("Transaction inserted successfully.")
        except Exception as e:
            logging.error(f"\nError inserting data: {e}")

    async def get_transactions(self, wallet_address):
        try:
            # PostgreSQL
            return await self.postgres_connection.fetch(
                """
                SELECT * FROM transactions WHERE receiver_address = $1
                """,
                wallet_address
            )
        except Exception as e:
            logging.error(f"\nError querying data: {e}")
            return None

    async def close_connections(self):
        try:
            # Close the PostgreSQL connection
            if self.postgres_connection:
                await self.postgres_connection.close()

        except Exception as e:
            logging.error(f"\nError closing connection: {e}")
   
async def main():
    database = Database()
    await database.connect_to_postgresql()
    await database.create_postgresql_tables()
    await database.close_connections()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted, closing gracefully...")
