# NebulaBlock API MCP

This project serves as a Model Context Protocol (MCP) server for the NebulaBlock API (`https://api.nebulablock.com`). It demonstrates how to integrate with the `fastmcp` library to expose NebulaBlock API functionalities as tools, enabling seamless interaction within an MCP-compatible environment.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── tools.py
│   └── mcp_project.egg-info/
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── scripts/
├── docs/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```

*   `src/`: Contains the main application source code, including configuration and tool definitions.
*   `tests/`: Contains unit and integration tests.
*   `scripts/`: Reserved for utility scripts (e.g., setup, data generation).
*   `docs/`: Reserved for supplementary documentation.
*   `.env.example`: Example file for environment variables.
*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `pyproject.toml`: Project metadata and build system configuration, including dependencies and project information.
*   `README.md`: This documentation file.
*   `uv.lock`: Lock file for `uv` dependency management.

## Installation and Setup

To set up and run this project, follow these steps:

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/Nebula-Block-Data/api-mcp
    cd mcp-project
    ```

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install dependencies:**
    This project uses `pyproject.toml` for dependency management. Install `setuptools` and then the project in editable mode.
    ```bash
    pip install setuptools
    pip install -e .
    ```
    This will install `fastmcp` and any other dependencies specified in `pyproject.toml`.

## Running the Application

To run the simple "hello world" application:

```bash
python -m src.main
```

You should see the output: `Hello from mcp_project! fastmcp is integrated.`

### Configuring API Key

The NebulaBlock API key can be configured in two ways:

1.  **Using the `--api-key` command-line argument:**
    You can provide the API key directly when running the application:
    ```bash
    python -m src.main --api-key your_nebula_block_api_key
    ```
    This method will override any API key set in the `.env` file.

2.  **Using a `.env` file:**
    Create a file named `.env` in the root directory of the project and add your API key to it:
    ```
    NEBULA_BLOCK_API_KEY=your_nebula_block_api_key
    ```
    The application will automatically load the API key from this file if the `--api-key` argument is not provided.

## Running Tests

To run the unit tests, ensure your virtual environment is activated and `pytest` is installed (it will be installed with `pip install -e .`):

```bash
pytest
```

You should see output indicating that the tests passed.

## MCP Server Configuration Example

Here's an example of how you might configure an MCP server in your `settings.json` (or similar configuration file) to run this project:

```json
{
  "mcpServers": {
    "nebula": {
      "command": "~/path/to/uv",
      "args": [
        "--directory",
        "~/path/to/nebulablock_mcp",
        "run",
        "-m",
        "src.main",
        "--api-key=YOUR_API_KEY"
      ]
    }
  }
}
```

*   Replace `~/path/to/uv` with the actual path to your `uv` executable.
*   Replace `~/path/to/nebulablock_mcp` with the actual path to your project directory.
*   Replace `YOUR_API_KEY` with your actual NebulaBlock API key.

## `fastmcp` Integration

This project demonstrates a minimal integration of `fastmcp`. The `src/main.py` module initializes a basic `fastmcp.mcp.MCP` object, showcasing that the library can be successfully imported and instantiated within the project's structure. This serves as a starting point for more complex simulations or applications using `fastmcp`.

## Code Quality and Style

This project adheres to the following code quality standards:

*   **Type Hinting:** Extensive use of Python's type hints for improved readability and maintainability.
*   **PEP 8:** Strict adherence to PEP 8 guidelines for code formatting and style.
*   **Docstrings:** Comprehensive Google-style docstrings for all modules, classes, methods, and functions.
*   **Comments:** Judicious use of inline comments for complex logic or design decisions.

## License

This project is licensed under the MIT License. See the `LICENSE` file (if created) for details.