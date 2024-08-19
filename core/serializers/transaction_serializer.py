from rest_framework import serializers
from core.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    transaction_date = serializers.SerializerMethodField()

    def get_transaction_date(self, obj):
        return obj.transaction_created_on.strftime('%Y-%m-%d')

    class Meta:
        model = Transaction
        exclude = ('transaction_created_on', 'id', 'transaction_updated_on')
        extra_kwargs = {'password': {'write_only': True},
                        'transaction_status': {'write_only': True}}
