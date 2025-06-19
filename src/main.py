import click
from tools import mcp
from src.config import settings

@click.command()
@click.option("--api-key", type=str, help="API key for NebulaBlock")
def main(api_key):
    """
    NebulaBlock MCP Server
    """
    if api_key:
        settings.NEBULA_BLOCK_API_KEY = api_key
        print("NEBULA_BLOCK_API_KEY updated from command line argument.")

    # mcp.run(transport="sse", host="192.168.2.98", port=8000)
    mcp.run()

if __name__ == "__main__":
    main()
