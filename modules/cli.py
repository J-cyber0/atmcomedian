import os
import dotenv
import asyncio
import click
from modules.security import SecurityModule
from modules.database import Database
from modules.payment import Payment

# Initialize the user database
user_db = {}

# Create an instance of the security module, passing the user database
security_module = SecurityModule(user_db=user_db)

# Initialize the database object
db = Database()

# Define the main CLI command group
@click.group()
def cli():
    pass

async def user_login():
    # Prompt for user credentials asynchronously
    print("Please enter your user credentials or enter 'new user' to create a new account:")
    
    # Asynchronous input for username
    username = await asyncio.to_thread(input, "Username: ")
    
    # Asynchronous input for password (hide_input=True is not supported asynchronously)
    password = await asyncio.to_thread(input, "Password: ")
    
    if not security_module.secure_login(username, password):
        print("Invalid username or password.")
        return None, None
    else:
        print("Successfully logged in.")
        # Store the user credentials in the database
        user_db["username"] = username
        user_db["password"] = password
        
        return username, password

    
async def is_user_logged_in():
    # Check if the user is logged in
    print("Checking if user is logged in...")
    if "username" in user_db and "password" in user_db:
        return True
    else:
        return False

    

# Define the "user setup" command
@click.command()
@click.option('--phrase', prompt='Enter command:', help='Enter a command.')
def process_command(phrase):
    if phrase.lower() == 'new user':
        user_setup()
    elif phrase.lower() == 'new wallet':
        wallet_setup()
    elif phrase.lower() == 'new nft collection':
        nft_collection_setup()
    else:
        print("Command not recognized.")

def user_setup():
    # Prompt for user credentials
    print("Create a new user")
    username = click.prompt("Username:")
    password = click.prompt("Password:", hide_input=True)
    confirm_password = click.prompt("Confirm Password:", hide_input=True)

    # Validate the password confirmation
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return None, None
    
    # Create the user account
    if security_module.create_user(username, password):
        print("User account created successfully.")
        configure_database()
    else:
        print("Failed to create user account. Please try again.")
    return None, None

def configure_database():
    # Prompt for user credentials
    print("Please enter the database connection details:")
    db_host = input("Database host: ")
    db_port = input("Database port: ")
    db_name = input("Database name: ")
    db_user = input("Database user: ")
    db_password = input("Database password: ")

    # Create the database configuration string
    db_config_str = f"POSTGRES_HOST={db_host}\n" \
                    f"POSTGRES_PORT={db_port}\n" \
                    f"POSTGRES_DATABASE={db_name}\n" \
                    f"POSTGRES_USER={db_user}\n" \
                    f"POSTGRES_PASSWORD={db_password}\n"

    # Path to the .env file
    env_file_path = "../.env"

    # Write the database configuration to the .env file
    with open(env_file_path, "w") as env_file:
        env_file.write(db_config_str)

    print("Database configuration saved to .env file")

    # Connect to the database
    db.connect_to_postgresql()
    print("Successfully connected to PostgreSQL database.")
    print("Creating tables...")
    db.create_postgresql_tables()

    # Load the environment variables from the .env file
    dotenv.load_dotenv()

    nft_collection_setup()
    return None, None

def nft_collection_setup(collection_name):
    # Prompt for user credentials
    print("Create a new NFT collection")
    collection_name = input("Enter the name of your NFT collection: ")
    collection_description = input("Enter a description for your NFT collection: ")
    print("Successfully connected to PostgreSQL database.")
    print("Storing NFT collection info...")
    db.store_nft_collection_info(collection_name, collection_description)
    return None, None

def get_nft_collection_info(collection_name):
    current_collection = db.query_nft_collection_info(collection_name)
    if current_collection == None:
        print("NFT collection not found.")
        return None, None
    wallet_setup(collection_name)
    return current_collection

def wallet_setup(self, collection_name): 
    # Prompt for user credentials
    print("Create a new wallet")
    private_key = input("Enter your private key: ")
    wallet_address = input("Enter the address to send funds to: ")
    infura_url = input("Enter your Infura URL: ")

    # Create a new wallet with the provided information
    wallet = {
        "wallet_name": "eth",
        "private_key": private_key,
        "wallet_address": wallet_address,
        "nft_collection_name": collection_name,
        "infura_url": infura_url
    }
    
    print("Storing wallet info...")
    db.insert_wallet_data(wallet)
    print("Done.")    
    resp = input("Would you like to create another wallet? (y/n): ")
    if resp == 'y':
        wallet_setup()
    else:
        print("Done configuring wallets.")
        #log_transactions()
        get_wallets(self, current_collection=collection_name)
        return None, None
    
async def get_wallets(self, current_collection):
    # Get current wallets asynchronously
    wallets = await db.query_wallet_info(current_collection)

    print("Getting recent wallets")

    # Get the list of recent wallet addresses
    recent_wallets = await royalty_wallet_list(self, wallets, current_collection)
    return recent_wallets

