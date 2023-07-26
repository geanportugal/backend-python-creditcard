import pytest
from datetime import date, datetime
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from card.api.serializers import CreditCardSerializer
from card.api.utils import CreditCardEncryptor, ValidatedCreditCard
from card.models import CreditCard


class FakeRequest(object):
    status_code = 200
    method = 'POST'

@pytest.fixture
def valid_credit_card_data():
    return {
        'number': '4111111111111111',
        'exp_date': '02/2026',
        'holder': 'John Doe',
        'cvv': '123',
    }

@pytest.fixture
def invalid_credit_card_data():
    return {
        'holder': 'John Doe',
        'cvv': '123',
        'number': 'invalid_number',
        'exp_date': '06/2024',
    }

@pytest.fixture
def fake_request():
    return FakeRequest()

@pytest.fixture
def generate_secret_key_card():
    return 'NOvE58y2SFJ8J0U_QDuZyZ-L9uyidRkp4koTlybCXuc'

@pytest.fixture    
def generate_salt():
    return 'NT_tPimVURw3pTVtIvsefQ'

@pytest.mark.django_db
def test_credit_card_serializer_valid(valid_credit_card_data, fake_request):
    serializer = CreditCardSerializer(data=valid_credit_card_data, context={'request': fake_request})
    assert serializer.is_valid()

@pytest.mark.django_db
def test_credit_card_serializer_invalid(invalid_credit_card_data, fake_request):
    serializer = CreditCardSerializer(data=invalid_credit_card_data, context={'request': fake_request})
    assert not serializer.is_valid()

@pytest.mark.django_db
def test_credit_card_serializer_encryption(valid_credit_card_data, fake_request):
    serializer = CreditCardSerializer(data=valid_credit_card_data, context={'request': fake_request})
    serializer.is_valid()
    encrypted_number = serializer.validated_data['number']
    assert encrypted_number != valid_credit_card_data['number']  # Check if the number is encrypted

@pytest.mark.django_db
def test_credit_card_serializer_exp_date_conversion(valid_credit_card_data, fake_request):
    serializer = CreditCardSerializer(data=valid_credit_card_data, context={'request': fake_request})
    serializer.is_valid()
    exp_date = serializer.validated_data['exp_date']
    assert isinstance(exp_date, date)

@pytest.mark.django_db
def test_credit_card_serializer_invalid_exp_date_format(invalid_credit_card_data, fake_request):
    serializer = CreditCardSerializer(data=invalid_credit_card_data, context={'request': fake_request})
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_credit_card_serializer_to_representation(valid_credit_card_data, fake_request):
    valid_credit_card_data['exp_date'] = date(2026, 2, 28)
    credit_card = CreditCard(**valid_credit_card_data)
    serializer = CreditCardSerializer(instance=credit_card, context={'request': fake_request})
    representation = serializer.data
    assert representation['exp_date'] == '02/2026'  # Check if the exp_date is correctly formatted

@pytest.mark.django_db
def test_credit_card_serializer_to_internal_value(valid_credit_card_data, fake_request):
    fake_request_put = fake_request
    fake_request_put.method = 'PUT'
    serializer = CreditCardSerializer(data=valid_credit_card_data, context={'request': fake_request_put})
    serializer.is_valid()
    internal_value = serializer.validated_data
    assert 'exp_date' in internal_value
    assert 'number' in internal_value

def test_validated_credit_card_get_brand(valid_credit_card_data):
    credit_card = ValidatedCreditCard(valid_credit_card_data['number'])
    assert credit_card.get_brand() == 'visa'

def test_encrypt_credit_card(generate_secret_key_card, generate_salt):
    credit_card_number = '5334477627922012'

    encryptor = CreditCardEncryptor(generate_secret_key_card, generate_salt)
    encrypted_card = encryptor.encrypt_credit_card(credit_card_number).hex()

    assert encrypted_card == '2f4764f9cca5bf24e97b4b7a2a0700191435bb8c175e386ce47b0174d84e5323'


def test_decrypt_credit_card(generate_secret_key_card, generate_salt):
    credit_card_number = '5334477627922012'
    encrypted_card = str('2f4764f9cca5bf24e97b4b7a2a0700191435bb8c175e386ce47b0174d84e5323')

    encryptor = CreditCardEncryptor(generate_secret_key_card, generate_salt)
    decrypted_card = encryptor.decrypt_credit_card(encrypted_card)

    assert decrypted_card == credit_card_number
