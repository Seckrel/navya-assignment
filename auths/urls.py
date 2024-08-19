from django.urls import path
from auths.views import (
    CustomRefreshView, CustomTokenObtainPariView, CustomTokenVerifyView)

urlpatterns = [
    path('login/', CustomTokenObtainPariView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', CustomTokenVerifyView.as_view(), name='token_verify')
]
