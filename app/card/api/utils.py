from django.core.validators import RegexValidator
from rest_framework import serializers

def validate_holder(value):
    allowed_characters = r'^[a-zA-Z ]+$'  # Apenas letras e espaços em branco são permitidos
    if not RegexValidator(allowed_characters).match(value):
        raise serializers.ValidationError("O nome do titular deve conter apenas letras e espaços em branco.")
    