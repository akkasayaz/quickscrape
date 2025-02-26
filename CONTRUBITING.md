# Contributing to QuickScrape

This document provides guidelines and instructions for contributing to this project.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots
- Your environment (Python version and pip freeze result)

### Suggesting Features

Have an idea for a new feature? Please create an issue with:

- A clear, descriptive title
- Detailed description of the proposed feature
- Any relevant examples or use cases
- Explanation of why this feature would be useful (Doesn't have to be long)

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add or update tests as needed
5. Run tests to ensure they pass
6. Update documentation if necessary
7. Commit your changes with clear commit messages
8. Push to your branch (`git push origin feature/your-feature-name`)
9. Open a pull request

## Development Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/quickscrape.git
   cd quickscrape
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   pip install pytest
   ```
3. Run tests to ensure everything is working:

   ```bash
   pytest
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines (as much as you can)
- Write docstrings for all functions, classes, and modules
- Include type hints where possible
- Keep functions focused and small
- Add comments for complex logic

## Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting pull requests
- Aim for good test coverage

## Documentation

- Update the README.md if necessary
- Add docstrings to all public functions and classes
- Include usage examples for new features

## Branching Strategy

- `main` branch is protected and represents the latest stable release
- Development happens on feature branches
- Create feature branches from `dev` named like `feature/your-feature`
- Create bugfix branches named like `fix/issue-description`
- Create documentation branches named like `documentation/whatever-you-are-enhancing`

## Release Process

The maintainers will handle the release process, including:

1. Version bumping
2. PyPI releases

## Questions?

If you have any questions about contributing, please open an issue labeled "question".

Thank you for helping improve QuickScrape!
