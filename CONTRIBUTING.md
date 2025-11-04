# Contributing to Astrologer API

Thank you for your interest in contributing to Astrologer API! We welcome contributions from everyone, regardless of experience level.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check the existing [issues](https://github.com/your-username/astrologer-api/issues) to avoid duplicates
2. Create a new issue with a clear title and detailed description
3. Include steps to reproduce the bug
4. Specify your environment (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has already been suggested in the issues
2. Create a new issue with a clear title and detailed description
3. Explain why this feature would be useful
4. Describe the expected behavior

### Pull Requests

1. Fork the repository
2. Create a new branch with a descriptive name:
   - For features: `feature/descriptive-name`
   - For bug fixes: `fix/descriptive-name`
3. Make your changes following the code style
4. Add tests if applicable
5. Update documentation if needed
6. Ensure all tests pass
7. Submit a pull request with a clear description

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/astrologer-api.git
   cd astrologer-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pipenv
   pipenv install --dev
   ```

4. Set up environment variables:
   ```bash
   export GEONAMES_USERNAME="your_username"
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write clear, descriptive names for variables and functions
- Include docstrings for all public functions and classes
- Keep functions focused and small

## Testing

- Write tests for new functionality
- Run existing tests before submitting a pull request:
  ```bash
  pipenv run test
  ```

### Running Tests

```bash
pipenv run test  # Run all tests
pipenv run test-verbose  # Run tests with more detailed output
```

## Documentation

- Update documentation when adding new features
- Use clear and concise language
- Include examples where appropriate

## Questions?

If you have any questions, feel free to open an issue with the "question" label.