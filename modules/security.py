import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Authentication:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        # Only allow the first user to be created
        if len(self.users) > 0:
            return False

        # Store username and hashed password
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
        return True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        # Check if username exists and compare hashed passwords
        if username in self.users:
            hashed_password = self._hash_password(password)
            if self.users[username] == hashed_password:
                return True
        return False

    def create_user(self, username, password):
        return self.register_user(username, password)

class Encryption:
    def __init__(self, key):
        self.key = key

    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return ciphertext, cipher.nonce, tag

    def decrypt_data(self, ciphertext, nonce, tag):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode()
        except ValueError:
            # Handle decryption failure
            return None

class SecurityModule:
    def __init__(self, user_db):
        self.authentication = Authentication()
        self.user_db = user_db
        self.encryption = Encryption(get_random_bytes(16))

    def secure_login(self, username, password):
        if self.authentication.authenticate_user(username, password):
            return True
        else:
            return False

    def encrypt_sensitive_data(self, data):
        return self.encryption.encrypt_data(data)

    def decrypt_sensitive_data(self, ciphertext, nonce, tag):
        return self.encryption.decrypt_data(ciphertext, nonce, tag)

    def create_user(self, username, password):
        return self.authentication.create_user(username, password)

if __name__ == "__main__":
    # Example usage
    user_db = {}  # Initialize user database
    security_module = SecurityModule(user_db)

    # Create a new user
    username = input("Enter username: ")
    password = input("Enter password: ")
    if security_module.create_user(username, password):
        print("User created successfully!")
    else:
        print("Username already exists or user creation is disabled.")