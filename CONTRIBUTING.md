# Contributing to OrganiserPro

Thank you for your interest in contributing to OrganiserPro! We welcome contributions from the community.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/the-solution-desk/OrganiserPro.git
   cd OrganiserPro
   ```

2. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.in
   pip install -e .
   ```

3. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep lines under 88 characters
- Remove trailing whitespace

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Test on multiple Linux distributions when possible

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Reporting Issues

When reporting issues, please include:
- Your Linux distribution and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Any error messages or logs

## Code of Conduct

Please be respectful and inclusive in all interactions. We want OrganiserPro to be welcoming to contributors from all backgrounds.

## Questions?

Feel free to open an issue for questions about contributing!
