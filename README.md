

   $$$$$$\$$$$$$$$\ $$\      $$\  $$$$$$\   $$$$$$\  $$\      $$\ $$$$$$$$\ $$$$$$$\  $$$$$$\  $$$$$$\  $$\   $$\ 
  $$  __$$\__$$  __|$$$\    $$$ |$$  __$$\ $$  __$$\ $$$\    $$$ |$$  _____|$$  __$$\ \_$$  _|$$  __$$\ $$$\  $$ |
  $$ /  $$ | $$ |   $$$$\  $$$$ |$$ /  \__|$$ /  $$ |$$$$\  $$$$ |$$ |      $$ |  $$ |  $$ |  $$ /  $$ |$$$$\ $$ |
  $$$$$$$$ | $$ |   $$\$$\$$ $$ |$$ |      $$ |  $$ |$$\$$\$$ $$ |$$$$$\    $$ |  $$ |  $$ |  $$$$$$$$ |$$ $$\$$ |
  $$  __$$ | $$ |   $$ \$$$  $$ |$$ |      $$ |  $$ |$$ \$$$  $$ |$$  __|   $$ |  $$ |  $$ |  $$  __$$ |$$ \$$$$ |
  $$ |  $$ | $$ |   $$ |\$  /$$ |$$ |  $$\ $$ |  $$ |$$ |\$  /$$ |$$ |      $$ |  $$ |  $$ |  $$ |  $$ |$$ |\$$$ |
  $$ |  $$ | $$ |   $$ | \_/ $$ |\$$$$$$  | $$$$$$  |$$ | \_/ $$ |$$$$$$$$\ $$$$$$$  |$$$$$$\ $$ |  $$ |$$ | \$$ |
  \__|  \__| \__|   \__|     \__| \______/  \______/ \__|     \__|\________|\_______/ \______|\__|  \__|\__|  \__|
                                                                                                                  
                                                                                                                  
                                                                                                                 
### Installation and Setup

#### Prerequisites

* Python 3.9 or any version below Python 3.11
* Pip
* Git
* PostgreSQL


#### Optional (Recommended)

* Python setup.py command for automated setup

### Step-by-Step Guide

#### 1. Clone or Download the Repository
```
git clone https://github.com/J-cyber0/atmcomedian.git
```

#### 2. Create a Virtual Environment (if not using setup.py)

A virtual environment helps isolate the application's dependencies from the system's global Python environment.

**Windows/macOS/Linux:**
```
python3 -m venv venv
```

#### 3. Install Required Dependencies (if not using setup.py)

Activate the virtual environment to install the dependencies:

**Windows:**
```
venv\Scripts\activate
```

**macOS/Linux:**
```
source venv/bin/activate
```

#### Installation

Before proceeding, make sure to have PostgreSQL installed on your system. If not, follow these steps:

**Download PostgreSQL:**

- **Windows:**
  - Download the PostgreSQL installer for Windows [https://www.postgresql.org/download/windows/]
  - This installer can run in graphical or silent install modes.

- **macOS:**
  - Download the PostgreSQL installer for macOS [https://www.postgresql.org/download/macosx/]
  - This installer can run in graphical or silent install modes.
 
- **Linux:**
  - To install PostgreSQL on Ubuntu, use the apt-get (or other apt-driving) command:
```
sudo apt-get -y install postgresql
```

  - To upgrade PostgreSQL on Ubuntu, use the apt command:
```
sudo apt update
sudo apt upgrade postgresql
```

   - After the upgrade, restart PostgreSQL:
```
sudo systemctl restart postgresql
```

- **WSL2 Ubuntu:**
  - To install PostgreSQL on WSL2 Ubuntu, use the following commands:
```
sudo apt-get update
```

   - To install PostgreSQL on WSL2 Ubuntu, use the following commands:
```
sudo apt install postgresql postgresql-contrib
```

sudo apt-get update

sudo apt-get -y install postgresql postgresql-contrib
```

  - After the upgrade, start PostgreSQL:
```
psql --version
 
sudo service postgresql status
 
sudo service postgresql start
```

  - For other distributions, refer to your package manager or visit [https://www.postgresql.org/download/]

Once installed, proceed with the setup.


Change current directory to `atmcomedian`:
```
cd atmcomedian
```

Then, install the dependencies:

```
pip install -r requirements.txt
```

## Create Database - Do this no matter which method you installed with

**PostgreSQL:**

1. Ensure PostgreSQL server is running.
2. Connect to PostgreSQL and create a database named `cryptos` with the following details:
   * Host: localhost
   * Port: 5432
   * User: postgres
   * Password: password
3. Run the following command to create the database:
```
createdb -h localhost -U atmcomedian -p 5432 cryptos
```

### After Run the Application - Do this no matter which method you installed with
```
python main.py
```

### Additional Notes

* Optional: Install the python framework sgpt by tbckr on GitHub to get an AI in your command line. Refer to the following GitHub repository for more info:

https://github.com/tbckr/sgpt