from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from core.models import Transaction
from core.serializers.transaction_serializer import TransactionSerializer


class TransactionModelViewSet(ModelViewSet):
    allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'transaction_id'

    # TODO permission class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = serializer.instance
        return Response(instance.transaction_id, status=status.HTTP_201_CREATED, headers=headers)
