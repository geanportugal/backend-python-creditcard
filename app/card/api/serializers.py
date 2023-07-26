import os
import re
from rest_framework import serializers
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.utils.dateparse import parse_date
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
                regex=r'^[A-Za-z\s]+$',
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
    
    exp_date = serializers.DateField()
    brand = serializers.CharField(required=False)

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
    
    
    def validate_number(self, value):
        # Validate the value field.
        value = value.replace(" ", "")
        regex = r'^[0-9]+$'
        match = re.match(regex, value) 
        if bool(match) is False:
            raise serializers.ValidationError("Invalid credit card")
        try:
            # Validate the credit card number
            credit_card_number = ValidatedCreditCard(value).is_valid()
        except ValueError:
            raise serializers.ValidationError("Invalid credit card")
        else:
            if not credit_card_number:
                raise serializers.ValidationError("Invalid credit card")
        
        encryptor = CreditCardEncryptor(self.key, self.salt)
        value = encryptor.encrypt_credit_card(value).hex()
        return value
    
    def to_internal_value(self, data):
        # Get the request method.
        request = self.context['request']
        method = request.method
        # Check if the request method is PUT or PATCH.
        if method in ('PUT', 'PATCH'):
            # Check if the "exp_date" and "number" fields are present in the data.
            if 'exp_date' not in data or 'number' not in data:
                # Do not require the "exp_date" and "number" fields in the update.
                return data
        try:
            # Convert the "exp_date" string in the format "02/2026" to a datetime.date object
            date_obj = datetime.strptime(data['exp_date'], '%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Use 'MM/YYYY' format.")
        # Calculate the last day of the month
        last_day_of_month = date_obj.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        data['exp_date'] = last_day_of_month
        
        credit_card = ValidatedCreditCard(data['number']).is_valid()
        if credit_card is True:
            brand = ValidatedCreditCard(data['number']).get_brand()
            if not brand:
                raise serializers.ValidationError("Brand not Found!")
    
            data['brand'] = brand 

        return super().to_internal_value(data)