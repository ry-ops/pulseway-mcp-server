# Contributing to Pulseway MCP Server

Thank you for your interest in contributing to the Pulseway MCP Server! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Submit a pull request

## Development Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/pulseway-mcp-server.git
   cd pulseway-mcp-server
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Set up your environment:**
   ```bash
   cp secrets.env.example secrets.env
   # Edit secrets.env with your test credentials
   ```

## Making Changes

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Run tests with: `uv run pytest`

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

Example:
```
Add support for contract management

- Add list_contracts tool
- Add get_contract tool
- Update README with contract examples

Fixes #123
```

## Pull Request Process

1. **Update Documentation:** Ensure README.md and any relevant docs are updated
2. **Add Tests:** Include tests for new functionality
3. **Update CHANGELOG:** Add your changes to the unreleased section
4. **Ensure CI Passes:** All GitHub Actions checks must pass
5. **Request Review:** Tag maintainers for review

## Adding New API Endpoints

When adding support for new Pulseway PSA API endpoints:

1. **Add the method to PulsewayClient:**
   ```python
   async def new_operation(self, param: str) -> dict[str, Any]:
       """Description of the operation"""
       return await self._request("GET", "/endpoint", params={"param": param})
   ```

2. **Add the tool definition to list_tools():**
   ```python
   Tool(
       name="new_operation",
       description="Clear description of what this does",
       inputSchema={
           "type": "object",
           "properties": {
               "param": {
                   "type": "string",
                   "description": "Parameter description",
               },
           },
           "required": ["param"],
       },
   ),
   ```

3. **Add the handler to call_tool():**
   ```python
   elif name == "new_operation":
       result = await client.new_operation(arguments["param"])
   ```

4. **Add tests:**
   ```python
   @pytest.mark.asyncio
   async def test_new_operation():
       # Test implementation
       pass
   ```

5. **Update README.md** with the new feature

## Testing with Real API

When testing with the real Pulseway API:
- Use a dedicated test account
- Be mindful of rate limits (1500 requests/hour per endpoint)
- Clean up any test data you create
- Never commit real credentials

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about contributing
- General discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
