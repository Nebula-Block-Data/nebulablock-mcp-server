
import pytest
import json

from fastmcp.client import Client
from unittest import mock
from src.tools import mcp
from src.config import settings


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_computing_products(mock_get: mock.MagicMock) -> None:
    """
    Test that get_computing_products resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"products": ["product1", "product2"]}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://computing_products")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/products",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    assert json.loads(result[0].text) == {"products": ["product1", "product2"]}

@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_user_instances(mock_get: mock.MagicMock) -> None:
    """
    Test that get_user_instances resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": "123", "host_name": "test-instance"}]}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource without limit and offset
        result = await client.read_resource("mcp://user_instances")

    # Assertions for call without limit and offset
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instances",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params={}
    )
    assert json.loads(result[0].text) == {"data": [{"id": "123", "host_name": "test-instance"}]}

    # Reset mock for the next call
    mock_get.reset_mock()

    # Call the resource with limit and offset
    async with Client(mcp) as client:
        result_with_params = await client.read_resource("mcp://user_instances", limit=10, offset=5)

    # Assertions for call with limit and offset
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instances",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params={"limit": 10, "offset": 5}
    )
    assert json.loads(result_with_params[0].text) == {"data": [{"id": "123", "host_name": "test-instance"}]}