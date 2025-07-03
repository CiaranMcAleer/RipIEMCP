# RIP.ie MCP Server

[![Test MCP Server](https://github.com/CiaranMcAleer/RipIEMCP/actions/workflows/test.yml/badge.svg)](https://github.com/CiaranMcAleer/RipIEMCP/actions/workflows/test.yml)
[![Security and Dependencies](https://github.com/CiaranMcAleer/RipIEMCP/actions/workflows/security.yml/badge.svg)](https://github.com/CiaranMcAleer/RipIEMCP/actions/workflows/security.yml)

A **Model Context Protocol (MCP) compliant** server that provides access to the RIP.ie GraphQL backend. This server enables seamless integration with various MCP-compatible client applications, allowing users to query and retrieve death notices and related information from RIP.ie.

## Overview

This server implements a fully compliant MCP server with proper JSON-RPC 2.0 protocol support and provides a set of tools to interact with RIP.ie's GraphQL API:

- **Tool Discovery**: Automatic tool listing with detailed schemas and descriptions
- **Error Handling**: Proper JSON-RPC error responses with meaningful error codes

### Available Functionality

- Retrieve death notices and funeral arrangements
- Search through counties and towns
- Access detailed funeral director information
- Obtain comprehensive death notice details
## Installation

1. Ensure Python 3.7 or higher is installed on your system
2. Clone this repository:
   ```bash
   git clone https://github.com/CiaranMcAleer/RipIEMCP.git
   cd RipIEMCP
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing

Run the test suite to verify the server functionality:

```bash
python test_rip_ie_mcp.py
```

The test suite will:
- Initialize the MCP server
- Test tool discovery
- Verify all available tools
- Test actual API calls to RIP.ie
## Configuration

### For Claude Desktop

1. Open Claude Desktop settings
2. Navigate to the MCP Servers section
3. Add a new server with the following configuration:
   ```json
   {
     "mcpServers": {
       "ripie": {
         "command": "python",
         "args": ["path/to/RipIEMCP/rip-ie-server/rip_ie_server.py"]
       }
     }
   }
   ```

### For Other MCP Clients

This server follows the MCP 2025-06-18 specification and should work with any compliant MCP client. Configure your client to use:

- **Transport**: stdio
- **Command**: `python path/to/RipIEMCP/rip-ie-server/rip_ie_server.py`
- **Protocol Version**: 2025-06-18
## Available Tools

The server automatically advertises the following tools via the MCP `tools/list` endpoint:

- **`get_counties`**: Get all counties in Ireland from Rip.ie
- **`get_counties_for_filters`**: Get counties filtered by search criteria
- **`get_towns_for_filters`**: Get towns in a specific county
- **`search_death_notices`**: Search for death notices with filters
- **`get_death_notice_full`**: Get full details of a death notice
- **`get_death_notice_fd_info`**: Get funeral director and location information for a death notice

Each tool includes detailed JSON schema validation for parameters and comprehensive error handling.

## Protocol Features

### JSON-RPC 2.0 Compliance
- Proper request/response ID handling
- Standard error codes and messages
- Protocol version negotiation

### MCP Specification Support
- Server initialization with capability negotiation
- Tool discovery through `tools/list`
- Structured tool execution via `tools/call`
- Proper content block formatting for responses

## Usage Examples

### MCP Client Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_death_notices",
    "arguments": {
      "list": {
        "page": 1,
        "records": 5,
        "searchFields": [],
        "filters": [
          {"field": "a.createdAt", "operator": "gte", "value": "2025-06-01 00:00:00"}
        ],
        "orders": [
          {"field": "a.createdAtCastToDate", "type": "DESC"}
        ]
      },
      "isTiledView": false
    }
  }
}
```

### Tool Parameters

#### get_counties_for_filters
```json
{
  "input": {
    "search": "Dublin"
  }
}
```

#### get_towns_for_filters
```json
{
  "countyId": 10,
  "input": {
    "page": 1,
    "records": 10
  }
}
```

## Error Handling

The server implements robust JSON-RPC 2.0 error handling:
- **-32600**: Invalid Request (malformed JSON-RPC)
- **-32601**: Method Not Found (unknown tool or method)
- **-32602**: Invalid Params (missing required parameters)
- **-32603**: Internal Error (API failures, network issues)
- **-32002**: Server Not Initialized (server state error)

## Technical Requirements

- **Python 3.7+** (updated requirement)
- **requests library** (for API calls)
- **Internet connection** to access RIP.ie API
- **MCP-compatible client** (Claude Desktop, VS Code, etc.)

## CI/CD

This project includes GitHub Actions for automated testing:
- Runs tests on Python 3.7, 3.8, 3.9, 3.10, 3.11
- Tests all MCP protocol functionality
- Validates API integration
- Reports test results with detailed output
## Support

For issues, questions, or contributions, please create an issue in the project repository.

## Legal Notice

Users should comply with RIP.ie's terms of service and use the tool responsibly.