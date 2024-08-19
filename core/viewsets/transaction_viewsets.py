from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from core.models import Transaction
from core.serializers.transaction_serializer import TransactionSerializer
from core.permissions import StaffAllowedPermission
from django.db import IntegrityError


class TransactionModelViewSet(ModelViewSet):
    allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'transaction_id'
    permission_classes = [StaffAllowedPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            instance = serializer.instance
        except IntegrityError as e:
            return Response(str(e), status=400)

        return Response(instance.transaction_id, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
