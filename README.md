Installation and Setup

### Prerequisites

* Python 3.9 or higher
* Pip
* Git

### Installation

### Optional (Recommended)

* Python setup.py command for automated setup



### Step-by-Step Guide

#### 1. Clone or Download the Repository

```
git clone https://github.com/J-cyber0/atmcomedian.git
```


#### 2. Create a Virtual Environment (if not using setup.py)

A virtual environment helps isolate the application's dependencies from the system's global Python environment.

**Windows:**

```
python -m venv venv
```

**macOS/Linux:**

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

Then, install the dependencies:

```
pip install -r requirements.txt
```

## Create Database - Do this no matter which method you installed with

**PostgreSQL:**

1. Create a database named `crtypos` with the following details:
   * Host: localhost
   * Port: 8081
   * User: atmcomedian
   * Password: password
2. Run the following command to create the database:

```
createdb -h localhost -U atmcomedian -p 8081 -e cryptos
```

### After Run the Application - Do this no matter which method you installed with

```
python main.py
```

### Additional Notes

* Optional: Install the python framework sgpt by tbckr on github to get an AI in your command line. Refer to the following github repository for more info:

 ```
 https://github.com/tbckr/sgpt
 ```