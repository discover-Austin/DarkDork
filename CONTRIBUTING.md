# Contributing to DarkDork

Thank you for your interest in contributing to DarkDork! This document provides guidelines for contributing to the project.

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive criticism
- Use welcoming and professional language
- Respect differing viewpoints and experiences
- Accept responsibility for mistakes
- Remember this is a security tool - ethical use is paramount

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Use a clear and descriptive title
- Provide detailed explanation of the proposed feature
- Explain why this enhancement would be useful
- List any potential drawbacks or considerations

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Write clear commit messages**
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Follow the coding style** used in the project
6. **Include comments** for complex logic

#### Pull Request Checklist

- [ ] Code follows the project style
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated if applicable
- [ ] All tests pass

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/darkdork.git
cd darkdork

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specifics:
- **Indentation**: 4 spaces
- **Line length**: 100 characters maximum
- **Imports**: Group stdlib, third-party, and local imports
- **Docstrings**: Use for all public methods and classes
- **Type hints**: Use where beneficial

### Example Code Style

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    # Implementation
    return True
```

## Security Considerations

When contributing, keep in mind:
- **Never include credentials** or sensitive data
- **Validate all user input**
- **Avoid command injection vulnerabilities**
- **Follow secure coding practices**
- **Consider rate limiting** for network operations
- **Respect privacy** of users and targets

## Adding New Dork Categories

When adding new dork categories:

1. Add to `DorkCategory.CATEGORIES` dictionary
2. Use clear, descriptive category name
3. Include relevant, ethical dorks only
4. Test all dorks before submission
5. Document the purpose of the category

Example:
```python
"Category Name": [
    'dork query 1',
    'dork query 2',
    # More dorks...
]
```

## Testing

Before submitting:
```bash
# Run the application
python darkdork.py

# Test different features:
# - Category selection
# - Custom dork building
# - Export functionality
# - Settings configuration
```

## Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Fixing bugs that affect user behavior
- Adding configuration options

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

Contributors will be recognized in the project's README and release notes.

---

Thank you for making DarkDork better!
