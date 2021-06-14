from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


def verify_token(attrs: dict) -> dict:
    """
    Verify JWT token

    Args:
        attrs (dict): dict that contains tokens to verify it, {'token': <sometoken>}

    Returns:
        {} - empty dict

    Raises:
        TokenError - token invalid or expired

    """
    UntypedToken(attrs['token'])

    return {}


def obtain_token(attrs: dict) -> dict:
    """
    Create new JWT token based on username and password

    Args:
        attrs (dict): username and password

    Returns:
        data (dict): refresh and access tokens

    Raises:
        AuthenticationFailed - nonexistent or 'deleted' user
        TokenError - token invalid or expired

    """
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


def refresh_token(attrs: dict) -> dict:
    """
    Get new access token based on refresh token

    Args:
        attrs (dict): refresh token

    Returns:
        data (dict): access token

    Raises:
        TokenError - token invalid or expired

    """
    refresh = RefreshToken(attrs['refresh'])

    data = {'access': str(refresh.access_token)}
    return data


def get_tokens(user: 'User', password: str, request: 'Request') -> dict[str, str]:
    """
    Returns tokens that will be passed to this serializer

    Args:
        request (Request): Passed request
        user (User): User
        password (str): User password

    Returns:
        {'access_token': <sometoken>} if no need to generate new token,
        data(dict) otherwise

    Raises:
        TokenError, TokenBackendError, AuthenticationFailed - any troubles with auth by JWT token
    """
    access = request.session.get('jwt_access')
    data = {}
    print(f"Access: {access}")
    if access is None:
        print(f"Obtain")
        data = obtain_token({'username': user.username, 'password': password})
    else:
        try:
            print(f"Verify")
            verify_token({'token': access})
        except TokenError:
            refresh = request.session.get('jwt_refresh')
            try:
                print(f"Verify")
                verify_token({'token': refresh})
                data = refresh_token({'refresh': refresh})
            except TokenError:
                print(f"Obtain")
                data = obtain_token({'username': user.username, 'password': password})
        if not data:
            data = {'access': access}

    return data


# TODO docs
def render_tags(tags: list['Tag']) -> list[str]:
    result = []
    for tag in tags:
        title_color = tag.title_color if tag.title_color else "#FFFFFF"
        back_color = tag.back_color if tag.back_color else "#000000"
        result.append(f"<span id='{tag.id}' class='badge py-1 mb-2' "
                      f"style='color: {title_color} !important;"
                      f"background-color: {back_color};'>"
                      f"{tag.title}</span>")

    return result
