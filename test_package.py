#!/usr/bin/env python3
"""
Test script to verify the mercury-bank-api-python package works correctly.
"""

try:
    # Test imports
    from mercury_bank_api import MercuryBankAPIClient, MercuryBankAPIError
    from mercury_bank_api import Account, Transaction, TransactionResponse
    print("✅ All imports successful")
    
    # Test basic instantiation
    client = MercuryBankAPIClient(api_token="test_token")
    print("✅ Client instantiation successful")
    
    # Test that the client has expected methods
    expected_methods = ['get_accounts', 'get_transactions', 'get_transaction']
    for method in expected_methods:
        if hasattr(client, method):
            print(f"✅ Method {method} exists")
        else:
            print(f"❌ Method {method} missing")
    
    print("\n🎉 Package verification complete!")
    print("Your Mercury Bank API Python package is ready for PyPI!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
