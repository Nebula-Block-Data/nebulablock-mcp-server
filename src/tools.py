from fastmcp import FastMCP
import requests
from src.config import settings

mcp = FastMCP()

def _make_api_request(endpoint: str, params: dict = None):
    api_url = settings.NEBULA_BLOCK_API_URL
    api_key = settings.NEBULA_BLOCK_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{api_url}/api/v1/{endpoint}", headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def _make_api_put_request(endpoint: str, json_data: dict):
    api_url = settings.NEBULA_BLOCK_API_URL
    api_key = settings.NEBULA_BLOCK_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.put(f"{api_url}/api/v1/{endpoint}", headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def _make_api_post_request(endpoint: str, json_data: dict):
    api_url = settings.NEBULA_BLOCK_API_URL
    api_key = settings.NEBULA_BLOCK_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{api_url}/api/v1/{endpoint}", headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def _make_api_delete_request(endpoint: str):
    api_url = settings.NEBULA_BLOCK_API_URL
    api_key = settings.NEBULA_BLOCK_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.delete(f"{api_url}/api/v1/{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()


@mcp.tool("get_computing_products")
@mcp.resource("mcp://computing_products")
def get_computing_products():
    return _make_api_request("computing/products")


@mcp.tool("get_user_instances")
@mcp.resource("mcp://user_instances?limit={limit}&offset={offset}")
def get_user_instances(limit: int = None, offset: int = None):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return _make_api_request("computing/instances", params)


@mcp.tool("get_user_instance_detail")
@mcp.resource("mcp://user_instance_detail/{id}")
def get_user_instance_detail(id: str):
    return _make_api_request(f"computing/instance/{id}")


@mcp.tool("list_deleted_user_instances")
@mcp.resource("mcp://deleted_user_instances")
def list_deleted_user_instances():
    return _make_api_request("computing/deleted-instances")


@mcp.tool("get_user_credit_balance")
@mcp.resource("mcp://billing_user_credit_balance")
def get_user_credit_balance():
    return _make_api_request("users/credits")


@mcp.tool("list_user_invoices")
@mcp.resource("mcp://billing_user_invoices?limit={limit}&offset={offset}")
def list_user_invoices(limit: int = None, offset: int = None):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return _make_api_request("users/invoices", params)


@mcp.resource("mcp://api_keys")
@mcp.tool("list_api_keys")
def list_api_keys():
    return _make_api_request("keys")


@mcp.tool("list_ssh_keys")
@mcp.resource("mcp://ssh_keys")
def list_ssh_keys():
    return _make_api_request("ssh-keys")


@mcp.tool("delete_gpu_instance")
def delete_gpu_instance(id: str):
    """
    Delete GPU Instances.

    Permanently delete an instance by specifying the instance ID in the path to delete the selected instance.
    """
    return _make_api_delete_request(f"computing/instance/{id}")


@mcp.tool("start_gpu_instance")
def start_gpu_instance(id: str):
    """
    Start GPU Instances.

    Initiate the startup of an instance. Provide the instance ID in the path to start the specified instance.
    """
    return _make_api_request(f"computing/instance/{id}/start")


@mcp.tool("stop_gpu_instance")
def stop_gpu_instance(id: str):
    """
    Stop GPU Instances.

    Shut down an instance. Provide the instance ID in the path to initiate the shutdown process for that instance.
    """
    return _make_api_request(f"computing/instance/{id}/stop")


@mcp.tool("reboot_gpu_instance")
def reboot_gpu_instance(id: str):
    """
    Reboot GPU Instances.

    Initiate a reboot of an instance. Provide the instance ID in the path to reboot the specified instance.
    """
    return _make_api_request(f"computing/instance/{id}/reboot")


@mcp.tool("create_gpu_instance")
def create_gpu_instance(instance_name: str, product_id: str, image_id: str, ssh_key_id: str):
    """
    Create GPU Instances.

    Create an instance with the specified custom configuration and features provided in the request body.
    """
    json_data = {
        "instance_name": instance_name,
        "product_id": product_id,
        "image_id": image_id,
        "ssh_key_id": ssh_key_id
    }
    return _make_api_post_request("computing/instance", json_data)


# NOTE: seems this api does not exist
# @mcp.tool("rename_ssh_key")
# def rename_ssh_key(id: int, key_name: str):
#     """
#     Rename SSH Key.

#     Updates the name of a specified SSH key. Include the ID of the SSH key in the endpoint path and the new name in the body of the request.
#     """
#     json_data = {
#         "key_name": key_name
#     }
#     return _make_api_put_request(f"ssh-keys/{id}", json_data)


@mcp.tool("delete_ssh_key")
def delete_ssh_key(id: str):
    """
    Deletes a specified SSH key by including the ID of the SSH key in the endpoint path.
    """
    return _make_api_delete_request(f"ssh-keys/{id}")


# NOTE: seems this api does not exist
# @mcp.tool("delete_api_key")
# def delete_api_key(id: int):
#     """
#     Deletes a specified API key by including the ID of the API key in the endpoint path.
#     """
#     return _make_api_delete_request(f"api_keys/{id}")


@mcp.tool("list_available_os_images")
@mcp.resource("mcp://available_os_images")
def list_available_os_images():
    """
    List Available OS Images.

    Return a list of all available operating system images, including details about each image's version and driver, if applicable.
    """
    return _make_api_request("computing/images")


@mcp.tool("create_ssh_key")
def create_ssh_key(key_name: str, key_data: str):
    """
    Creates an SSH key for use in your instances.
    """
    json_data = {
        "key_name": key_name,
        "key_data": key_data
    }
    return _make_api_post_request("ssh-keys", json_data)


@mcp.tool("get_payment_history")
@mcp.resource("mcp://payment_history?limit={limit}&offset={offset}")
def get_payment_history(limit: int = None, offset: int = None):
    """
    Retrieve the user's transaction history.

    Retrieve your credit payment history for different products.
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return _make_api_request("users/credits/history", params)
