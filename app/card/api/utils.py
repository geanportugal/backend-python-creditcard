import re

from creditcard.card import BRAND_REGEX, CreditCard
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from drf_yasg import openapi
from rest_framework.serializers import ValidationError


class ValidatedCreditCard(CreditCard):
    def __init__(self, *args, **kwargs):
        """Initialize the credit card."""
        return super().__init__(*args, **kwargs)

    # Check the card number against known brand regex patterns and return the brand name
    # override method from CreditCard from python-creditcard MAISTODOS
    def get_brand(self):
        """Get the brand of the credit card."""
        for brand, regex in BRAND_REGEX.items():
            if re.match(regex, self.number):
                return brand
        # return none because original method return Exception
        raise ValidationError({'brand': 'Brand not Found"'})


class CreditCardEncryptor:
    """ A class that encrypts and decrypts credit card numbers.
        AES symmetry algorithm was used for encryption. For more details, see
        https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
    """

    def __init__(self, encryption_key, salt):
        """Initialize the encryptor."""
        self.encryption_key = encryption_key.encode()
        self.key = self.derive_key(salt.encode())

    def derive_key(self, salt):
        """Derive the encryption key from the salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,  # A unique salt is used for each encryption process
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.encryption_key)

    # Encrypt the credit card number using AES encryption
    def encrypt_credit_card(self, card_number):
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(card_number.encode()) + padder.finalize()
        encrypted_card = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_card

    # Decrypt the encrypted credit card number using AES decryption
    def decrypt_credit_card(self, encrypted_card):
        encrypted_card = bytes.fromhex(encrypted_card)
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(
            encrypted_card) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_card = unpadder.update(
            decrypted_padded_data) + unpadder.finalize()
        return decrypted_card.decode()


# --- Request Schema Definition ---
"""
    function to be used in the swagger_auto_schema decorator, used in the api viewset 
    to return a post example in the swagger documentation
"""
request_schema_dict = openapi.Schema(
    title=("Create Credit Card"),
    type=openapi.TYPE_OBJECT,
    properties={
        'holder': openapi.Schema(type=openapi.TYPE_STRING, description=('holder'), example='Fulano'),
        'number': openapi.Schema(type=openapi.TYPE_STRING, description=('number'), example="0000000000000001"),
        'exp_date': openapi.Schema(type=openapi.TYPE_STRING, description=('exp_date'), example="02/2026"),
        'cvv': openapi.Schema(type=openapi.TYPE_STRING, description=('cvv'), example="123"),
    }
)
