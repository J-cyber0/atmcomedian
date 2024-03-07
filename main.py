import asyncio
import modules.database as db
import modules.cli as cli
from modules.deposit import Deposit

class Main:
    def __init__(self):
        self.user_logged_in = False

    async def main(self):
        await self.check_user_login()

    async def check_user_login(self):
        if not self.user_logged_in:
            if not await cli.is_user_logged_in():
                await cli.user_login()
            self.user_logged_in = True
        royalty_wallets = await self.get_royalty_wallets()
        await self.start_monitor(royalty_wallets)

    async def get_royalty_wallets(self):
        return await cli.get_wallets(self, current_collection='eth')

    async def start_monitor(self, royalty_wallets):
        cli.log_transactions()
        deposit_instance = Deposit()

        # Get latest wallet
        latest_wallet = royalty_wallets[0]  # Get the first wallet in the list

        # Call listen_deposit_events for the latest wallet only
        await deposit_instance.listen_deposits(wallet_address=latest_wallet)

if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
