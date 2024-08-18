from django.urls import path
from rest_framework.routers import DefaultRouter
from core.viewsets.transaction_viewsets import TransactionModelViewSet
from core.views import ListTransactionPdf

router = DefaultRouter()

router.register('transactions', TransactionModelViewSet)

urlpatterns = [
    path("pdf/transactions/", ListTransactionPdf.as_view())
]

urlpatterns += router.urls
