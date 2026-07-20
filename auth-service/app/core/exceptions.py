class UserAlreadyExistsException(Exception):
    """Raised when a user tries to register with an existing email."""
    pass


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""
    pass


class UserNotFoundException(Exception):
    """Raised when a user cannot be found."""
    pass