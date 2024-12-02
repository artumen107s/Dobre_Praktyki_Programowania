# Definicje wyjątków

class NetworkException(Exception):
    """Wyjątek - problemy z siecią."""
    pass


class PaymentException(Exception):
    """Wyjątek - problemy podczas przetwarzania płatności."""
    pass


class RefundException(Exception):
    """Wyjątek - problemy podczas realizacji zwrotu."""
    pass
