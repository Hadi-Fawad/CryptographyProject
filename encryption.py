# encryption.py

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

# Constants
KEY_LENGTH = 32  # Key length in bytes
ITERATIONS = 100000  # Iterations of key derivation for security


def derive_key(password: str) -> bytes:
    """Derive a cryptographic key from a password."""
    # Use a static salt amount
    static_salt = b'static_salt'
    return PBKDF2(password, static_salt, dkLen=KEY_LENGTH, count=ITERATIONS)


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypt a message using the given key."""
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext)


def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decrypt a message using the given key."""
    try:
        encrypted_message = base64.b64decode(encrypted_message)
        nonce, tag, ciphertext = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
    except (ValueError, KeyError):
        return "Incorrect decryption."


def bytes_to_base64_str(bytes_data):
    return base64.b64encode(bytes_data).decode('utf-8')


# Example implementation below
if __name__ == "__main__":
    password = "SecurePassword"
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password, salt)

    original_message = "Hello, World!"
    encrypted = encrypt_message(original_message, key)
    decrypted = decrypt_message(encrypted, key)

    print(f"Original: {original_message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
