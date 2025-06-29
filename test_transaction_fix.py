#!/usr/bin/env python3
"""
Test script to verify the transaction model fix for KeyError issues.
"""

from mercury_bank_api.models.transaction import Transaction, ElectronicRoutingInfo

def test_electronic_routing_info():
    """Test ElectronicRoutingInfo parsing with correct field name."""
    
    # Test data with the correct field name
    test_data = {
        "accountNumber": "123456789",
        "routingNumber": "987654321",
        "bankName": "Test Bank"
    }
    
    try:
        routing_info = ElectronicRoutingInfo.from_dict(test_data)
        print("✅ ElectronicRoutingInfo parsing successful")
        print(f"   Account Number: {routing_info.accountNumber}")
        print(f"   Routing Number: {routing_info.routingNumber}")
        print(f"   Bank Name: {routing_info.bankName}")
        
        # Test without optional bankName
        minimal_data = {
            "accountNumber": "123456789",
            "routingNumber": "987654321"
        }
        minimal_routing = ElectronicRoutingInfo.from_dict(minimal_data)
        print("✅ ElectronicRoutingInfo minimal parsing successful")
        print(f"   Bank Name (should be None): {minimal_routing.bankName}")
        
        return True
    except (KeyError, ValueError, TypeError) as e:
        print(f"❌ ElectronicRoutingInfo parsing failed: {e}")
        return False

def test_transaction_with_all_fields():
    """Test full transaction parsing with all possible fields."""
    
    transaction_data = {
        "amount": 100.50,
        "bankDescription": "Test transaction",
        "counterpartyId": "cp_123",
        "counterpartyName": "Test Counterparty",
        "counterpartyNickname": "Test Nick",
        "createdAt": "2025-06-29T10:00:00Z",
        "dashboardLink": "https://dashboard.mercury.com/transaction/123",
        "details": {
            "electronicRoutingInfo": {
                "accountNumber": "123456789",
                "routingNumber": "987654321",
                "bankName": "Test Bank"
            }
        },
        "estimatedDeliveryDate": "2025-06-30T10:00:00Z",
        "failedAt": None,
        "id": "txn_123",
        "kind": "externalTransfer",
        "note": "Test note",
        "externalMemo": "Test memo",
        "postedAt": "2025-06-29T11:00:00Z",
        "reasonForFailure": None,
        "status": "sent",
        "feeId": None,
        "currencyExchangeInfo": {
            "convertedFromCurrency": "USD",
            "convertedToCurrency": "EUR",
            "convertedFromAmount": 100.0,
            "convertedToAmount": 85.0,
            "feeAmount": 2.5,
            "feePercentage": 2.5,
            "exchangeRate": 0.85,
            "feeTransactionId": "fee_123"
        },
        "compliantWithReceiptPolicy": True,
        "hasGeneratedReceipt": False,
        "creditAccountPeriodId": None,
        "mercuryCategory": "transfer",
        "generalLedgerCodeName": "Transfers",
        "attachments": [
            {
                "fileName": "receipt.pdf",
                "url": "https://example.com/receipt.pdf",
                "attachmentType": "receipt"
            }
        ]
    }
    
    try:
        transaction = Transaction.from_dict(transaction_data)
        print("✅ Full transaction parsing successful")
        print(f"   Transaction ID: {transaction.id}")
        print(f"   Amount: ${transaction.amount}")
        print(f"   Electronic Routing Number: {transaction.details.electronicRoutingInfo.routingNumber}")
        print(f"   Currency Exchange Rate: {transaction.currencyExchangeInfo.exchangeRate}")
        print(f"   Attachments: {len(transaction.attachments)}")
        return True
    except (KeyError, ValueError, TypeError) as e:
        print(f"❌ Full transaction parsing failed: {e}")
        return False

def test_minimal_transaction():
    """Test transaction parsing with only required fields."""
    
    minimal_data = {
        "amount": 50.0,
        "counterpartyId": "cp_456",
        "counterpartyName": "Minimal Counterparty", 
        "createdAt": "2025-06-29T12:00:00Z",
        "dashboardLink": "https://dashboard.mercury.com/transaction/456",
        "estimatedDeliveryDate": "2025-06-30T12:00:00Z",
        "id": "txn_456",
        "kind": "internalTransfer",
        "status": "pending",
        "attachments": []
    }
    
    try:
        transaction = Transaction.from_dict(minimal_data)
        print("✅ Minimal transaction parsing successful")
        print(f"   Transaction ID: {transaction.id}")
        print(f"   Amount: ${transaction.amount}")
        print(f"   Details (should be None): {transaction.details}")
        print(f"   Bank Description (should be None): {transaction.bankDescription}")
        return True
    except (KeyError, ValueError, TypeError) as e:
        print(f"❌ Minimal transaction parsing failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing transaction model fixes...\n")
    
    success1 = test_electronic_routing_info()
    print()
    success2 = test_transaction_with_all_fields()
    print()
    success3 = test_minimal_transaction()
    
    if success1 and success2 and success3:
        print("\n🎉 All tests passed! The transaction model is working correctly.")
        print("The KeyError 'routingnumber' issue has been fixed.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
