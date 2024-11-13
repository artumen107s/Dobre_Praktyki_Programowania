import unittest
from unittest.mock import Mock
from payment_processor import PaymentProcessor
from payment_gateway import PaymentGateway, TransactionResult

class TestPaymentProcessor(unittest.TestCase):
    def test_process_payment_success(self):
        # Mockowanie PaymentGateway
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.return_value = TransactionResult(success=True, transaction_id="12345", message="OK")
        
        # Inicjalizacja PaymentProcessor z mockiem
        processor = PaymentProcessor(gateway=gateway_mock)
        
        # Weryfikacja metody processPayment
        result = processor.processPayment("user_1", 100.0)
        
        self.assertTrue(result.success)
        self.assertEqual(result.transaction_id, "12345")
        self.assertEqual(result.message, "OK")

if __name__ == '__main__':
    unittest.main()
