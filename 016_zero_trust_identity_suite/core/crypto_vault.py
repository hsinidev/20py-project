import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class CryptoVault:
    """
    Handles AES-256-GCM encryption/decryption for local credential storage.
    """
    def __init__(self, master_password):
        self.salt = b'\x12\xab\xf4\x89\x33\x11\xde\xad\xbe\xef' # In production, this should be unique per user
        self.key = self._derive_key(master_password)
        self.aesgcm = AESGCM(self.key)

    def _derive_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def encrypt(self, data):
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, data.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_data):
        raw_data = base64.b64decode(encrypted_data)
        nonce = raw_data[:12]
        ciphertext = raw_data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

if __name__ == "__main__":
    vault = CryptoVault("hsini_secure_pw")
    secret = "TopSecretFaceVector_2026"
    enc = vault.encrypt(secret)
    print(f"Encrypted: {enc}")
    dec = vault.decrypt(enc)
    print(f"Decrypted: {dec}")
