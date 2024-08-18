from rest_framework.routers import DefaultRouter
from core.viewsets.transaction_viewsets import TransactionModelViewSet

router = DefaultRouter()

router.register('transactions', TransactionModelViewSet)

urlpatterns = [
]

urlpatterns += router.urls