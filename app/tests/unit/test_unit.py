# import pytest
# from datetime import date
# from rest_framework.exceptions import ValidationError
# from card.api.serializers import CreditCardSerializer
# from card.api.utils import CreditCardEncryptor, ValidatedCreditCard
# from card.models import CreditCard

# @pytest.fixture
# def valid_credit_card_data():
#     return {
#         'number': '4111111111111111',
#         'exp_date': '02/2026',
#         'holder': 'John Doe',
#         'cvv': '123',
#     }

# def test_credit_card_serializer(valid_credit_card_data):
#     serializer = CreditCardSerializer(data=valid_credit_card_data)
#     assert serializer.is_valid()

# def test_credit_card_serializer_invalid_number():
#     invalid_credit_card_data = {
#         'number': '1234567890123456',
#         'exp_date': '02/2026',
#         'holder': 'John Doe',
#         'cvv': '123',
#     }
#     serializer = CreditCardSerializer(data=invalid_credit_card_data)
#     with pytest.raises(ValidationError) as exc_info:
#         serializer.is_valid(raise_exception=True)
#     assert 'Invalid credit card' in str(exc_info.value)

# def test_credit_card_serializer_invalid_date_format():
#     invalid_credit_card_data = {
#         'number': '4111111111111111',
#         'exp_date': '2026-02',
#         'holder': 'John Doe',
#         'cvv': '123',
#     }
#     serializer = CreditCardSerializer(data=invalid_credit_card_data)
#     with pytest.raises(ValidationError) as exc_info:
#         serializer.is_valid(raise_exception=True)
#     assert 'Invalid date format. Use \'MM/YYYY\' format.' in str(exc_info.value)

# def test_credit_card_serializer_invalid_brand():
#     invalid_credit_card_data = {
#         'number': '4111111111111111',
#         'exp_date': '02/2026',
#         'holder': 'John Doe',
#         'cvv': '123',
#         'brand': 'InvalidBrand',
#     }
#     serializer = CreditCardSerializer(data=invalid_credit_card_data)
#     with pytest.raises(ValidationError) as exc_info:
#         serializer.is_valid(raise_exception=True)
#     assert 'Invalid brand' in str(exc_info.value)

# def test_credit_card_encryptor(valid_credit_card_data):
#     encryptor = CreditCardEncryptor('my_secret_key', 'my_salt')
#     encrypted_card = encryptor.encrypt_credit_card(valid_credit_card_data['number'])
#     assert isinstance(encrypted_card, bytes)

# def test_credit_card_decryptor(valid_credit_card_data):
#     encryptor = CreditCardEncryptor('my_secret_key', 'my_salt')
#     encrypted_card = encryptor.encrypt_credit_card(valid_credit_card_data['number'])
#     decrypted_card = encryptor.decrypt_credit_card(encrypted_card)
#     assert decrypted_card == valid_credit_card_data['number']

# def test_validated_credit_card_get_brand(valid_credit_card_data):
#     credit_card = ValidatedCreditCard(valid_credit_card_data['number'])
#     assert credit_card.get_brand() == 'visa'

# def test_encrypt_credit_card(settings):
#     settings.SECRET_KEY_CARD = 'secret_key'
#     settings.SALT = 'salt'

#     credit_card_number = '0000000000000001'

#     encryptor = CreditCardEncryptor(settings.SECRET_KEY_CARD, settings.SALT)
#     encrypted_card = encryptor.encrypt_credit_card(credit_card_number)

#     assert encrypted_card.startswith('0000000000000001')
#     assert len(encrypted_card) == 32


# def test_decrypt_credit_card(settings):
#     settings.SECRET_KEY_CARD = 'secret_key'
#     settings.SALT = 'salt'

#     credit_card_number = '0000000000000001'
#     encrypted_card = '00000000000000011234567890abcdef'

#     encryptor = CreditCardEncryptor(settings.SECRET_KEY_CARD, settings.SALT)
#     decrypted_card = encryptor.decrypt_credit_card(encrypted_card)

#     assert decrypted_card == credit_card_number
