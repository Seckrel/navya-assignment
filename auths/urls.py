from django.urls import path
from auths.views import (
    CustomRefreshView, CustomTokenObtainPariView,
    CustomTokenVerifyView, SignUp, SignUpStaffUser, LogoutView)

urlpatterns = [
    path('login/', CustomTokenObtainPariView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup-manager'),
    path('signup/staff/', SignUpStaffUser.as_view(), name='signup-staff')
]
