# Quick Start Guide

Get up and running with Pulseway MCP Server in 5 minutes!

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed
- Pulseway PSA account

## Installation Steps

### 1. Install uv (if needed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
git clone https://github.com/yourusername/pulseway-mcp-server.git
cd pulseway-mcp-server
uv pip install -e .
```

### 3. Configure Credentials

```bash
cp secrets.env.example secrets.env
```

Edit `secrets.env`:
```env
PULSEWAY_GATEWAY_URL=https://psa.pulseway.com
PULSEWAY_USERNAME=your_username
PULSEWAY_PASSWORD=your_password
PULSEWAY_COMPANY_NAME=your_company_name
```

### 4. Add to Claude Desktop

**macOS:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** Edit `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pulseway": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/pulseway-mcp-server",
        "pulseway-mcp"
      ]
    }
  }
}
```

### 5. Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

## Test It Out

Try these commands in Claude:

- "List all open tickets in Pulseway"
- "Show me all customer accounts"
- "Create a test ticket for account 123"
- "List recent invoices"

## Troubleshooting

**Authentication Error?**
- Double-check credentials in `secrets.env`
- Verify your Gateway URL includes `https://`
- Ensure company name is correct (case-sensitive)

**Connection Error?**
- Check network connection
- Verify Gateway URL is accessible
- Check for firewall issues

**MCP Server Not Loading?**
- Verify absolute path in config is correct
- Check that `secrets.env` exists with valid credentials
- Look at Claude Desktop logs for errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- See [API Documentation](https://intercom.help/pulseway/en/articles/6072337-psa-rest-apis-v2) for more endpoint details

## Support

- GitHub Issues: [Report a bug or request a feature](https://github.com/yourusername/pulseway-mcp-server/issues)
- Pulseway Support: [https://support.pulseway.com](https://support.pulseway.com)
