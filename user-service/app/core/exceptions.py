class UserAlreadyExistsException(Exception):
    """Raised when a user tries to register with an existing email."""
    pass


class UserNotFoundException(Exception):
    """Raised when the requested user profile is not found."""
    pass