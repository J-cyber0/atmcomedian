import os
import asyncio
from web3 import Web3
import json
from modules.database import Database
from modules.payment import Payment

class Deposit:
    def __init__(self):
        self.web3 = Web3(Web3.WebsocketProvider("ws://localhost:8546", websocket_timeout=60))
        self.contract_abi = self.load_contract_abi()
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.db = Database()

    def load_contract_abi(self):
        with open(os.path.join(os.getcwd(), 'contracts', 'Coin.abi'), 'r') as contract_file:
            return json.load(contract_file)

    async def listen_deposits(self, receiver_wallet_address):
        while True:
            try:
                print("Getting access to wallets...")
                new_block_filter = self.web3.eth.filter('latest')
                async for block in new_block_filter.get_new_entries():
                    print('\nNew deposit detected:')
                    deposit_event = await self.trigger_payments(block)
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

    async def trigger_payments(self, block):
        # Update royalty wallets in database
        print("triggering payments...")
        royalty_wallets = await self.get_royalty_wallets()
        if royalty_wallets:
            print("Successfully retrieved royalty wallets.")
            payment_instance = Payment()
            if len(royalty_wallets) >= 3:
                for wallet_info in royalty_wallets:
                    wallet_address = wallet_info['wallet_address']
                    wallet_id = wallet_info['id']
                    print("Processing payments to wallet id:", wallet_id)
                    await payment_instance.initiate_transaction(recipient_address=wallet_address, amount=input("Enter amount for deposit: "), private_key=os.getenv('PRIVATE_KEY'))
                    print("Successfully processed and stored payments to wallet id:", wallet_id)
            else:
                print("Not enough royalty wallets to distribute payments.")
        else:
            print("Error processing payments.")

    async def get_royalty_wallets(self):
        try:
            royalty_wallets = self.db.query_royalty_wallets()
            return royalty_wallets
        except Exception as e:
            print("Error finding royalty wallets:", e)
            return None

    async def update_royalty_wallets(self, new_wallet):
        try:
            self.db.store_royalty_wallets(wallet=new_wallet)
            print("Successfully updated royalty wallets.")
        except Exception as e:
            print("Error updating royalty wallets:", e)


async def main(royalty_wallets):
    deposit_listener = Deposit()
    tasks = [asyncio.create_task(deposit_listener.listen_deposits(wallet['wallet_address'])) for wallet in royalty_wallets]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # royalty_wallets should be passed from the main.py script
    royalty_wallets = [...]  # Define royalty wallets here or fetch from main.py
    asyncio.run(main(royalty_wallets))
