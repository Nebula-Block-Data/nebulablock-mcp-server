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
        },
        params=None
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

@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_computing_products_api_error(mock_get: mock.MagicMock) -> None:
    """
    Test get_computing_products when the API returns an error (e.g., 500).
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = Exception("Internal Server Error")
    mock_get.return_value = mock_response

    async with Client(mcp) as client:
        with pytest.raises(Exception) as excinfo:
            await client.read_resource("mcp://computing_products")
    assert "Internal Server Error" in str(excinfo.value)

@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_user_instances_api_unauthorized(mock_get: mock.MagicMock) -> None:
    """
    Test get_user_instances when the API returns a 401 Unauthorized error.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = Exception("Unauthorized")
    mock_get.return_value = mock_response

    async with Client(mcp) as client:
        with pytest.raises(Exception) as excinfo:
            await client.read_resource("mcp://user_instances?limit=10&offset=0")
    assert "Unauthorized" in str(excinfo.value)

@pytest.mark.asyncio
async def test_get_user_instances_missing_params():
    """
    Test get_user_instances with incorrect parameter type (limit is string instead of int).
    """
    async with Client(mcp) as client:
        with pytest.raises(Exception):
            await client.read_resource("mcp://user_instances?limit=abc&offset=None")

@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_user_instances_invalid_limit(mock_get: mock.MagicMock) -> None:
    """
    Test get_user_instances with a negative limit (abnormal input data).
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = Exception("Invalid limit")
    mock_get.return_value = mock_response

    async with Client(mcp) as client:
        with pytest.raises(Exception) as excinfo:
            await client.read_resource("mcp://user_instances?limit=-5&offset=0")
    assert "Invalid limit" in str(excinfo.value)


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_user_instance_detail(mock_get: mock.MagicMock) -> None:
    """
    Test that get_user_instance_detail resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123", "host_name": "test-instance"}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://user_instance_detail/123")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance/123",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == {"id": "123", "host_name": "test-instance"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_list_deleted_user_instances(mock_get: mock.MagicMock) -> None:
    """
    Test that list_deleted_user_instances resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "host_name": "test-instance"}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://deleted_user_instances")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/deleted-instances",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == [{"id": "123", "host_name": "test-instance"}]


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_user_credit_balance(mock_get: mock.MagicMock) -> None:
    """
    Test that get_user_credit_balance resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"credit": 100}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://billing_user_credit_balance")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/users/credits",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == {"credit": 100}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_list_user_invoices(mock_get: mock.MagicMock) -> None:
    """
    Test that list_user_invoices resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "amount": 100}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://billing_user_invoices?limit=10&offset=0")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/users/invoices",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params={"limit": 10, "offset": 0} 
    )
    assert json.loads(result[0].text) == [{"id": "123", "amount": 100}]


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_list_api_keys(mock_get: mock.MagicMock) -> None:
    """
    Test that list_api_keys resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "name": "test-key"}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://api_keys")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/api_keys",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == [{"id": "123", "name": "test-key"}]


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_list_ssh_keys(mock_get: mock.MagicMock) -> None:
    """
    Test that list_ssh_keys resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "name": "test-key"}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://ssh_keys")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/ssh-keys",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == [{"id": "123", "name": "test-key"}]


@pytest.mark.asyncio
@mock.patch("requests.delete")
async def test_delete_gpu_instance(mock_delete: mock.MagicMock) -> None:
    """
    Test that delete_gpu_instance tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Instance deleted successfully"}
    mock_delete.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool("delete_gpu_instance", {"id": "123"})

    # Assertions
    mock_delete.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance/123",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    assert json.loads(result[0].text) == {"message": "Instance deleted successfully"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_start_gpu_instance(mock_get: mock.MagicMock) -> None:
    """
    Test that start_gpu_instance tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Instance started successfully"}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool("start_gpu_instance", {"id": "123"})

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance/123/start",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == {"message": "Instance started successfully"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_stop_gpu_instance(mock_get: mock.MagicMock) -> None:
    """
    Test that stop_gpu_instance tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Instance stopped successfully"}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool("stop_gpu_instance", {"id": "123"})

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance/123/stop",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == {"message": "Instance stopped successfully"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_reboot_gpu_instance(mock_get: mock.MagicMock) -> None:
    """
    Test that reboot_gpu_instance tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Instance rebooted successfully"}
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool("reboot_gpu_instance", {"id": "123"})

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance/123/reboot",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == {"message": "Instance rebooted successfully"}


@pytest.mark.asyncio
@mock.patch("requests.post")
async def test_create_gpu_instance(mock_post: mock.MagicMock) -> None:
    """
    Test that create_gpu_instance tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Instance created successfully"}
    mock_post.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool(
            "create_gpu_instance",
            {
                "instance_name": "test-instance",
                "product_id": "test-product",
                "image_id": "test-image",
                "ssh_key_id": "123"
            }
        )

    # Assertions
    mock_post.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/instance",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "instance_name": "test-instance",
            "product_id": "test-product",
            "image_id": "test-image",
            "ssh_key_id": "123"
        }
    )
    assert json.loads(result[0].text) == {"message": "Instance created successfully"}


@pytest.mark.asyncio
@mock.patch("requests.delete")
async def test_delete_ssh_key(mock_delete: mock.MagicMock) -> None:
    """
    Test that delete_ssh_key tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "SSH key deleted successfully"}
    mock_delete.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool("delete_ssh_key", {"id": "123"})

    # Assertions
    mock_delete.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/ssh-keys/123",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    assert json.loads(result[0].text) == {"message": "SSH key deleted successfully"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_list_available_os_images(mock_get: mock.MagicMock) -> None:
    """
    Test that list_available_os_images resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "name": "test-image"}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://available_os_images")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/computing/images",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params=None
    )
    assert json.loads(result[0].text) == [{"id": "123", "name": "test-image"}]


@pytest.mark.asyncio
@mock.patch("requests.post")
async def test_create_ssh_key(mock_post: mock.MagicMock) -> None:
    """
    Test that create_ssh_key tool calls the correct API endpoint.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "SSH key created successfully"}
    mock_post.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the tool
        result = await client.call_tool(
            "create_ssh_key",
            {
                "key_name": "test-key",
                "key_data": "test-data"
            }
        )

    # Assertions
    mock_post.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/ssh-keys",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "key_name": "test-key",
            "key_data": "test-data"
        }
    )
    assert json.loads(result[0].text) == {"message": "SSH key created successfully"}


@pytest.mark.asyncio
@mock.patch("requests.get")
async def test_get_payment_history(mock_get: mock.MagicMock) -> None:
    """
    Test that get_payment_history resource returns expected data.
    """
    # Mock the response from the external API
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "123", "amount": 100}]
    mock_get.return_value = mock_response

    # Create a FastMCP Client instance
    async with Client(mcp) as client:
        # Call the resource
        result = await client.read_resource("mcp://payment_history?limit=10&offset=0")

    # Assertions
    mock_get.assert_called_once_with(
        f"{settings.NEBULA_BLOCK_API_URL}/api/v1/users/credits/history",
        headers={
            "Authorization": f"Bearer {settings.NEBULA_BLOCK_API_KEY}",
            "Content-Type": "application/json"
        },
        params={"limit": 10, "offset": 0}
    )
    assert json.loads(result[0].text) == [{"id": "123", "amount": 100}]
