import time
import logging
from payment_gateway import PaymentGateway, TransactionResult, TransactionStatus
from exceptions import PaymentException, NetworkException, RefundException

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def processPayment(self, user_id: str, amount: float) -> TransactionResult:
        # Walidacja danych wejściowych
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        # Obsługa przetwarzania płatności z próbami ponownymi w przypadku NetworkException
        for attempt in range(3):
            try:
                result = self.gateway.charge(user_id, amount)
                # Logowanie sukcesu
                logger.info(f"Payment successful for user {user_id} with amount {amount}. Transaction ID: {result.transaction_id}")
                return result
            except NetworkException as e:
                if attempt < 2:
                     # Czekanie przed ponowną próbą
                    time.sleep(1) 
                else:
                    # Logowanie błędu sieci
                    logger.error(f"Network error during payment for user {user_id}. Error: {e}")
                    return TransactionResult(success=False, transaction_id="", message=str(e))
            except PaymentException as e:
                # Logowanie błędu płatności
                logger.error(f"Payment failed for user {user_id} due to payment exception. Error: {e}")
                return TransactionResult(success=False, transaction_id="", message=str(e))

    def refundPayment(self, transaction_id: str) -> TransactionResult:
        # Walidacja danych wejściowych
        if not transaction_id:
            raise ValueError("Transaction ID cannot be empty.")
        
        # Obsługa zwrotu z kilkoma próbami ponownymi w przypadku NetworkException
        for attempt in range(3):
            try:
                result = self.gateway.refund(transaction_id)
                # Logowanie sukcesu zwrotu
                logger.info(f"Refund successful for transaction ID {transaction_id}.")
                return result
            except NetworkException as e:
                if attempt < 2:
                    time.sleep(1)  
                else:
                    # Logowanie błędu sieci
                    logger.error(f"Network error during refund for transaction ID {transaction_id}. Error: {e}")
                    return TransactionResult(success=False, transaction_id=transaction_id, message=str(e))
            except RefundException as e:
                # Logowanie błędu zwrotu
                logger.error(f"Refund failed for transaction ID {transaction_id} due to refund exception. Error: {e}")
                return TransactionResult(success=False, transaction_id=transaction_id, message=str(e))
            
    def getPaymentStatus(self, transaction_id: str) -> TransactionStatus:
        # Walidacja danych wejściowych
        if not transaction_id:
            raise ValueError("Transaction ID cannot be empty.")
        
        # Obsługa pobierania statusu z kilkoma próbami ponownymi w przypadku NetworkException
        for attempt in range(3):
            try:
                status = self.gateway.get_status(transaction_id)
                # Logowanie sukcesu pobrania statusu
                logger.info(f"Status retrieval successful for transaction ID {transaction_id}: {status.name}")
                return status
            except NetworkException as e:
                if attempt < 2:
                    time.sleep(1)
                else:
                    # Logowanie błędu sieci przy pobieraniu statusu
                    logger.error(f"Network error during status retrieval for transaction ID {transaction_id}. Error: {e}")
                    # Rzucenie wyjątku po nieudanych próbach
                    raise e  