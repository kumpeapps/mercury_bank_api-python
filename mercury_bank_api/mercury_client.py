"""Mercury Bank API Client."""

from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
import logging
import requests  # type: ignore

from .models.account import Account
from .models.transaction import TransactionResponse, Transaction


class MercuryBankAPIError(Exception):
    """Base exception for Mercury Bank API errors."""

    pass


class MercuryBankAPIClient:
    """
    Mercury Bank API Client for interacting with Mercury's banking API.

    This client provides methods to interact with Mercury Bank's API endpoints,
    including retrieving account information and transaction data.

    Example usage:
        client = MercuryBankAPIClient(api_token="your_api_token")
        accounts = client.get_accounts()
        transactions = client.get_transactions(account_id="account_123")
    """

    BASE_URL = "https://api.mercury.com/api/v1"

    def __init__(self, api_token: str, timeout: int = 30):
        """
        Initialize the Mercury Bank API client.

        Args:
            api_token: Your Mercury API token
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()

        # Set up authentication headers
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # Set up logging
        self.logger = logging.getLogger(__name__)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Mercury API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary

        Raises:
            MercuryBankAPIError: If the API request fails
        """
        url = urljoin(self.BASE_URL + "/", endpoint.lstrip("/"))

        try:
            response = self.session.request(
                method=method, url=url, params=params, json=data, timeout=self.timeout
            )

            # Log the request
            self.logger.debug(f"{method} {url} - Status: {response.status_code}")

            # Handle HTTP errors
            if response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f": {error_data['error']}"
                    elif "message" in error_data:
                        error_msg += f": {error_data['message']}"
                except ValueError:
                    error_msg += f": {response.text}"

                raise MercuryBankAPIError(error_msg)

            return response.json()

        except requests.exceptions.Timeout:
            raise MercuryBankAPIError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError:
            raise MercuryBankAPIError("Failed to connect to Mercury API")
        except requests.exceptions.RequestException as e:
            raise MercuryBankAPIError(f"Request failed: {str(e)}")

    def get_accounts(self) -> List[Account]:
        """
        Retrieve information about all your bank accounts.

        Returns:
            List of Account objects

        Raises:
            MercuryBankAPIError: If the API request fails
        """
        response_data = self._make_request("GET", "/accounts")

        accounts = []
        for account_data in response_data.get("accounts", []):
            try:
                account = Account.from_dict(account_data)
                accounts.append(account)
            except Exception as e:
                self.logger.warning(f"Failed to parse account data: {e}")

        return accounts

    def get_transactions(
        self,
        account_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        kind: Optional[str] = None,
    ) -> TransactionResponse:
        """
        Retrieve information about transactions for a specific account.

        Args:
            account_id: The ID of the account to get transactions for
            limit: Maximum number of transactions to return
            offset: Number of transactions to skip
            start_date: Start date filter (ISO format)
            end_date: End date filter (ISO format)
            status: Filter by transaction status (pending, sent, cancelled, failed)
            kind: Filter by transaction kind

        Returns:
            TransactionResponse object containing transactions and total count

        Raises:
            MercuryBankAPIError: If the API request fails
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if status is not None:
            params["status"] = status
        if kind is not None:
            params["kind"] = kind

        endpoint = f"/account/{account_id}/transactions"
        response_data = self._make_request("GET", endpoint, params=params)

        try:
            return TransactionResponse.from_dict(response_data)
        except Exception as e:
            self.logger.error(f"Failed to parse transaction response: {e}")
            raise MercuryBankAPIError(f"Failed to parse transaction response: {e}")

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """
        Get a specific account by its ID.

        Args:
            account_id: The ID of the account to retrieve

        Returns:
            Account object if found, None otherwise

        Raises:
            MercuryBankAPIError: If the API request fails
        """
        accounts = self.get_accounts()
        for account in accounts:
            if account.id == account_id:
                return account
        return None

    def get_transaction_by_id(
        self, account_id: str, transaction_id: str
    ) -> Optional[Transaction]:
        """
        Get a specific transaction by its ID.

        Args:
            account_id: The ID of the account
            transaction_id: The ID of the transaction

        Returns:
            Transaction object if found, None otherwise

        Raises:
            MercuryBankAPIError: If the API request fails
        """
        # Get all transactions for the account
        transaction_response = self.get_transactions(account_id)

        for transaction in transaction_response.transactions:
            if transaction.id == transaction_id:
                return transaction

        return None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session:
            self.session.close()
