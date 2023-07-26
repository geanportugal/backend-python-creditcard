from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
from .utils import request_schema_dict
from card.models import CreditCard
from .serializers import CreditCardSerializer


class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer
    permission_classes = (DjangoModelPermissions, IsAuthenticated)

    queryset = CreditCard.objects.all()
     
    @swagger_auto_schema(request_body=request_schema_dict,)
    def create(self, request):
        return super().create(request)
    
    def perform_create(self, serializer):
        # Limpando e validando os dados antes de salvar
        holder = serializer.validated_data['holder'].strip()
        # Criar e salvar o objeto no banco de dados
        if serializer.is_valid():
            serializer.save(holder=holder)
