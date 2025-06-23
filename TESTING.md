# 🧪 Testing Guide for EPT-MX-ADM

This document describes the testing infrastructure and how to run tests for EPT-MX-ADM.

## 📋 Testing Stack

- **pytest** - Main testing framework
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Enhanced mocking capabilities
- **unittest.mock** - Python standard mocking
- **GitHub Actions** - CI/CD pipeline

## 🚀 Quick Start

### Install Testing Dependencies

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Or install specific testing packages
pip install pytest pytest-cov pytest-mock
```

### Run Tests

```bash
# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only

# Run with coverage
make test-coverage

# Run all CI checks locally
make ci
```

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_simple.py       # Basic functionality tests
│   ├── test_utils.py        # Utility function tests
│   └── test_modules.py      # Module tests
└── integration/             # Integration tests
    └── test_routes.py       # Route/endpoint tests
```

## 🔧 Configuration Files

- **pytest.ini** - Pytest configuration
- **pyproject.toml** - Black, isort, mypy, coverage config
- **.flake8** - Linting configuration
- **Makefile** - Development commands

## 📊 Current Test Status

### ✅ Working Tests (12/30)

- **Basic functionality tests** - Python version, project structure, imports
- **Math operations** - Simple arithmetic tests
- **String operations** - String manipulation tests
- **Translation tests** - I18n functionality (partial)

### ❌ Known Issues

1. **Flask app factory** - `create_app()` signature mismatch
2. **Module imports** - Some modules don't have expected classes
3. **Flask context** - Request context needed for session tests
4. **API mocking** - Need to match actual API structure

## 🎯 Test Coverage

Current coverage: **24%**

Coverage report available in:
- Terminal: `make test-coverage`
- HTML: Open `htmlcov/index.html` after running tests

## 🔄 Continuous Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

1. **Testing** - Python 3.10, 3.11, 3.12
2. **Linting** - flake8 code quality checks
3. **Formatting** - black and isort checks
4. **Type checking** - mypy static analysis
5. **Security** - bandit security scan
6. **Coverage** - codecov.io integration
7. **Build** - Deployment package creation

## 📝 Writing Tests

### Unit Test Example

```python
class TestUserManager:
    """User management module tests"""
    
    def test_user_validation(self):
        """Test user validation logic"""
        # Arrange
        user_data = {"username": "test", "email": "test@example.com"}
        
        # Act
        result = validate_user(user_data)
        
        # Assert
        assert result is True
```

### Integration Test Example

```python
class TestUserRoutes:
    """User routes integration tests"""
    
    def test_users_page_requires_auth(self, client):
        """Test authentication requirement"""
        response = client.get('/users')
        assert response.status_code == 302
        assert 'login' in response.location
```

## 🛠️ Development Commands

```bash
# Setup development environment
make install-dev

# Run linting
make lint

# Format code
make format

# Type checking
make type-check

# Security scan
make security

# Clean temporary files
make clean

# Setup git hooks
make setup-git-hooks
```

## 🎨 Code Quality Tools

### Linting (flake8)
- Max line length: 127
- Excludes: vendor files, migrations
- Custom rules for imports

### Formatting (black + isort)
- Line length: 127
- Python 3.10+ target
- Automatic import sorting

### Type Checking (mypy)
- Gradual typing adoption
- Ignore missing imports
- Legacy code support

### Security (bandit)
- Automated security scanning
- JSON report generation
- CI integration

## 🚧 Roadmap

### Short Term
- [ ] Fix Flask app factory for integration tests
- [ ] Add proper module mocking
- [ ] Implement request context for session tests
- [ ] Increase test coverage to 50%

### Medium Term
- [ ] Add API endpoint tests
- [ ] Database operation tests
- [ ] Performance tests
- [ ] End-to-end tests with Selenium

### Long Term
- [ ] Mutation testing
- [ ] Property-based testing
- [ ] Load testing
- [ ] Visual regression testing

## 📞 Help & Support

- Check existing tests for examples
- Review pytest documentation
- Use `make help` for available commands
- CI logs available in GitHub Actions

## 🏆 Best Practices

1. **Test naming** - Descriptive test method names
2. **AAA pattern** - Arrange, Act, Assert
3. **One assertion per test** - Clear failure messages
4. **Mock external dependencies** - Isolated tests
5. **Test edge cases** - Error conditions and boundaries
6. **Documentation** - Docstrings for test classes/methods 