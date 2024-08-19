from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from auths.utils.cookie import set_cookie
from django.conf import settings


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
