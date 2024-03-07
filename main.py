import asyncio
import modules.database as db
import modules.cli as cli
from modules.deposit import Deposit
import tracemalloc
import signal
import logging

class Main:
    def __init__(self):
        self.user_logged_in = False

    async def main(self):
        try:
            await self.check_user_login()
        except Exception as e:
            logging.error(f"Error in main: {e}")

    async def check_user_login(self):
        try:
            tracemalloc.start()
            if not self.user_logged_in:
                # Pass an empty phrase for now, you may adjust this according to your logic
                await cli.main()
                royalty_wallets = await self.get_royalty_wallets()
                if royalty_wallets:
                    await self.start_monitor(royalty_wallets)
                else:
                    self.user_logged_in = True
                    await cli.user_login()
        except Exception as e:
            logging.error(f"Error in check_user_login: {e}")
        finally:
            tracemalloc.stop()

    async def get_royalty_wallets(self):
        cli_instance = cli
        try:
            # Start tracing memory allocations
            tracemalloc.start()
    
            # Assuming cli is an instance of the class containing get_wallets method
            return await cli_instance.royalty_wallet_list(self, current_collection=None)

            # Code to handle if no nft collections made ye
        except Exception as e:
            logging.error(f"Error in get_royalty_wallets: {e}")
            return None
        finally:
            tracemalloc.stop()

    async def start_monitor(self, royalty_wallets):
        try:
            cli.log_transactions()
            deposit_instance = Deposit()

            if royalty_wallets:
                # Get latest wallet
                latest_wallet = royalty_wallets[0]  # Get the first wallet in the list

                # Call listen_deposit_events for the latest wallet only
                await deposit_instance.listen_deposits(wallet_address=latest_wallet)
            else:
                logging.warning("No royalty wallets found.")
        except Exception as e:
            logging.error(f"Error in start_monitor: {e}")

async def handle_sigint(sig, frame):
    logging.info("Received SIGINT, stopping gracefully...")
    raise KeyboardInterrupt

async def run_main():
    logging.basicConfig(level=logging.INFO)
    main_instance = Main()
    signal.signal(signal.SIGINT, lambda sig, frame: asyncio.create_task(handle_sigint(sig, frame)))
    try:
        await main_instance.main()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: Stopping gracefully...")

if __name__ == "__main__":
    asyncio.run(run_main())
