# Mercury Bank API Python Client

A comprehensive Python client library for interacting with the Mercury Bank API. This library provides easy access to account information, transaction data, and other Mercury banking services.

## Features

- **Complete API Coverage**: Full support for Mercury Bank's transaction and account endpoints
- **Type Safety**: Comprehensive type hints and data models for all API responses
- **Error Handling**: Proper exception handling with custom error types
- **Robust Parsing**: Built-in parsing for complex transaction details and routing information
- **Easy to Use**: Simple, intuitive interface with sensible defaults
- **Well Documented**: Comprehensive documentation and examples

## Installation

### Prerequisites

- Python 3.7+
- A Mercury Bank API token (get one from your [Mercury dashboard](https://mercury.com/settings/tokens))

### Install from PyPI (Recommended)

```bash
pip install mercury-bank-api
```

## Quick Start

```python
from mercury_bank_api import MercuryBankAPIClient

# Initialize the client with your API token
client = MercuryBankAPIClient(api_token="your_api_token_here")

# Get all accounts
accounts = client.get_accounts()
for account in accounts:
    print(f"{account.name}: ${account.currentBalance:.2f}")

# Get transactions for a specific account
transactions = client.get_transactions(account_id="account_123", limit=10)
for transaction in transactions.transactions:
    print(f"${transaction.amount:.2f} - {transaction.counterpartyName}")
```

**Note:** Make sure to replace `"your_api_token_here"` with your actual Mercury API token from your [Mercury dashboard](https://mercury.com/settings/tokens).

## API Reference

### MercuryBankAPIClient

The main client class for interacting with the Mercury Bank API.

#### Initialization

```python
client = MercuryBankAPIClient(
    api_token="your_token",  # Required: Your Mercury API token
    timeout=30               # Optional: Request timeout in seconds (default: 30)
)
```

#### Methods

##### `get_accounts() -> List[Account]`

Retrieve information about all your bank accounts.

```python
accounts = client.get_accounts()
for account in accounts:
    print(f"Account: {account.name}")
    print(f"Balance: ${account.currentBalance:.2f}")
    print(f"Available: ${account.availableBalance:.2f}")
    print(f"Status: {account.status}")
```

##### `get_transactions(account_id, **kwargs) -> TransactionResponse`

Retrieve transactions for a specific account with optional filtering.

**Parameters:**
- `account_id` (str): The ID of the account
- `limit` (int, optional): Maximum number of transactions to return
- `offset` (int, optional): Number of transactions to skip
- `start_date` (str, optional): Start date filter (ISO format)
- `end_date` (str, optional): End date filter (ISO format)
- `status` (str, optional): Filter by status ("pending", "sent", "cancelled", "failed")
- `kind` (str, optional): Filter by transaction kind

```python
# Get recent transactions
transactions = client.get_transactions(
    account_id="account_123",
    limit=50,
    status="pending"
)

print(f"Total transactions: {transactions.total}")
for transaction in transactions.transactions:
    print(f"${transaction.amount:.2f} - {transaction.counterpartyName}")
```

##### `get_account_by_id(account_id) -> Optional[Account]`

Get a specific account by its ID.

```python
account = client.get_account_by_id("account_123")
if account:
    print(f"Found account: {account.name}")
```

##### `get_transaction_by_id(account_id, transaction_id) -> Optional[Transaction]`

Get a specific transaction by its ID.

```python
transaction = client.get_transaction_by_id("account_123", "transaction_456")
if transaction:
    print(f"Transaction: ${transaction.amount:.2f}")
```

## Data Models

### Account

Represents a Mercury bank account.

**Key Attributes:**
- `id`: Account ID
- `name`: Account name
- `currentBalance`: Current account balance
- `availableBalance`: Available balance
- `accountNumber`: Account number
- `routingNumber`: Routing number
- `status`: Account status ("active", "deleted", "pending", "archived")
- `type`: Account type ("mercury", "external", "recipient")

### Transaction

Represents a Mercury bank transaction.

**Key Attributes:**
- `id`: Transaction ID
- `amount`: Transaction amount
- `counterpartyName`: Name of the counterparty
- `createdAt`: Transaction creation date
- `status`: Transaction status ("pending", "sent", "cancelled", "failed")
- `kind`: Transaction type (see API docs for all types)
- `details`: Detailed routing and payment information
- `attachments`: List of transaction attachments

### TransactionResponse

Response object containing transactions and metadata.

**Attributes:**
- `total`: Total number of transactions matching the query
- `transactions`: List of Transaction objects

## Error Handling

The client raises `MercuryBankAPIError` for API-related errors:

```python
from mercury_bank_api import MercuryBankAPIClient, MercuryBankAPIError

try:
    client = MercuryBankAPIClient(api_token="invalid_token")
    accounts = client.get_accounts()
except MercuryBankAPIError as e:
    print(f"API Error: {e}")
```

### Common Error Messages

- **401 Unauthorized**: Invalid or missing API token. Check your token in the [Mercury dashboard](https://mercury.com/settings/tokens)
- **403 Forbidden**: Token doesn't have sufficient permissions for the requested operation
- **404 Not Found**: The requested resource (account, transaction) doesn't exist
- **429 Too Many Requests**: Rate limit exceeded. Implement retry logic with backoff

## Authentication

The Mercury API uses Bearer token authentication. You can obtain an API token from your [Mercury dashboard](https://mercury.com/settings/tokens).

**Security Note:** Never commit your API token to version control. Use environment variables:

```python
import os
from mercury_bank_api import MercuryBankAPIClient

api_token = os.getenv("MERCURY_API_TOKEN")
client = MercuryBankAPIClient(api_token=api_token)
```

## Examples

See `examples.py` for comprehensive usage examples, including:

- Fetching all accounts
- Retrieving transactions with filtering
- Finding specific transactions
- Working with transaction details and attachments

To run the examples:

```bash
export MERCURY_API_TOKEN="your_token_here"
python examples.py
```

## API Token Permissions

Make sure your API token has the appropriate permissions:

- **Read Only**: Can fetch accounts and transactions
- **Read and Write**: Additionally can initiate transactions (requires IP whitelist)
- **Custom**: Can be configured with specific scopes

For this client library, a **Read Only** token is sufficient for all implemented features.

## Rate Limiting

The Mercury API may have rate limits. The client will raise a `MercuryBankAPIError` if you exceed these limits. Implement appropriate retry logic in your application if needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Submit a pull request

## Support

For API-related questions, consult the [Mercury API documentation](https://docs.mercury.com/reference).

For client library issues, please open an issue in this repository.

## License

See LICENSE file for details.