# Klasa PaymentProcessor, która będzie główną klasą odpowiedzialną za przetwarzanie płatności, zwrotów oraz sprawdzanie statusu transakcji.

from payment_gateway import PaymentGateway, TransactionResult

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def processPayment(self, user_id: str, amount: float) -> TransactionResult:
        return self.gateway.charge(user_id, amount)
