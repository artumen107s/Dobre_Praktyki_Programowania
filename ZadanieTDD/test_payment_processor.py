# test_payment_processor.py

import unittest
from unittest.mock import Mock, patch
from payment_processor import PaymentProcessor
from payment_gateway import PaymentGateway, TransactionResult, TransactionStatus
from exceptions import NetworkException, PaymentException, RefundException

class TestPaymentProcessor(unittest.TestCase):
    
    @patch("time.sleep", return_value=None)
    def test_process_payment_success(self, _):
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
        
    # Mockowanie sleep, aby testy były szybsze
    @patch("time.sleep", return_value=None)
    def test_process_payment_invalid_amount(self, _):
        # Mockowanie PaymentGateway
        gateway_mock = Mock(spec=PaymentGateway)
        processor = PaymentProcessor(gateway=gateway_mock)
        
        # Sprawdzenie, czy wywołanie z ujemną kwotą zgłasza ValueError
        with self.assertRaises(ValueError):
            processor.processPayment("user_1", -50.0)

    @patch("time.sleep", return_value=None)
    def test_process_payment_empty_user_id(self, _):
        # Mockowanie PaymentGateway
        gateway_mock = Mock(spec=PaymentGateway)
        processor = PaymentProcessor(gateway=gateway_mock)
        
        # Sprawdzenie, czy wywołanie z pustym user_id zgłasza ValueError
        with self.assertRaises(ValueError):
            processor.processPayment("", 50.0)

    @patch("time.sleep", return_value=None)  
    def test_process_payment_network_exception(self, _):
        # Mockowanie PaymentGateway
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.side_effect = NetworkException("Network error")

        processor = PaymentProcessor(gateway=gateway_mock)

        # Sprawdzenie, czy po 3 próbach rzucany jest NetworkException
        result = processor.processPayment("user_1", 100.0)

        # Wynik powinien wskazywać na niepowodzenie
        self.assertFalse(result.success)
        self.assertIn("Network error", result.message)

    @patch("time.sleep", return_value=None)
    def test_process_payment_payment_exception(self, _):
        # Mockowanie PaymentGateway
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.side_effect = PaymentException("Payment error")

        processor = PaymentProcessor(gateway=gateway_mock)

        # Sprawdzenie, czy payment_exception kończy się niepowodzeniem
        result = processor.processPayment("user_1", 100.0)

        # Wynik powinien wskazywać na niepowodzenie bez powtarzania prób
        self.assertFalse(result.success)
        self.assertIn("Payment error", result.message)

    @patch("time.sleep", return_value=None)
    def test_log_payment_success(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.return_value = TransactionResult(success=True, transaction_id="12345", message="OK")

        processor = PaymentProcessor(gateway=gateway_mock)

        with self.assertLogs('payment_processor', level='INFO') as log:
            processor.processPayment("user_1", 100.0)
            # Sprawdzenie, czy log zawiera komunikat o sukcesie
            self.assertIn("Payment successful for user user_1 with amount 100.0", log.output[0])

    @patch("time.sleep", return_value=None)
    def test_log_network_exception(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.side_effect = NetworkException("Network error")

        processor = PaymentProcessor(gateway=gateway_mock)

        with self.assertLogs('payment_processor', level='ERROR') as log:
            processor.processPayment("user_1", 100.0)
            # Sprawdzenie, czy log zawiera komunikat o błędzie sieci
            self.assertIn("Network error during payment for user user_1", log.output[0])

    @patch("time.sleep", return_value=None)
    def test_log_payment_exception(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.charge.side_effect = PaymentException("Payment error")

        processor = PaymentProcessor(gateway=gateway_mock)

        with self.assertLogs('payment_processor', level='ERROR') as log:
            processor.processPayment("user_1", 100.0)
            # Sprawdzenie, czy log zawiera komunikat o błędzie płatności
            self.assertIn("Payment failed for user user_1 due to payment exception", log.output[0])

    @patch("time.sleep", return_value=None)
    def test_refund_payment_success(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.refund.return_value = TransactionResult(success=True, transaction_id="12345", message="Refund successful")

        processor = PaymentProcessor(gateway=gateway_mock)

        # Weryfikacja poprawnego zwrotu
        result = processor.refundPayment("12345")
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Refund successful")

    @patch("time.sleep", return_value=None)
    def test_refund_payment_refund_exception(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.refund.side_effect = RefundException("Refund error")

        processor = PaymentProcessor(gateway=gateway_mock)

        # Weryfikacja niepowodzenia zwrotu z powodu RefundException
        result = processor.refundPayment("12345")
        self.assertFalse(result.success)
        self.assertIn("Refund error", result.message)

    @patch("time.sleep", return_value=None)
    def test_refund_payment_network_exception(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.refund.side_effect = NetworkException("Network error during refund")

        processor = PaymentProcessor(gateway=gateway_mock)

        # Weryfikacja niepowodzenia po 3 próbach
        result = processor.refundPayment("12345")
        self.assertFalse(result.success)
        self.assertIn("Network error during refund", result.message)

    @patch("time.sleep", return_value=None)
    def test_get_payment_status_completed(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.get_status.return_value = TransactionStatus.COMPLETED

        processor = PaymentProcessor(gateway=gateway_mock)
        status = processor.getPaymentStatus("12345")

        self.assertEqual(status, TransactionStatus.COMPLETED)

    @patch("time.sleep", return_value=None)
    def test_get_payment_status_pending(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.get_status.return_value = TransactionStatus.PENDING

        processor = PaymentProcessor(gateway=gateway_mock)
        status = processor.getPaymentStatus("12345")

        self.assertEqual(status, TransactionStatus.PENDING)

    @patch("time.sleep", return_value=None)
    def test_get_payment_status_failed(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.get_status.return_value = TransactionStatus.FAILED

        processor = PaymentProcessor(gateway=gateway_mock)
        status = processor.getPaymentStatus("12345")

        self.assertEqual(status, TransactionStatus.FAILED)

    @patch("time.sleep", return_value=None)
    def test_get_payment_status_network_exception(self, _):
        gateway_mock = Mock(spec=PaymentGateway)
        gateway_mock.get_status.side_effect = NetworkException("Network error during status retrieval")

        processor = PaymentProcessor(gateway=gateway_mock)

        with self.assertRaises(NetworkException):
            processor.getPaymentStatus("12345")


if __name__ == '__main__':
    unittest.main()
