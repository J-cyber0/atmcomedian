import os
import click
from security import SecurityModule
from database import Database
from payment import Payment

# Initialize the user database
user_db = {}

# Create an instance of the security module, passing the user database
security_module = SecurityModule()

# Initialize the database object
db = Database()

# Define the main CLI command group
@click.group()
def cli():
    pass

# Define the "wallet setup" command
@cli.command()
def wallet_setup():
    # Prompt for user credentials
    username = click.prompt("Username:")
    password = click.prompt("Password:", hide_input=True)
    confirm_password = click.prompt("Confirm Password:", hide_input=True)

    # Validate the password confirmation
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    # Create the user account
    if security_module.create_user(username, password):
        print("User account created successfully.")
    else:
        print("Failed to create user account. Please try again.")

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
