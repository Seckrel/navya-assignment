from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from auths.utils.cookie import set_cookie
from django.conf import settings
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from auths.permissions import IsManagerPermission
from rest_framework.permissions import AllowAny


class CustomTokenObtainPariView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response = set_cookie(response, settings.AUTH_COOKIE['access']['name'],
                                  access_token, settings.AUTH_COOKIE['access']['max_age'])
            response = set_cookie(response, settings.AUTH_COOKIE['refresh']['name'],
                                  refresh_token, settings.AUTH_COOKIE['refresh']['max_age'])
            del response.data['access']
            del response.data['refresh']
            response.data['message'] = "Login Successful"
        else:
            response.data['message'] = "Failed To Login"
            response.status_code = 400

        return response


class CustomRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get(
            settings.AUTH_COOKIE['refresh']['name'])

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            response = set_cookie(response, settings.AUTH_COOKIE['access']['name'],
                                  access_token, settings.AUTH_COOKIE['access']['max_age'])
            del response.data['access']
            response.data['message'] = "Session Refreshed Successfully"
        else:
            response.data['message'] = "Failed To Refresh The Session"
            response.status_code = 400

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get(
            settings.AUTH_COOKIE['access']['name'])

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=204)
        response.delete_cookie(settings.AUTH_COOKIE['access']['name'])
        response.delete_cookie(settings.AUTH_COOKIE['refresh']['name'])
        return response


class SignUp(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        manager_grp = Group.objects.get(name="Manager")
        instance.groups.add(manager_grp)
        instance.save()

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SignUpStaffUser(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsManagerPermission]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        instance.is_admin = True
        instance.save()

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
