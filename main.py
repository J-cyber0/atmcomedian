from agents.wallet_monitor_agent import read_settings, start_, do_start
from agents.payment_agent import transfer

def main():
    wallets = read_settings()
    for wallet in wallets:
        private_key = wallet.get('private_key')
        withdraw_to = wallet.get('withdraw_to')
        percent_of_total_amount = wallet.get('percent_of_total_amount')
        infura_url = wallet.get('infura_url')
        do_start(private_key, withdraw_to, percent_of_total_amount, infura_url)

if __name__ == "__main__":
    main()
