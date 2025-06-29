#!/usr/bin/env python3
"""Simple test script to verify the package imports correctly and test basic functionality."""

import os


def test_imports():
    """Test that all imports work correctly."""
    try:
        from mercury_bank_api import MercuryBankAPIClient, MercuryBankAPIError
        from mercury_bank_api import Account, Transaction, TransactionResponse

        print("✅ All imports successful!")
        print(f"MercuryBankAPIClient: {MercuryBankAPIClient}")
        print(f"MercuryBankAPIError: {MercuryBankAPIError}")
        print(f"Account: {Account}")
        print(f"Transaction: {Transaction}")
        print(f"TransactionResponse: {TransactionResponse}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_client_initialization():
    """Test client initialization."""
    try:
        from mercury_bank_api import MercuryBankAPIClient

        # Test with dummy token
        client = MercuryBankAPIClient(api_token="test_token")
        print("✅ Client initialization successful!")
        print(f"Client base URL: {client.BASE_URL}")
        return True
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False


def test_api_connection():
    """Test actual API connection if token is available."""
    api_token = os.getenv("MERCURY_API_TOKEN")
    if not api_token:
        print("⚠️  No MERCURY_API_TOKEN environment variable found.")
        print(
            "   To test API connection, set your token: export MERCURY_API_TOKEN='your_token'"
        )
        return True

    try:
        from mercury_bank_api import MercuryBankAPIClient, MercuryBankAPIError

        client = MercuryBankAPIClient(api_token=api_token)
        accounts = client.get_accounts()
        print(f"✅ API connection successful! Found {len(accounts)} accounts.")
        return True
    except MercuryBankAPIError as e:
        print(f"❌ API connection failed: {e}")
        print("   Check your API token and permissions in the Mercury dashboard.")
        return False


if __name__ == "__main__":
    print("Testing Mercury Bank API Python Client...")
    print("=" * 50)

    success = True
    success &= test_imports()
    print()
    success &= test_client_initialization()
    print()
    success &= test_api_connection()
    print()

    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
        exit(1)
