class PaymentServiceException(Exception):
    """Base exception for Payment Service."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(self.message)


class PaymentNotFoundException(PaymentServiceException):
    """Raised when a payment is not found."""

    def __init__(
        self,
        message: str = "Payment not found"
    ):
        super().__init__(
            message=message,
            status_code=404
        )


class PaymentAlreadyExistsException(PaymentServiceException):
    """Raised when a payment already exists."""

    def __init__(
        self,
        message: str = "Payment already exists"
    ):
        super().__init__(
            message=message,
            status_code=409
        )


class PaymentProcessingException(PaymentServiceException):
    """Raised when payment processing fails."""

    def __init__(
        self,
        message: str = "Payment processing failed"
    ):
        super().__init__(
            message=message,
            status_code=400
        )