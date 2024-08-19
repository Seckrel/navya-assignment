from django.urls import path
from auths.views import (
    CustomRefreshView, CustomTokenObtainPariView, CustomTokenVerifyView, SignUp)

urlpatterns = [
    path('login/', CustomTokenObtainPariView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('signup/', SignUp.as_view(), name='signup-manager')
]
