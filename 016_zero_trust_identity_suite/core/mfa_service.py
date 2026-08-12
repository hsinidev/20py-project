import pyotp
import qrcode
from io import BytesIO

class MFAService:
    """
    Handles RFC 6238 TOTP logic for Multi-Factor Authentication.
    """
    def __init__(self, secret=None):
        self.secret = secret if secret else pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)

    def generate_qr_data(self, user_email):
        """Generates the provisioning URI for Google Authenticator / Authy"""
        return self.totp.provisioning_uri(name=user_email, issuer_name="ZeroTrustVault")

    def verify_token(self, token):
        """Verifies a 6-digit TOTP token"""
        return self.totp.verify(token)

if __name__ == "__main__":
    mfa = MFAService()
    print(f"Secret: {mfa.secret}")
    print(f"Current Token: {mfa.totp.now()}")
