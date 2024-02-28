import subprocess
#import agents.eth_agent as eth_agent

#Agent = eth_agent.ethBot()

#def do_start(private_key, wallet_address, percent_of_total_amount, infura_url):
#    #Agent.start_agent(private_key, wallet_address, percent_of_total_amount, infura_url)
#    return


def send_(private_key, recipient_address, infura_url):
    # Get user input for the transaction.
    recipient_address = input("Enter the recipient's address: ")
    amount = input("Enter the amount to transfer: ")

    # Call the ethBot.py script with the necessary arguments.
    cmd = ["python", "ethBot.py", private_key, recipient_address, amount]
    if infura_url:
        cmd.append(infura_url)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Handle the response from the ethBot.py script.
    if process.returncode == 0:
        print(f"Transaction successful: {output.decode()}")
    else:
        print(f"Transaction failed: {error.decode()}")