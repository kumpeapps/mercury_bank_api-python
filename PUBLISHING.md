# Publishing to PyPI

This guide explains how to publish the Mercury Bank API Python package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org/account/register/) and [TestPyPI](https://test.pypi.org/account/register/)
2. **API Tokens**: Generate API tokens for uploading packages
3. **Build Tools**: Ensure you have the necessary tools installed (already done):
   ```bash
   pip install --upgrade pip setuptools wheel build twine
   ```

## Step-by-Step Publishing Process

### 1. Update Package Metadata

Before publishing, update these fields in `pyproject.toml`:

- `authors`: Replace with your actual name and email
- `maintainers`: Replace with your actual name and email  
- `project.urls`: Update GitHub repository URLs

### 2. Choose Package Name

⚠️ **Important**: Before publishing, check if the package name `mercury-bank-api-python` is available on PyPI:
- Visit https://pypi.org/project/mercury-bank-api-python/
- If taken, choose a different name in `pyproject.toml`

### 3. Test on TestPyPI First

Always test on TestPyPI before publishing to the main PyPI:

```bash
# Build the package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ mercury-bank-api-python
```

### 4. Publish to PyPI

Once tested successfully:

```bash
# Upload to PyPI
python -m twine upload dist/*
```

### 5. Configure Authentication

For secure uploads, configure your `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-api-token-here
```

## Package Structure

The built package includes:
- `mercury_bank_api/` - Main package directory
- `mercury_bank_api/__init__.py` - Package initialization and exports
- `mercury_bank_api/mercury_client.py` - Main API client
- `mercury_bank_api/models/` - Data models (Account, Transaction, etc.)
- `README.md` - Documentation
- `LICENSE` - MIT license
- Metadata and dependencies

## Version Management

To release new versions:
1. Update version in `pyproject.toml`
2. Update version in `mercury_bank_api/__init__.py`
3. Clean previous builds: `rm -rf dist/ build/ *.egg-info/`
4. Build and upload new version

## Installation After Publishing

Once published, users can install with:

```bash
pip install mercury-bank-api-python
```

And use it with:

```python
from mercury_bank_api import MercuryBankAPIClient

client = MercuryBankAPIClient(api_token="your_token")
accounts = client.get_accounts()
```

## Troubleshooting

- **Permission Errors**: Ensure you have correct API tokens
- **Package Name Conflicts**: Choose a unique package name
- **Build Errors**: Check `pyproject.toml` syntax and package structure
- **Import Errors**: Verify package structure and `__init__.py` exports
