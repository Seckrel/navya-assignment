from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class CookieBasedJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Takes access token from either header or cookie to authenticate users

        Args:
            request (Request): object of request class

        Returns:
            Option[User|None]: on success returns instance of logged in user
        """
        try:
            header = self.get_header(request)
            if header is None:
                raw_token = request.COOKIES.get(
                    settings.AUTH_COOKIE['access']['name'])
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except Exception as e:
            return None
