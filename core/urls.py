from django.urls import path
from rest_framework.routers import DefaultRouter
from core.viewsets.transaction_viewsets import TransactionModelViewSet
from core.views import ListTransactionPdf, ApproveNewTransaction

router = DefaultRouter()

router.register('transactions', TransactionModelViewSet)

urlpatterns = [
    path("pdf/transactions/", ListTransactionPdf.as_view()),
    path("pdf/transactions/<str:transaction_id>/", ListTransactionPdf.as_view()),
    path('transactions/approve/<str:transaction_id>/',
         ApproveNewTransaction.as_view()),
]

urlpatterns += router.urls
