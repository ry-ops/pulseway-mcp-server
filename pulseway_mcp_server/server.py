"""
Pulseway PSA MCP Server

This MCP server provides tools to interact with the Pulseway PSA API,
allowing Claude to manage tickets, invoices, opportunities, time logs, and more.
"""

import os
import asyncio
from typing import Any, Optional
from dotenv import load_dotenv
import httpx
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

# Load environment variables
load_dotenv("secrets.env")


class PulsewayClient:
    """Client for interacting with Pulseway PSA API"""

    def __init__(
        self,
        gateway_url: str,
        username: str,
        password: str,
        company_name: str,
    ):
        self.gateway_url = gateway_url.rstrip("/")
        self.username = username
        self.password = password
        self.company_name = company_name
        self.base_url = f"{self.gateway_url}/api/v2"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Pulseway API"""
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
        }

        auth = httpx.BasicAuth(
            username=f"{self.company_name}\\{self.username}",
            password=self.password,
        )

        response = await self.client.request(
            method=method,
            url=url,
            headers=headers,
            auth=auth,
            params=params,
            json=json,
        )

        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    # Ticket Operations
    async def list_tickets(
        self,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, Any]:
        """List tickets with optional filters"""
        params = {"page": page, "pageSize": page_size}
        if status:
            params["status"] = status
        if assignee:
            params["assignee"] = assignee

        return await self._request("GET", "/servicedesk/tickets", params=params)

    async def get_ticket(self, ticket_id: int) -> dict[str, Any]:
        """Get details of a specific ticket"""
        return await self._request("GET", f"/servicedesk/tickets/{ticket_id}")

    async def create_ticket(
        self,
        title: str,
        description: str,
        account_id: int,
        priority: Optional[str] = None,
        issue_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new ticket"""
        data = {
            "title": title,
            "description": description,
            "accountId": account_id,
        }
        if priority:
            data["priority"] = priority
        if issue_type:
            data["issueType"] = issue_type

        return await self._request("POST", "/servicedesk/tickets", json=data)

    async def update_ticket(
        self, ticket_id: int, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing ticket"""
        return await self._request("PUT", f"/servicedesk/tickets/{ticket_id}", json=updates)

    # Invoice Operations
    async def list_invoices(
        self, page: int = 1, page_size: int = 50
    ) -> dict[str, Any]:
        """List all invoices"""
        params = {"page": page, "pageSize": page_size}
        return await self._request("GET", "/finance/invoices/summary", params=params)

    async def get_invoice(self, invoice_id: int) -> dict[str, Any]:
        """Get details of a specific invoice"""
        return await self._request("GET", f"/finance/invoices/{invoice_id}")

    # Opportunity Operations
    async def list_opportunities(
        self, page: int = 1, page_size: int = 50
    ) -> dict[str, Any]:
        """List all opportunities"""
        params = {"page": page, "pageSize": page_size}
        return await self._request("GET", "/crm/opportunities", params=params)

    async def get_opportunity(self, opportunity_id: int) -> dict[str, Any]:
        """Get details of a specific opportunity"""
        return await self._request("GET", f"/crm/opportunities/summary/{opportunity_id}")

    async def create_opportunity(
        self,
        title: str,
        account_id: int,
        estimated_value: Optional[float] = None,
        probability: Optional[int] = None,
    ) -> dict[str, Any]:
        """Create a new opportunity"""
        data = {
            "title": title,
            "accountId": account_id,
        }
        if estimated_value is not None:
            data["estimatedValue"] = estimated_value
        if probability is not None:
            data["probability"] = probability

        return await self._request("POST", "/crm/opportunities", json=data)

    # Time Log Operations
    async def list_timelogs(
        self, page: int = 1, page_size: int = 50
    ) -> dict[str, Any]:
        """List all time logs"""
        params = {"page": page, "pageSize": page_size}
        return await self._request("GET", "/time/timelogs", params=params)

    # Account Operations
    async def list_accounts(
        self, page: int = 1, page_size: int = 50
    ) -> dict[str, Any]:
        """List all accounts"""
        params = {"page": page, "pageSize": page_size}
        return await self._request("GET", "/crm/accounts", params=params)

    async def get_account(self, account_id: int) -> dict[str, Any]:
        """Get details of a specific account"""
        return await self._request("GET", f"/crm/accounts/{account_id}")


# Initialize the MCP server
app = Server("pulseway-mcp-server")

# Initialize Pulseway client
pulseway_client: Optional[PulsewayClient] = None


def get_client() -> PulsewayClient:
    """Get or create the Pulseway client"""
    global pulseway_client

    if pulseway_client is None:
        gateway_url = os.getenv("PULSEWAY_GATEWAY_URL")
        username = os.getenv("PULSEWAY_USERNAME")
        password = os.getenv("PULSEWAY_PASSWORD")
        company_name = os.getenv("PULSEWAY_COMPANY_NAME")

        if not all([gateway_url, username, password, company_name]):
            raise ValueError(
                "Missing required environment variables. Please check secrets.env file."
            )

        pulseway_client = PulsewayClient(
            gateway_url=gateway_url,
            username=username,
            password=password,
            company_name=company_name,
        )

    return pulseway_client


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Pulseway PSA tools"""
    return [
        Tool(
            name="list_tickets",
            description="List tickets from Pulseway PSA with optional filters for status and assignee",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by ticket status (e.g., 'Open', 'In Progress', 'Resolved')",
                    },
                    "assignee": {
                        "type": "string",
                        "description": "Filter by assignee name",
                    },
                    "page": {
                        "type": "number",
                        "description": "Page number (default: 1)",
                    },
                    "page_size": {
                        "type": "number",
                        "description": "Number of results per page (default: 50)",
                    },
                },
            },
        ),
        Tool(
            name="get_ticket",
            description="Get detailed information about a specific ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "number",
                        "description": "The ID of the ticket to retrieve",
                    },
                },
                "required": ["ticket_id"],
            },
        ),
        Tool(
            name="create_ticket",
            description="Create a new ticket in Pulseway PSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Ticket title/subject",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed ticket description",
                    },
                    "account_id": {
                        "type": "number",
                        "description": "The account/company ID this ticket is for",
                    },
                    "priority": {
                        "type": "string",
                        "description": "Ticket priority (e.g., 'Low', 'Medium', 'High', 'Critical')",
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Type of issue",
                    },
                },
                "required": ["title", "description", "account_id"],
            },
        ),
        Tool(
            name="update_ticket",
            description="Update an existing ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "number",
                        "description": "The ID of the ticket to update",
                    },
                    "updates": {
                        "type": "object",
                        "description": "Object containing fields to update (e.g., {'status': 'Resolved', 'assignee': 'John Doe'})",
                    },
                },
                "required": ["ticket_id", "updates"],
            },
        ),
        Tool(
            name="list_invoices",
            description="List all invoices from Pulseway PSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "Page number (default: 1)",
                    },
                    "page_size": {
                        "type": "number",
                        "description": "Number of results per page (default: 50)",
                    },
                },
            },
        ),
        Tool(
            name="get_invoice",
            description="Get detailed information about a specific invoice",
            inputSchema={
                "type": "object",
                "properties": {
                    "invoice_id": {
                        "type": "number",
                        "description": "The ID of the invoice to retrieve",
                    },
                },
                "required": ["invoice_id"],
            },
        ),
        Tool(
            name="list_opportunities",
            description="List all CRM opportunities from Pulseway PSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "Page number (default: 1)",
                    },
                    "page_size": {
                        "type": "number",
                        "description": "Number of results per page (default: 50)",
                    },
                },
            },
        ),
        Tool(
            name="get_opportunity",
            description="Get detailed information about a specific opportunity",
            inputSchema={
                "type": "object",
                "properties": {
                    "opportunity_id": {
                        "type": "number",
                        "description": "The ID of the opportunity to retrieve",
                    },
                },
                "required": ["opportunity_id"],
            },
        ),
        Tool(
            name="create_opportunity",
            description="Create a new CRM opportunity",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Opportunity title",
                    },
                    "account_id": {
                        "type": "number",
                        "description": "The account/company ID this opportunity is for",
                    },
                    "estimated_value": {
                        "type": "number",
                        "description": "Estimated value of the opportunity",
                    },
                    "probability": {
                        "type": "number",
                        "description": "Probability of closing (0-100)",
                    },
                },
                "required": ["title", "account_id"],
            },
        ),
        Tool(
            name="list_timelogs",
            description="List all time logs from Pulseway PSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "Page number (default: 1)",
                    },
                    "page_size": {
                        "type": "number",
                        "description": "Number of results per page (default: 50)",
                    },
                },
            },
        ),
        Tool(
            name="list_accounts",
            description="List all accounts/companies from Pulseway PSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "Page number (default: 1)",
                    },
                    "page_size": {
                        "type": "number",
                        "description": "Number of results per page (default: 50)",
                    },
                },
            },
        ),
        Tool(
            name="get_account",
            description="Get detailed information about a specific account/company",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "number",
                        "description": "The ID of the account to retrieve",
                    },
                },
                "required": ["account_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for Pulseway PSA operations"""
    try:
        client = get_client()

        if name == "list_tickets":
            result = await client.list_tickets(
                status=arguments.get("status"),
                assignee=arguments.get("assignee"),
                page=arguments.get("page", 1),
                page_size=arguments.get("page_size", 50),
            )
        elif name == "get_ticket":
            result = await client.get_ticket(arguments["ticket_id"])
        elif name == "create_ticket":
            result = await client.create_ticket(
                title=arguments["title"],
                description=arguments["description"],
                account_id=arguments["account_id"],
                priority=arguments.get("priority"),
                issue_type=arguments.get("issue_type"),
            )
        elif name == "update_ticket":
            result = await client.update_ticket(
                ticket_id=arguments["ticket_id"],
                updates=arguments["updates"],
            )
        elif name == "list_invoices":
            result = await client.list_invoices(
                page=arguments.get("page", 1),
                page_size=arguments.get("page_size", 50),
            )
        elif name == "get_invoice":
            result = await client.get_invoice(arguments["invoice_id"])
        elif name == "list_opportunities":
            result = await client.list_opportunities(
                page=arguments.get("page", 1),
                page_size=arguments.get("page_size", 50),
            )
        elif name == "get_opportunity":
            result = await client.get_opportunity(arguments["opportunity_id"])
        elif name == "create_opportunity":
            result = await client.create_opportunity(
                title=arguments["title"],
                account_id=arguments["account_id"],
                estimated_value=arguments.get("estimated_value"),
                probability=arguments.get("probability"),
            )
        elif name == "list_timelogs":
            result = await client.list_timelogs(
                page=arguments.get("page", 1),
                page_size=arguments.get("page_size", 50),
            )
        elif name == "list_accounts":
            result = await client.list_accounts(
                page=arguments.get("page", 1),
                page_size=arguments.get("page_size", 50),
            )
        elif name == "get_account":
            result = await client.get_account(arguments["account_id"])
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        import json
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2),
            )
        ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
