"""Tests for Pulseway MCP Server"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pulseway_mcp_server.server import PulsewayClient


@pytest.mark.asyncio
async def test_pulseway_client_initialization():
    """Test that PulsewayClient initializes correctly"""
    client = PulsewayClient(
        gateway_url="https://psa.pulseway.com",
        username="testuser",
        password="testpass",
        company_name="testcompany",
    )
    
    assert client.gateway_url == "https://psa.pulseway.com"
    assert client.username == "testuser"
    assert client.password == "testpass"
    assert client.company_name == "testcompany"
    assert client.base_url == "https://psa.pulseway.com/api/v2"
    
    await client.close()


@pytest.mark.asyncio
async def test_pulseway_client_strips_trailing_slash():
    """Test that trailing slash is stripped from gateway URL"""
    client = PulsewayClient(
        gateway_url="https://psa.pulseway.com/",
        username="testuser",
        password="testpass",
        company_name="testcompany",
    )
    
    assert client.gateway_url == "https://psa.pulseway.com"
    assert client.base_url == "https://psa.pulseway.com/api/v2"
    
    await client.close()


@pytest.mark.asyncio
async def test_list_tickets():
    """Test listing tickets"""
    client = PulsewayClient(
        gateway_url="https://psa.pulseway.com",
        username="testuser",
        password="testpass",
        company_name="testcompany",
    )
    
    # Mock the HTTP request
    mock_response = {"tickets": [{"id": 1, "title": "Test Ticket"}]}
    
    with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status = Mock()
        
        result = await client.list_tickets()
        
        assert result == mock_response
        mock_request.assert_called_once()
    
    await client.close()


@pytest.mark.asyncio
async def test_create_ticket():
    """Test creating a ticket"""
    client = PulsewayClient(
        gateway_url="https://psa.pulseway.com",
        username="testuser",
        password="testpass",
        company_name="testcompany",
    )
    
    mock_response = {"id": 123, "title": "New Ticket", "status": "Open"}
    
    with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status = Mock()
        
        result = await client.create_ticket(
            title="New Ticket",
            description="Test description",
            account_id=456,
            priority="High",
        )
        
        assert result == mock_response
        mock_request.assert_called_once()
        
        # Verify the request parameters
        call_args = mock_request.call_args
        assert call_args.kwargs['json']['title'] == "New Ticket"
        assert call_args.kwargs['json']['description'] == "Test description"
        assert call_args.kwargs['json']['accountId'] == 456
        assert call_args.kwargs['json']['priority'] == "High"
    
    await client.close()


def test_get_client_missing_env_vars():
    """Test that get_client raises error when environment variables are missing"""
    from pulseway_mcp_server.server import get_client
    
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="Missing required environment variables"):
            get_client()
