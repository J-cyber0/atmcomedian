import os
import asyncio
from web3 import Web3
import json
import threading
from modules.database import Database
from modules.payment import Payment

class Deposit:
    def __init__(self):
        self.web3 = Web3(Web3.WebsocketProvider("ws://localhost:8546", websocket_timeout=60))
        self.db = Database()
        self.pause_event = threading.Event()

    async def listen_deposits(self, receiver_wallet_address):
        while True:
            try:
                print("Getting access to wallets...")
                new_block_filter = self.web3.eth.filter('latest')
                async for block in new_block_filter.get_new_entries():
                    if self.pause_event.is_set():
                        print("Pausing to distribute payments...")
                        self.pause_event.clear()
                        await self.pause_event.wait()  # Wait until the event is set again
                    print('\nNew deposit detected:')
                    deposit_event = await self.trigger_payments(block, receiver_wallet_address)
                    if deposit_event['args']['receiver'] == receiver_wallet_address:
                        return deposit_event['args']['receiver']
                    
                    print("Updating royalty wallets...")
                    new_wallet = deposit_event['args']['sender']
                    await self.update_royalty_wallets(new_wallet)
                else:
                    print('Listening for new deposit events...', end=', ', flush=True)
                    await asyncio.sleep(2)  # Adjust sleep duration as needed
            except Exception as e:
                print(f'Error occurred: {str(e)}')

    async def trigger_payments(self):
        try:
            print("Triggering payments...")
            royalty_wallets = await self.get_royalty_wallets()
            if not royalty_wallets:
                print("Error processing payments: No royalty wallets found.")
                return

            print("Successfully retrieved royalty wallets.")
            payment_instance = Payment()
            for wallet_info in royalty_wallets:
                wallet_address = wallet_info['wallet_address']
                wallet_id = wallet_info['id']
                print("Processing payments to wallet id:", wallet_id)
                amount = await self.get_valid_amount()
                await payment_instance.initiate_transaction(recipient_address=wallet_address, amount=amount, private_key=os.getenv('PRIVATE_KEY'))
                print("Successfully processed and stored payments to wallet id:", wallet_id)
        except Exception as e:
            print(f"Error processing payments: {str(e)}")

    async def get_royalty_wallets(self):
        try:
            return await self.db.query_royalty_wallets()
        except Exception as e:
            print(f"Error finding royalty wallets: {str(e)}")
            return None

    async def update_royalty_wallets(self, new_wallet):
        try:
            await self.db.store_royalty_wallets(wallet=new_wallet)
            print("Successfully updated royalty wallets.")
        except Exception as e:
            print(f"Error updating royalty wallets: {str(e)}")

    async def get_valid_amount(self):
        while True:
            amount = input("Enter amount for deposit: ")
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Amount must be a positive number.")
                else:
                    return amount
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

async def main(royalty_wallets):
    deposit_listener = Deposit()
    tasks = [asyncio.create_task(deposit_listener.listen_deposits(wallet['wallet_address'])) for wallet in royalty_wallets]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # royalty_wallets should be passed from the main.py script
    royalty_wallets = [...]  # Define royalty wallets here or fetch from main.py
    asyncio.run(main(royalty_wallets))
