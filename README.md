# RIP.ie MCP Server

A Model Context Protocol (MCP) server that provides access to the RIP.ie GraphQL backend. This server enables seamless integration with various client applications, allowing users to query and retrieve death notices and related information from RIP.ie.

## Overview

This server implements a set of tools to interact with RIP.ie's GraphQL API, providing functionality to:

- Retrieve death notices and funeral arrangements
- Search through counties and towns
- Access detailed funeral director information
- Obtain comprehensive death notice details

## Installation

1. Ensure Python 3.6 or higher is installed on your system
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/RipIEMCP.git
   cd RipIEMCP
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

### For Claude Desktop

1. Open Claude Desktop settings
2. Navigate to the MCP Servers section
3. Add a new server with the following configuration:
   ```
   Name: RIP.ie
   Type: Local (stdio)
   Command: python path/to/rip_ie_server.py
   ```

### For Visual Studio Code

1. Install the MCP extension for Visual Studio Code
2. Open VS Code settings
3. Add the following configuration to your settings.json:
   ```json
   {
     "mcp.servers": {
       "ripie": {
         "name": "RIP.ie",
         "type": "local",
         "command": "python",
         "args": ["path/to/rip_ie_server.py"]
       }
     }
   }
   ```

## Available Tools

The server provides the following tools:

- `get_counties`: Retrieves a list of all counties
- `get_counties_for_filters`: Gets counties based on filter criteria
- `get_towns_for_filters`: Obtains towns within a specified county
- `search_death_notices`: Searches for death notices using various criteria
- `get_death_notice_fd_info`: Retrieves funeral director information for a specific death notice
- `get_death_notice_full`: Obtains complete details for a specific death notice

## Usage Examples

### Searching Death Notices

```python
{
    "list": {
        "page": 1,
        "perPage": 10,
        "filterQuery": {
            "counties": [],
            "towns": [],
            "dateFrom": null,
            "dateTo": null
        }
    },
    "isTiledView": false
}
```

### Retrieving County Information

```python
{
    "input": {
        "counties": [],
        "towns": [],
        "dateFrom": null,
        "dateTo": null
    }
}
```

## Error Handling

The server implements robust error handling for:
- Invalid JSON input
- Unknown tool requests
- Network communication failures
- API response errors

## Technical Requirements

- Python 3.6+
- requests library
- Internet connection to access RIP.ie API
- Compatible MCP client (Claude Desktop or VS Code with MCP extension)

## Support

For issues, questions, or contributions, please create an issue in the project repository.

## Legal Notice

This tool is designed for legitimate use of publicly available data from RIP.ie. Users should comply with RIP.ie's terms of service and use the tool responsibly.