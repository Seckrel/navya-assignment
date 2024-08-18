from rest_framework.serializers import ModelSerializer
from core.models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('transaction_status',)
