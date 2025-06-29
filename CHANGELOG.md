# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-28

### Added
- Initial release of Mercury Bank API Python client
- Complete API coverage for Mercury Bank's transaction and account endpoints
- Type-safe data models for all API responses
- Comprehensive error handling with custom exception types
- Built-in parsing for complex transaction details and routing information
- Full documentation and usage examples
- PyPI package configuration

### Features
- `MercuryBankAPIClient` - Main API client class
- `Account` model - Bank account information
- `Transaction` model - Transaction data with full details
- `TransactionResponse` model - API response wrapper
- Custom error handling with `MercuryBankAPIError`
- Support for Python 3.7+

### Dependencies
- requests >= 2.25.0
- python-dateutil >= 2.8.0  
- typing-extensions >= 4.0.0
