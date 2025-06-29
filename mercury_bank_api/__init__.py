"""Mercury Bank API Python Client.

A comprehensive Python client for the Mercury Bank API, providing easy access
to account information and transaction data.

Usage:
    from mercury_bank_api import MercuryBankAPIClient

    client = MercuryBankAPIClient(api_token="your_token_here")
    accounts = client.get_accounts()
    transactions = client.get_transactions(account_id="account_123")
"""

from .mercury_client import MercuryBankAPIClient, MercuryBankAPIError
from .models import (
    Account,
    Transaction,
    TransactionResponse,
    TransactionDetails,
    Address,
    Attachment,
)

__version__ = "1.0.0"
__all__ = [
    "MercuryBankAPIClient",
    "MercuryBankAPIError",
    "Account",
    "Transaction",
    "TransactionResponse",
    "TransactionDetails",
    "Address",
    "Attachment",
]
