Run the Setup Script

Execute the setup.py script to create a virtual environment and install dependencies:


 python setup.py


                                                                   Important Notes

 • Virtual Environment Activation: The setup script will create a virtual environment, but due to shell limitations, it may not activate it. After
   running the setup script, activate the virtual environment with:

    source venv/bin/activate  # On Unix-like systems
    .\venv\Scripts\activate   # On Windows

 • Windows Compatibility: The setup script uses Unix-like paths for some operations. Adjustments might be necessary for Windows environments,
   particularly for activating the virtual environment within the script.
 • Execution Permission: If you're on a Unix-like system, ensure the setup.py script is executable by running:

    chmod +x setup.py

 • sgpt Verification: The script attempts to verify the sgpt installation. Ensure sgpt is correctly installed and accessible at
   /home/juan/.local/bin/sgpt or adjust the path in the script accordingly.


                                                                        Usage

After setting up, you can start using the application by running:


 python main.py


Modify the settings.json file in the settings/ directory to configure wallet and other application settings as needed.


                                                                    Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.


                                                                       License

This project is licensed under the MIT License. See the LICENSE file for details.


                                                                  Acknowledgements

 • Web3.py: Python library for interacting with the Ethereum blockchain.
 • Requests: Python library for making HTTP requests.



 This revised `README.md` provides a comprehensive guide for users to set up and start using the **atmcomedian** application, including important
 notes on virtual environment activation, Windows compatibility, execution permission, and `sgpt` verification.