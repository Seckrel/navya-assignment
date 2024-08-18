from rest_framework import serializers
from core.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    transaction_date = serializers.SerializerMethodField()

    def get_transaction_date(self, obj):
        return obj.transaction_created_on.strftime('%Y-%m-%d')

    class Meta:
        model = Transaction
        exclude = ('transaction_status', 'transaction_created_on',)
