import os
from rest_framework import serializers
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from django.conf import settings
from card.models import CreditCard
from .utils import CreditCardEncryptor, ValidatedCreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    holder = serializers.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(
                3, 
                message='The holder name must be at least 3 characters long'
            ),
            RegexValidator(
                regex=r'^[A-Za-z0-9]+$',
                message='Only alphanumeric characters are allowed.',
                code='invalid_input'
            )
        ]
    )
    cvv = serializers.CharField(
        max_length=4, 
        required=False,
        allow_null=True,
        validators=[
            MinLengthValidator(
                3, 
                message='The security code must be at least 3 characters long'
            )
        ])
    number = serializers.CharField(
        max_length=255, 
        validators=[
            UniqueValidator(
                queryset=CreditCard.objects.all(),
                message='Credit Card alred exists'),
        ])
    
    exp_date = serializers.DateField(format='YYYY-MM-DD')
    brand = serializers.CharField(write_only=True)

    class Meta:
        model = CreditCard
        fields = '__all__'
        read_only_fields = ['brand']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The secret key used for encryption
        self.key = settings.SECRET_KEY_CARD
        self.salt = settings.SALT

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['exp_date'] = instance.exp_date.strftime('%m/%Y')
        return representation

    def to_internal_value(self, data):
        try:
            # Validate the credit card number
            credit_card_number = ValidatedCreditCard(data['number']).is_valid()
        except ValueError:
            raise serializers.ValidationError("Invalid credit card")
        else:
            if not credit_card_number:
                raise serializers.ValidationError("Invalid credit card")

        try:
            # Convert the "exp_date" string in the format "02/2026" to a datetime.date object
            date_obj = datetime.strptime(data['exp_date'], '%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Use 'MM/YYYY' format.")

        try:
            # Get the brand of the credit card (Visa, MasterCard, etc.)
            brand = ValidatedCreditCard(data['number']).get_brand()
        except ValueError:
            raise serializers.ValidationError('Invalid brand')

        data['brand'] = brand
        encryptor = CreditCardEncryptor(self.key, self.salt)
        
        data['number'] = encryptor.encrypt_credit_card(data['number']).hex()
       
        # Calculate the last day of the month
        last_day_of_month = date_obj.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        data['exp_date'] = last_day_of_month

        return super().to_internal_value(data)