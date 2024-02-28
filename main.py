import os
import dotenv
from agents.monitor_wallet import read_settings, send
from modules.cli import wallet_setup as cli_wallet_setup
from modules.database import Database

db = Database()

def wallet_setup():
    return cli_wallet_setup()

def main():
    # Call the function to store the database data in the .env file
    store_db_data()
    # Proceed with wallet setup
    new_wallet = main_wallet_setup()
    if new_wallet:
        print("Wallet setup successful.")
    else:
        print("Wallet setup failed.")

def store_db_data():
    print("Please enter the database configuration:")
    postgres_host = input("Postgres host: ")
    postgres_port = input("Postgres port: ")
    postgres_database = input("Postgres database: ")
    postgres_user = input("Postgres username: ")
    postgres_pass = input("Enter your Postgres password: ")

    # Create the database configuration string
    db_config_str = f"POSTGRES_HOST={postgres_host}\n" \
                    f"POSTGRES_PORT={postgres_port}\n" \
                    f"POSTGRES_DATABASE={postgres_database}\n" \
                    f"POSTGRES_USER={postgres_user}\n" \
                    f"POSTGRES_PASSWORD={postgres_pass}\n"

    # Path to the .env file
    env_file_path = "./.env"

    # Write the database configuration to the .env file
    with open(env_file_path, "w") as env_file:
        env_file.write(db_config_str)

    print("Database configuration saved to .env file")

    # Load the environment variables from the .env file
    dotenv.load_dotenv()

def main_wallet_setup():
    private_key = input("Enter your private key: ")
    wallet_address = input("Enter the address to withdraw funds from: ")
    infura_url = input("Enter your Infura URL: ")

    # Create a new wallet with the provided information
    wallet = {
        "wallet_name": "eth",
        "private_key": private_key,
        "wallet_address": wallet_address,
        "infura_url": infura_url
    }

    # Start the wallet monitor agent with the new wallet
    store_wallet(wallet)
    return wallet

def store_wallet(wallet):
    db.insert_wallet_data(wallet)
    print("Storing wallet info...")

if __name__ == "__main__":
    main()