async def royalty_wallet_list(self, wallets, current_collection):
    try:
        # Sort wallets by creation time in descending order
        sorted_wallets = sorted(wallets, key=lambda x: x.get('created_at', 0), reverse=False)
        
        # Extract the wallet addresses with 'wallet_name' equal to 'eth' and limit to maximum of 6
        collection_wallets = [wallet['wallet_address'] for wallet in sorted_wallets if wallet.get('wallet_name') == 'eth']
        
        # If the collection wallets list is empty, return None
        if len(collection_wallets) == 0:
            print("No wallets found. Please create a wallet.")
            return None
        # If the collection wallets list is not empty, return the first 6 wallets and remap the columns
        else:
            active_wallets = []
            royalty_wallet_list = collection_wallets[:6]
            for wallet in royalty_wallet_list:
                active_wallets.append(wallet) 
            return await store_royalty_wallets(self, current_collection, active_wallets)
    except Exception as e:
        print("Error getting wallets due to the following error:")
        print(e)
        return None

    
def store_royalty_wallets(self, current_collection, active_wallets):
    # Store the royalty wallets in the database
    print("Updating wallets receiving royalties...")
    for wallet in active_wallets:
        db.store_royalty_wallets(self, current_collection=current_collection, wallet=wallet)
        print("Royalty wallets stored successfully.")
        return None, None

def log_transactions():
    try:
        print("Starting log...")
    except Exception as e:
        print(e)
        print("Error logging transactions. Please try again.")
        return None, None
    
if __name__ == '__main__':
    process_command()

def store_user_credentials(username, password):
    # Store the user credentials in the database
    db.connect_to_postgresql()
    print("Successfully connected to PostgreSQL database.")
    db.store_user_credentials(username, password)
    print("Querying database...")
    db.close_connections()
    print("Successfully closed connections to PostgreSQL database.")

# Validate user inputs
def validate_inputs(ctx, value):
    if ctx.info_name == "pay":
        if value <= 0:
            raise click.BadParameter("Amount must be greater than zero")
    elif ctx.info_name == "status":
        if not isinstance(value, str):
            raise click.BadParameter("Invalid transaction ID entered. Please enter a valid transaction ID.")
    return value

# Function to authenticate the user
def authenticate_user(ctx=None):
    username = click.prompt("Username:")
    password = click.prompt("Password:", hide_input=True)

    # Authenticate the user
    if not security_module.secure_login(username, password):
        print("Invalid username or password.")
        return None, None

    if ctx:
        # Pass the authenticated username to the callback function
        ctx.ensure_object(dict)
        ctx.obj["username"] = username

    return username, password

# Define the "pay" command
@cli.command()
@click.argument("receiver_address")
@click.argument("amount", type=float, callback=validate_inputs)
@click.pass_context
def pay(ctx, receiver_address, amount):
    # Prompt for user credentials and authenticate the user
    username, password = authenticate_user(ctx)
    if not username or not password:
        print("Invalid username or password.")
        return None, None
    else:
        # Prompt for sender's address
        sender_address = click.prompt("Your wallet address:")
        
        # Proceed with the pay command logic
        # Encrypt the amount
        ciphertext, nonce, tag = security_module.encryption.encrypt_data(str(amount))
        
        # Invoke payment module
        payment_result = Payment.initiate_transaction(recipient_address=receiver_address, amount=amount, private_key=os.environ.get("PRIVATE_KEY"))
        
        if payment_result == "success":
            # Insert the encrypted amount into the database
            db.insert_transaction(sender_address, receiver_address, amount, ciphertext, nonce, tag)
            print("Payment successful!")
            return username, password
        else:
            print("Payment failed. Please try again later.")
            return None, None

@cli.command()
@click.argument("sender_wallet")
@click.pass_context
def status(ctx, sender_wallet):
    # Prompt for user credentials and authenticate the user
    username, password = authenticate_user(ctx)
    if not username or not password:
        print("Invalid username or password.")
        return None, None
    else:
        # Proceed with the status command logic
        # Query the database for transactions related to the sender's wallet
        transactions = db.get_transactions(sender_wallet)
        if transactions:
            active_payments = len(transactions)
            print("Number of Active Payments found: {}".format(active_payments))
            for transaction in transactions:
                # Decrypt the amount
                amount = security_module.encryption.decrypt_data(transaction["ciphertext"], transaction["nonce"], transaction["tag"])
                if amount:
                    print("Transaction ID: {}".format(transaction["id"]))
                    print("Sender: {}".format(transaction["sender_address"]))
                    print("Receiver: {}".format(transaction["receiver_address"]))
                    print("Amount: {}".format(amount))
                    print("Status: {}".format(transaction["status"]))
                    print("Created At: {}".format(transaction["created_at"]))
                else:
                    print("Error decrypting transaction data for transaction ID: {}".format(transaction["id"]))
        else:
            print("No transactions found for the provided sender's wallet.")


    # Proceed with the status command logic

if __name__ == "__main__":
    cli()
