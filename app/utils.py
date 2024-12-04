import os
import qrcode
from cryptography.fernet import Fernet

# Generate encryption key (ensure secure storage)
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Directory for wallets
WALLETS_DIR = "static/wallets"
os.makedirs(WALLETS_DIR, exist_ok=True)


def save_qr_code(address):
    """
    Generate and save a QR code for the wallet address.
    Args:
        address (str): Wallet address to generate a QR code for.
    Returns:
        str: File path to the saved QR code.
    """
    try:
        qr = qrcode.make(address)
        qr_path = os.path.join(WALLETS_DIR, f"{address}.png")
        qr.save(qr_path)
        print(f"QR code successfully saved at {qr_path}")  # Debugging log
        return f"/static/wallets/{address}.png"
    except Exception as e:
        print(f"Error generating QR code: {e}")  # Log the error
        return None

def encrypt_and_save_key(private_key, filename):
    """
    Encrypt and save a private key to a file.
    Args:
        private_key (str): The private key to encrypt and save.
        filename (str): The file path to save the encrypted private key.
    """
    encrypted_key = cipher.encrypt(private_key.encode())
    with open(filename, "wb") as f:
        f.write(encrypted_key)

def save_wallet(address, private_key):
    """
    Save a wallet's private key securely.
    Args:
        address (str): Wallet address.
        private_key (str): Wallet's private key.
    Returns:
        str: File path to the saved encrypted private key.
    """
    print(f"Saving private key for address: {address}")  # Debug log
    encrypted_key_path = os.path.join(WALLETS_DIR, f"{address}_private.enc")
    encrypt_and_save_key(private_key, encrypted_key_path)
    return encrypted_key_path

