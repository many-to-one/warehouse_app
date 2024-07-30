import os

# Generate a random 32-byte key and convert it to a hexadecimal string
secret_key = os.urandom(32).hex()
print(f"SECRET_KEY = '{secret_key}'")
