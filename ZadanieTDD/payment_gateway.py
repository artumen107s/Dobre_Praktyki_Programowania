#  Interfejs PaymentGateway i klasy pomocnicze

from enum import Enum
from typing import Optional

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionResult:
    def __init__(self, success: bool, transaction_id: str, message: str = "", error_code: Optional[int] = None):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message
        self.error_code = error_code

class PaymentGateway:
    def charge(self, user_id: str, amount: float) -> TransactionResult:
        """Symulowana metoda do obciążenia konta."""
        raise NotImplementedError("This method should be written properly :)")

    def refund(self, transaction_id: str) -> TransactionResult:
        """Symulowana metoda do zwrotu płatności."""
        raise NotImplementedError("This method should be written properly :)")

    def get_status(self, transaction_id: str) -> TransactionStatus:
        """Symulowana metoda do pobrania statusu transakcji."""
        raise NotImplementedError("This method should be written properly :)")
