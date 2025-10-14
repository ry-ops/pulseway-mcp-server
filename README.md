<img src="https://github.com/ry-ops/pulseway-mcp-server/blob/main/pulseway_mcp_server.png" width="100%">

# Pulseway MCP Server

A Model Context Protocol (MCP) server that integrates Claude AI with the Pulseway PSA (Professional Services Automation) API. This server enables Claude to interact with your Pulseway PSA instance to manage tickets, invoices, opportunities, time logs, and more.

## Features

This MCP server provides the following capabilities:

### Service Desk
- **List Tickets** - View all tickets with optional filtering by status and assignee
- **Get Ticket Details** - Retrieve detailed information about specific tickets
- **Create Tickets** - Create new support tickets
- **Update Tickets** - Modify existing tickets (status, assignee, priority, etc.)

### Finance
- **List Invoices** - View all invoices
- **Get Invoice Details** - Retrieve detailed information about specific invoices

### CRM
- **List Opportunities** - View all sales opportunities
- **Get Opportunity Details** - Retrieve detailed information about specific opportunities
- **Create Opportunities** - Create new sales opportunities
- **List Accounts** - View all customer accounts/companies
- **Get Account Details** - Retrieve detailed information about specific accounts

### Time Tracking
- **List Time Logs** - View all time log entries

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- A Pulseway PSA account with API access
- Claude Desktop or another MCP client

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/pulseway-mcp-server.git
   cd pulseway-mcp-server
   ```

2. **Install dependencies using uv:**
   ```bash
   uv pip install -e .
   ```

3. **Configure your credentials:**
   ```bash
   cp secrets.env.example secrets.env
   ```

4. **Edit `secrets.env` with your Pulseway credentials:**
   ```env
   PULSEWAY_GATEWAY_URL=https://psa.pulseway.com
   PULSEWAY_USERNAME=your_username
   PULSEWAY_PASSWORD=your_password
   PULSEWAY_COMPANY_NAME=your_company_name
   ```

   To find these values:
   - **Gateway URL**: Your Pulseway PSA server URL (e.g., `https://psa.pulseway.com`)
   - **Username**: Your Pulseway PSA username
   - **Password**: Your Pulseway PSA password
   - **Company Name**: Your tenant/company name in Pulseway PSA
   
   You can find your Gateway URL and Company Name by navigating to **My Settings** in Pulseway PSA (click your name in the top navigation bar).

## Configuration with Claude Desktop

Add this server to your Claude Desktop configuration file:

### macOS
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Edit: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

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

Replace `/absolute/path/to/pulseway-mcp-server` with the actual path to your installation.

## Usage

Once configured, Claude will have access to Pulseway PSA tools. You can ask Claude to:

- "List all open tickets in Pulseway"
- "Show me ticket #12345"
- "Create a new ticket for ACME Corp about email issues"
- "Update ticket #12345 to mark it as resolved"
- "List all invoices from this month"
- "Show me all CRM opportunities"
- "Create a new opportunity for Company XYZ worth $50,000"
- "List all customer accounts"
- "Show me time logs from last week"

### Example Conversations

**Creating a Ticket:**
```
You: Create a new ticket for account ID 123 about a server outage. Title it "Critical Server Down" and mark it as high priority.

Claude: I'll create that ticket for you.
[Creates ticket using the create_ticket tool]
```

**Checking Ticket Status:**
```
You: What are all the open tickets assigned to John?

Claude: Let me check the open tickets for John.
[Uses list_tickets tool with status="Open" and assignee="John"]
```

## API Rate Limits

The Pulseway PSA API has a rate limit of **1500 requests per hour per endpoint**. The server does not implement rate limiting, so be mindful of the number of requests you make.

## Security

- **Never commit `secrets.env`** to version control. It contains sensitive credentials.
- Use an API-only user account in Pulseway PSA when possible (see [Dedicated API integration account](https://intercom.help/pulseway/en/articles/6813472-pulseway-psa-api-dedicated-api-integration-account-in-psa))
- Ensure proper file permissions on `secrets.env` (recommended: `chmod 600 secrets.env`)

## Development

### Running Tests

```bash
uv run pytest
```

### Project Structure

```
pulseway-mcp-server/
├── pulseway_mcp_server/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── pyproject.toml          # Project dependencies and configuration
├── secrets.env.example     # Example environment variables
├── .gitignore
└── README.md
```

## Troubleshooting

### Authentication Errors

If you receive authentication errors:
1. Verify your credentials in `secrets.env`
2. Ensure your company name is correct (case-sensitive)
3. Check that your Gateway URL includes the protocol (https://)
4. Verify your user has API access enabled in Pulseway PSA

### Connection Errors

If the server can't connect:
1. Verify your Gateway URL is accessible
2. Check your network connection
3. Ensure you're not behind a firewall blocking the API

### Missing Environment Variables

If you see "Missing required environment variables":
1. Ensure `secrets.env` exists in the project root
2. Verify all required variables are set in `secrets.env`
3. Check that variable names match exactly

## API Documentation

For more information about the Pulseway PSA API, see:
- [PSA REST APIs V2 Documentation](https://intercom.help/pulseway/en/articles/6072337-psa-rest-apis-v2)
- [API Guide](https://api.psa.pulseway.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [https://github.com/yourusername/pulseway-mcp-server/issues](https://github.com/yourusername/pulseway-mcp-server/issues)
- Pulseway Support: [https://support.pulseway.com](https://support.pulseway.com)

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io)
- Powered by [Pulseway PSA](https://www.pulseway.com)
