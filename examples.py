"""
Example usage of the Mercury Bank API client.

This module demonstrates how to use the Mercury Bank API client to interact 
with the Mercury banking API.
"""

import os
from datetime import datetime, timedelta
from mercury_client import MercuryBankAPIClient, MercuryBankAPIError


def main():
    """Main example function."""
    
    # Get API token from environment variable
    api_token = os.getenv("MERCURY_API_TOKEN")
    if not api_token:
        print("Please set the MERCURY_API_TOKEN environment variable")
        return
    
    # Initialize the client
    client = MercuryBankAPIClient(api_token=api_token)
    
    try:
        # Example 1: Get all accounts
        print("Fetching accounts...")
        accounts = client.get_accounts()
        print(f"Found {len(accounts)} accounts:")
        
        for account in accounts:
            print(f"  - {account.name} ({account.id})")
            print(f"    Balance: ${account.currentBalance:.2f}")
            print(f"    Available: ${account.availableBalance:.2f}")
            print(f"    Status: {account.status}")
            print()
        
        if not accounts:
            print("No accounts found.")
            return
        
        # Example 2: Get transactions for the first account
        first_account = accounts[0]
        print(f"Fetching transactions for account: {first_account.name}")
        
        # Get recent transactions (last 30 days)
        end_date = datetime.now().isoformat()
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
        
        transaction_response = client.get_transactions(
            account_id=first_account.id,
            limit=10,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"Found {transaction_response.total} total transactions (showing first 10):")
        
        for transaction in transaction_response.transactions:
            print(f"  - {transaction.createdAt.strftime('%Y-%m-%d')}: "
                  f"${transaction.amount:.2f} - {transaction.counterpartyName}")
            print(f"    Status: {transaction.status}, Kind: {transaction.kind}")
            if transaction.note:
                print(f"    Note: {transaction.note}")
            print()
        
        # Example 3: Filter transactions by status
        print("Fetching only pending transactions...")
        pending_transactions = client.get_transactions(
            account_id=first_account.id,
            status="pending",
            limit=5
        )
        
        if pending_transactions.transactions:
            print(f"Found {len(pending_transactions.transactions)} pending transactions:")
            for transaction in pending_transactions.transactions:
                print(f"  - ${transaction.amount:.2f} to {transaction.counterpartyName}")
        else:
            print("No pending transactions found.")
        
        # Example 4: Get a specific transaction by ID
        if transaction_response.transactions:
            first_transaction = transaction_response.transactions[0]
            print(f"\nFetching specific transaction: {first_transaction.id}")
            
            specific_transaction = client.get_transaction_by_id(
                account_id=first_account.id,
                transaction_id=first_transaction.id
            )
            
            if specific_transaction:
                print(f"Transaction details:")
                print(f"  Amount: ${specific_transaction.amount:.2f}")
                print(f"  Counterparty: {specific_transaction.counterpartyName}")
                print(f"  Status: {specific_transaction.status}")
                print(f"  Created: {specific_transaction.createdAt}")
                print(f"  Dashboard Link: {specific_transaction.dashboardLink}")
                
                if specific_transaction.attachments:
                    print(f"  Attachments: {len(specific_transaction.attachments)}")
                    for attachment in specific_transaction.attachments:
                        print(f"    - {attachment.fileName} ({attachment.attachmentType})")
        
    except MercuryBankAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
