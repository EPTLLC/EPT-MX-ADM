# Contributing to EPT-MX-ADM

Thank you for your interest in contributing to EPT-MX-ADM! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM
```

2. **Install dependencies**
```bash
pip install -r requirements-dev.txt
```

3. **Run tests**
```bash
make test
```

## Code Standards

- **Python 3.10+** required
- **Line length**: 127 characters max
- **Testing**: All new features must include tests
- **Documentation**: Update README.md for user-facing changes

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Make** your changes with tests
4. **Run** the test suite: `make ci`
5. **Commit** with clear messages
6. **Push** and create a Pull Request

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run linting
make lint

# Run all CI checks
make ci
```

## Code Quality

We use automated tools for code quality:
- **flake8** for linting
- **black** for formatting
- **isort** for import sorting
- **mypy** for type checking
- **bandit** for security scanning

## Reporting Issues

When reporting bugs, please include:
- **Python version**
- **Operating system**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error messages/logs**

## Feature Requests

For new features:
- **Check existing issues** first
- **Describe the use case**
- **Explain the expected behavior**
- **Consider backward compatibility**

## License

By contributing, you agree that your contributions will be licensed under the MIT License.