from django.contrib.auth import authenticate
from django.core.cache import cache

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


# TODO docs
def verify_token(attrs):
    UntypedToken(attrs['token'])

    return {}


# TODO docs
def obtain_token(attrs):
    authenticate_kwargs = {
        'username': attrs['username'],
        'password': attrs['password'],
    }

    user = authenticate(**authenticate_kwargs)

    if user is None or not user.is_active:
        raise AuthenticationFailed('No active account with provided credentials')

    refresh = RefreshToken.for_user(user)
    data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
    return data


# TODO docs
def refresh_token(attrs):
    refresh = RefreshToken(attrs['refresh'])

    data = {'access': str(refresh.access_token)}
    return data


def get_tokens(username: str, password: str) -> dict[str, str]:
    """
    Returns tokens that will be passed to this serializer

    Args:
        username (str): User username
        password (str): User password

    Returns:
        {'access_token': <sometoken>} if no need to generate new token,
        data(dict) otherwise

    """
    access = cache.get('jwt_access')
    data = {}

    if access is None:
        data = obtain_token({'username': username, 'password': password})
    else:
        try:
            verify_token({'token': access})
        except TokenError:
            refresh = cache.get('jwt_refresh')
            try:
                verify_token({'token': refresh})

                data = refresh_token({'refresh': refresh})
            except TokenError:
                data = obtain_token({'username': username, 'password': password})
        if not data:
            data = {'access': access}

    return data
