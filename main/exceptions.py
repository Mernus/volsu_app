class TokenAuthError(Exception):
    """
    Exception for any error with JWT authentication token.

    Args:
        username (str): The user username who faced the problem
        email (str): The user email who faced the problem
        message (:obj:`str`, optional): Some message, if other exception raised

    Attributes:
        credentials (dict): The user credentials who faced the problem
        message (str): Exception message

    """
    def __init__(self, username: str, email: str, message: str = None):
        if message is None:
            message = "some troubles with authentication via token"
        else:
            message = message.lower()
        self.credentials = {'username': username, 'email': email}
        self.message = f"{self.credentials['username']}({self.credentials['email']}): {message}"

    def __str__(self) -> str:
        formatted_message = f"[{self.__class__.__name__}]: {self.message}"
        return formatted_message
