# key_management.py

import time
from encryption import derive_key
from Crypto.Random import get_random_bytes

# Constants
KEY_UPDATE_INTERVAL = 3600  # 1 hour update interval
SALT_SIZE = 16


class KeyManager:
    def __init__(self, initial_password):
        self.password = initial_password
        self.key = derive_key(self.password)

    def update_key(self, new_password=None):
        """Update the encryption key."""
        if new_password:
            self.password = new_password
        self.key = derive_key(self.password)
        self.last_update_time = time.time()
        print("Key updated.")

    def check_key_update(self):
        """Check if it's time to update the key."""
        current_time = time.time()
        if current_time - self.last_update_time > KEY_UPDATE_INTERVAL:
            self.update_key()


# Example Implementation
if __name__ == "__main__":
    initial_password = "SecurePassword"
    key_manager = KeyManager(initial_password)

    time.sleep(2)  
    key_manager.check_key_update()  

    time.sleep(KEY_UPDATE_INTERVAL)
    key_manager.check_key_update()
