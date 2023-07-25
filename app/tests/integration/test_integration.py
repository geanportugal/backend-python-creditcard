import pytest
from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from card.models import CreditCard
from card.api.serializers import CreditCardSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def credit_card_data():
    return {
        'number': '4111111111111111',
        'exp_date': '02/2026',
        'holder': 'John Doe',
        'cvv': '123',
    }


@pytest.fixture
def create_credit_card(credit_card_data):
    return CreditCard.objects.create(**credit_card_data)


@pytest.mark.django_db
def test_create_credit_card(api_client, credit_card_data):
    url = reverse('creditcard-list')
    response = api_client.post(url, credit_card_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CreditCard.objects.count() == 1


@pytest.mark.django_db
def test_create_credit_card_invalid_data(api_client):
    url = reverse('creditcard-list')
    credit_card_data = {
        'number': '1234567890123456',  # Invalid credit card number
        'exp_date': '02/2026',
        'holder': 'John Doe',
        'cvv': '123',
    }
    response = api_client.post(url, credit_card_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert CreditCard.objects.count() == 0


@pytest.mark.django_db
def test_credit_card_encryption(create_credit_card):
    credit_card = create_credit_card
    encrypted_card_number = credit_card.number
    assert encrypted_card_number != credit_card.number


@pytest.mark.django_db
def test_credit_card_decryption(create_credit_card):
    credit_card = create_credit_card
    encrypted_card_number = credit_card.number
    decrypted_card_number = credit_card.decrypt_credit_card(encrypted_card_number)
    assert decrypted_card_number == credit_card.number


@pytest.mark.django_db
def test_get_credit_card(api_client, create_credit_card):
    url = reverse('creditcard-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['holder'] == create_credit_card.holder


@pytest.mark.django_db
def test_get_credit_card_detail(api_client, create_credit_card):
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['holder'] == create_credit_card.holder


@pytest.mark.django_db
def test_update_credit_card(api_client, create_credit_card):
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    updated_data = {
        'number': '4111111111111122',
        'exp_date': '02/2026',
        'holder': 'Jane Doe',
        'cvv': '123',
    }
    response = api_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    create_credit_card.refresh_from_db()
    assert create_credit_card.holder == 'Jane Doe'
    assert create_credit_card.number == '4111111111111122'


@pytest.mark.django_db
def test_delete_credit_card(api_client, create_credit_card):
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CreditCard.objects.count() == 0
