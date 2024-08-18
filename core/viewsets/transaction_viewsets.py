from rest_framework.viewsets import ModelViewSet
from core.models import Transaction
from core.serializers.transaction_serializer import TransactionSerializer


class TransactionModelViewSet(ModelViewSet):
    allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
