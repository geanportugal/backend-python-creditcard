from datetime import date

import pytest
from card.api.serializers import CreditCardSerializer
from card.models import CreditCard
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_superuser(username='testuser', password='testpassword', email='testuser@test.com')


@pytest.fixture
def get_tokens_for_user(test_user):
    refresh = RefreshToken.for_user(test_user)
    return f'Bearer {str(refresh.access_token)}'


@pytest.fixture
def credit_card_data():
    return {
        'number': '4111111111111111',
        'exp_date': '02/2026',
        'holder': 'John Doe',
        'cvv': '123',
    }


@pytest.fixture
def credit_card_data_encrypt():
    return {
        'number': 'b9f9540638c0afc987609227f170f6923dc7cd48d0bf5dffc1caf8debaa5af7f',
        'exp_date': '2028-02-28',
        'holder': 'John Doe',
        'cvv': '123',
    }


@pytest.fixture
def create_credit_card(credit_card_data_encrypt):
    return CreditCard.objects.create(**credit_card_data_encrypt)


@pytest.mark.django_db
def test_create_credit_card(api_client, credit_card_data, get_tokens_for_user):
    url = reverse('creditcard-list')
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    response = api_client.post(url, credit_card_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CreditCard.objects.count() == 1


@pytest.mark.django_db
def test_create_credit_card_invalid_data(api_client, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
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
def test_get_credit_card(api_client, create_credit_card, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    url = reverse('creditcard-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['holder'] == create_credit_card.holder


@pytest.mark.django_db
def test_get_credit_card_detail(api_client, create_credit_card, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['holder'] == create_credit_card.holder


@pytest.mark.django_db
def test_update_credit_card(api_client, create_credit_card, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    updated_data = {
        'number': '4235647728025682',
        'exp_date': '02/2028',
        'holder': 'Jane Doe',
        'cvv': '789'
    }
    response = api_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    create_credit_card.refresh_from_db()
    assert create_credit_card.holder == 'Jane Doe'
    assert create_credit_card.number == 'b9f9540638c0afc987609227f170f6923dc7cd48d0bf5dffc1caf8debaa5af7f'


@pytest.mark.django_db
def test_patch_credit_card(api_client, create_credit_card, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    updated_data = {
        'cvv': '456',
    }
    response = api_client.patch(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    create_credit_card.refresh_from_db()
    assert create_credit_card.cvv == '456'


@pytest.mark.django_db
def test_delete_credit_card(api_client, create_credit_card, get_tokens_for_user):
    api_client.credentials(HTTP_AUTHORIZATION=get_tokens_for_user)
    url = reverse('creditcard-detail', args=[create_credit_card.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CreditCard.objects.count() == 0
