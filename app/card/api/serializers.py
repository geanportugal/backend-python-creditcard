from rest_framework import serializers
from cryptography.fernet import Fernet
from django.core.validators import MinLengthValidator, RegexValidator
from decouple import config
from card.models import CreditCard
from .utils import validate_holder



class CreditCardSerializer(serializers.ModelSerializer):
    holder = serializers.CharField(max_length=30, validators=[MinLengthValidator(3), validate_holder])
    cvv = serializers.CharField(max_length=4, required=False)

    class Meta:
        model = CreditCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cipher_suite = Fernet(config('SECRET_KEY'))  # chave de criptografia 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Criptografa o número do cartão de crédito antes de retornar os dados serializados
        if 'number' in data:
            data['number'] = self.cipher_suite.encrypt(data['number'].encode()).decode()
        return data
    
    def create(self, validated_data):
        # Limpando e validando os dados antes de salvar
        holder = validated_data['holder'].strip()
        # Criar e salvar o objeto no banco de dados
        return CreditCard.objects.create(holder=holder, **validated_data)
