from django.conf import settings
from rest_framework.response import Response


def set_cookie(response: Response, cookie_name, value, cookie_max_age,
               cookie_secure=settings.AUTH_COOKIE['secure'],
               cookie_path=settings.AUTH_COOKIE['path'],
               cookie_same_site=settings.AUTH_COOKIE['same_site'],
               cookie_http_only=settings.AUTH_COOKIE['http_only'], ):
    """
    Sets Cookies to response object

    Args:
        response (Response): DRF response object
        cookie_name (str): name of cokkie
        value (str): value of the cookie in cause of auth this is the Token value
        cookie_max_age (int): max age of cookie in seconds
        cookie_secure (bool, optional): makes cookie secure in production if True. Defaults to settings.AUTH_COOKIE.secure.
        cookie_path (str, optional): path to the cookie. Defaults to settings.AUTH_COOKIE.path.
        cookie_same_site (str, optional): strict | lazy | None. Defaults to settings.AUTH_COOKIE.same_site.
        cookie_http_only (bool, optional): makes cookie http only if True. Defaults to settings.AUTH_COOKIE.http_only.

    Returns:
        Response: DRF response object with a new cookie
    """

    response.set_cookie(
        cookie_name,
        value,
        max_age=cookie_max_age,
        path=cookie_path,
        samesite=cookie_same_site,
        httponly=cookie_http_only,
        secure=cookie_secure
    )
    return response
