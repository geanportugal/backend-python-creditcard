from rest_framework import viewsets
from card.models import CreditCard
from .serializers import CreditCardSerializer


class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer

    def get_queryset(self):
        return CreditCard.objects.all()
    
    def perform_create(self, serializer):
        # Limpando e validando os dados antes de salvar
        holder = serializer.validated_data['holder'].strip()
        # Criar e salvar o objeto no banco de dados
        serializer.save(holder=holder)
