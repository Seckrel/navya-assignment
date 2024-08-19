from rest_framework import serializers
from core.models import Transaction, TransactionStatus


class TransactionSerializer(serializers.ModelSerializer):
    transaction_date = serializers.DateField()
    transaction_status = serializers.ChoiceField(
        choices=TransactionStatus.choices, required=False, write_only=True)

    def get_transaction_date(self, obj):
        return obj.transaction_date.strftime('%Y-%m-%d')

    class Meta:
        model = Transaction
        exclude = ('id', )
        extra_kwargs = {'password': {'write_only': True},
                        'transaction_status': {'write_only': True}}
