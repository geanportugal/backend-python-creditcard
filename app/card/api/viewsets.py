import json
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .utils import request_schema_dict
from card.models import CreditCard
from .serializers import CreditCardSerializer


class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]
    queryset = CreditCard.objects.all()
     
    def perform_create(self, serializer):
        # Limpando e validando os dados antes de salvar
        holder = serializer.validated_data['holder'].strip()
        # Criar e salvar o objeto no banco de dados
        serializer.save(holder=holder)

    @swagger_auto_schema(request_body=request_schema_dict,)
    def create(self, request):
        return super().create(request)
