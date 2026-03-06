from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, user_email: str) -> dict:
        raise NotImplementedError


class FakePaymentGateway(PaymentGateway):
    def charge(self, amount: float, user_email: str) -> dict:
        return {
            "success": True,
            "transaction_id": "TXN-FAKE-001",
            "amount": amount,
            "user_email": user_email,
            "message": "Payment approved.",
        }


class RejectedPaymentGateway(PaymentGateway):
    def charge(self, amount: float, user_email: str) -> dict:
        return {
            "success": False,
            "transaction_id": None,
            "amount": amount,
            "user_email": user_email,
            "message": "Payment rejected by provider.",
        }


class PaymentGatewayFactory:
    @staticmethod
    def create(provider: str) -> PaymentGateway:
        normalized_provider = provider.lower()

        if normalized_provider == "fake":
            return FakePaymentGateway()

        if normalized_provider == "rejected":
            return RejectedPaymentGateway()

        raise ValueError(f"Unsupported payment provider: {provider}")