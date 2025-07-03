#!/usr/bin/env python3
import json
import sys
import requests
from typing import Any, Dict, List, Optional, Union

# Base URL for the Rip.ie GraphQL API
RIP_IE_GRAPHQL_URL = "https://rip.ie/api/graphql"

# Common headers required for all requests
COMMON_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://rip.ie",
    "priority": "u=1, i",
    "referer": "https://rip.ie/death-notice/recent",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
}

# MCP Protocol Constants
MCP_VERSION = "2025-06-18"
SERVER_NAME = "rip-ie-mcp-server"
SERVER_VERSION = "2.0.0"#Last updated: 03-07-2025
def send_graphql_request(operation_name, variables, query):
    """Sends a GraphQL request to the Rip.ie GraphQl instance."""
    payload = {
        "operationName": operation_name,
        "variables": variables,
        "query": query,
    }
    try:
        response = requests.post(RIP_IE_GRAPHQL_URL, headers=COMMON_HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"errors": [{"message": f"HTTP Request failed: {e}"}]}

def create_text_content(text: str) -> Dict[str, Any]:
    """Creates a MCP text content block."""
    return {
        "type": "text",
        "text": text
    }

def create_tool_result(content: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Creates a MCP tool result."""
    return {
        "content": content
    }

def create_error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    """Creates a JSON-RPC error response."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message
        }
    }

def create_success_response(request_id: Any, result: Any) -> Dict[str, Any]:
    """Creates a JSON-RPC success response."""
    return {
        "jsonrpc": "2.0", 
        "id": request_id,
        "result": result
    }

def get_server_info() -> Dict[str, Any]:
    """Returns MCP server information."""
    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "protocolVersion": MCP_VERSION
    }

def get_server_capabilities() -> Dict[str, Any]:
    """Returns the server capabilities."""
    return {
        "tools": {}
    }

def get_tools_list() -> List[Dict[str, Any]]:
    """Returns the list of available tools with their schemas.""" #current implementation will require this to be updated if the tools change
    return [
        {
            "name": "get_counties",
            "description": "Get all counties in Ireland from Rip.ie",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "get_counties_for_filters",
            "description": "Get counties filtered by search criteria",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "object",
                        "description": "Filter input parameters",
                        "properties": {
                            "search": {
                                "type": "string",
                                "description": "Search term for county names"
                            }
                        }
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_towns_for_filters",
            "description": "Get towns in a specific county",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "countyId": {
                        "type": "number",
                        "description": "The ID of the county"
                    },
                    "input": {
                        "type": "object",
                        "description": "Filter input parameters",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number for pagination"
                            },
                            "records": {
                                "type": "number", 
                                "description": "Number of records per page"
                            }
                        }
                    }
                },
                "required": ["countyId"]
            }
        },
        {
            "name": "search_death_notices",
            "description": "Search for death notices with filters",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "list": {
                        "type": "object",
                        "description": "Search parameters",
                        "properties": {
                            "page": {"type": "number"},
                            "records": {"type": "number"},
                            "searchFields": {"type": "array"},
                            "filters": {"type": "array"},
                            "orders": {"type": "array"}
                        },
                        "required": ["page", "records"]
                    },
                    "isTiledView": {
                        "type": "boolean",
                        "description": "Whether to use tiled view format"
                    }
                },
                "required": ["list", "isTiledView"]
            }
        },
        {
            "name": "get_death_notice_full",
            "description": "Get full details of a death notice",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "deathNoticeId": {
                        "type": "number",
                        "description": "The ID of the death notice"
                    }
                },
                "required": ["deathNoticeId"]
            }
        },
        {
            "name": "get_death_notice_fd_info", 
            "description": "Get funeral director and location information for a death notice",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "deathNoticeId": {
                        "type": "number",
                        "description": "The ID of the death notice"
                    }
                },
                "required": ["deathNoticeId"]
            }
        }
    ]
def handle_get_counties_for_filters(input_data):
    """Handles the getCountiesForFilters tool call."""
    query = """
        query getCountiesForFilters($input: FilterInputGraphql!) {
          getCountiesForFilters(input: $input) {
            total
            records {
              id
              name
            }
          }
        }
    """
    result = send_graphql_request("getCountiesForFilters", {"input": input_data}, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])

def handle_get_towns_for_filters(county_id, input_data):
    """Handles the getTownsForFilters tool call."""
    query = """
        query getTownsForFilters($countyId: Float!, $input: FilterInputGraphql!) {
          getTownsForFilters(countyId: $countyId, input: $input) {
            total
            records {
              id
              name
            }
          }
        }
    """
    result = send_graphql_request("getTownsForFilters", {"countyId": county_id, "input": input_data}, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])

def handle_search_death_notices(list_input, is_tiled_view):
    """Handles the searchDeathNoticesForListTableWithoutPhoto tool call."""
    query = """
        query searchDeathNoticesForListTableWithoutPhoto($list: ListInput!, $isTiledView: Boolean!) {
          searchDeathNoticesForList(query: $list, isTiledView: $isTiledView) {
            count
            perPage
            page
            nextPage
            records {
              id
              firstname
              surname
              nee
              createdAt
              funeralArrangementsLater
              arrangementsChange
              county {
                id
                name
              }
              town {
                id
                name
              }
            }
          }
        }
    """
    variables = {"list": list_input, "isTiledView": is_tiled_view}
    result = send_graphql_request("searchDeathNoticesForListTableWithoutPhoto", variables, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])

def handle_get_death_notice_fd_info(death_notice_id):
    """Handles the getDeathNoticeFDInfo tool call."""
    query = """
        query getDeathNoticeFDInfo($deathNoticeId: Float!) {
          previewDeathNotice(deathNoticeId: $deathNoticeId) {
            locations {
              id
              type
              name
              latitude
              longitude
              town {
                id
                name
              }
            }
            funeralHome {
              id
              name
              addressFirstPart
              addressSecondPart
              addressThirdPart
              city
              mapUrl
              websiteUrl
              email
              phone
              mobilePhone
              county {
                id
                name
              }
              funeralHomeAds {
                topBannerAttachment {
                  id
                  name
                  file
                }
                topBannerUrl
                secondTopBannerAttachment {
                  id
                  name
                  file
                }
                secondTopBannerUrl
                sideTopBannerAttachment {
                  id
                  name
                  file
                }
                sideTopBannerUrl
                sideMiddleBannerAttachment {
                  id
                  name
                  file
                }
                sideMiddleBannerUrl
                sideBottomBannerAttachment {
                  id
                  name
                  file
                }
                sideBottomBannerUrl
              }
              funeralDirector {
                advertisePlaces
                isIafd
                strapline
              }
            }
          }
        }
    """
    result = send_graphql_request("getDeathNoticeFDInfo", {"deathNoticeId": death_notice_id}, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])

def handle_get_counties():
    """Handles the getCounties tool call."""
    query = """
        query getCounties {
          getCounties {
            id
            name
          }
        }
    """
    result = send_graphql_request("getCounties", {}, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])

def handle_get_death_notice_full(death_notice_id):
    """Handles the getDeathNoticeFull tool call."""
    query = """
        query getDeathNoticeFull($deathNoticeId: Float!) {
          previewDeathNotice(deathNoticeId: $deathNoticeId) {
            id
            firstname
            surname
            nee
            createdAt
            funeralArrangementsLater
            arrangementsChange
            county {
              id
              name
            }
            town {
              id
              name
            }
            locations {
              id
              type
              name
              latitude
              longitude
              town {
                id
                name
              }
            }
            funeralHome {
              id
              name
              addressFirstPart
              addressSecondPart
              addressThirdPart
              city
              mapUrl
              websiteUrl
              email
              phone
              mobilePhone
              county {
                id
                name
              }
            }
          }
        }
    """
    result = send_graphql_request("getDeathNoticeFull", {"deathNoticeId": death_notice_id}, query)
    return create_tool_result([create_text_content(json.dumps(result, indent=2))])
class MCPServer:
    def __init__(self):
        self.state = "init"
        self.initialized = False

    def handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the initialize request."""
        client_info = params.get("clientInfo", {})
        protocol_version = params.get("protocolVersion", "")
        
        sys.stderr.write(f"Client connecting: {client_info.get('name', 'unknown')} v{client_info.get('version', 'unknown')}\n")
        sys.stderr.flush()
        
        if not protocol_version.startswith("2025-"):
            return create_error_response(request_id, -32602, f"Unsupported protocol version: {protocol_version}")
        
        self.initialized = True
        return create_success_response(request_id, {
            "protocolVersion": MCP_VERSION,
            "capabilities": get_server_capabilities(),
            "serverInfo": get_server_info()
        })

    def handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Handle tools/list request."""
        if not self.initialized:
            return create_error_response(request_id, -32002, "Server not initialized")
        
        return create_success_response(request_id, {
            "tools": get_tools_list()
        })

    def handle_tools_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request."""
        if not self.initialized:
            return create_error_response(request_id, -32002, "Server not initialized")
        
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "get_counties_for_filters":
                result = handle_get_counties_for_filters(arguments.get("input", {}))
            elif tool_name == "get_towns_for_filters":
                result = handle_get_towns_for_filters(
                    arguments["countyId"], 
                    arguments.get("input", {})
                )
            elif tool_name == "search_death_notices":
                result = handle_search_death_notices(
                    arguments["list"], 
                    arguments["isTiledView"]
                )
            elif tool_name == "get_death_notice_fd_info":
                result = handle_get_death_notice_fd_info(arguments["deathNoticeId"])
            elif tool_name == "get_counties":
                result = handle_get_counties()
            elif tool_name == "get_death_notice_full":
                result = handle_get_death_notice_full(arguments["deathNoticeId"])
            else:
                return create_error_response(request_id, -32601, f"Unknown tool: {tool_name}")
            
            return create_success_response(request_id, result)
        except KeyError as e:
            return create_error_response(request_id, -32602, f"Missing required parameter: {e}")
        except Exception as e:
            sys.stderr.write(f"Error executing tool {tool_name}: {e}\n")
            sys.stderr.flush()
            return create_error_response(request_id, -32603, f"Tool execution failed: {e}")

    def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle a single JSON-RPC message."""
        jsonrpc = message.get("jsonrpc")
        if jsonrpc != "2.0":
            return create_error_response(
                message.get("id"), 
                -32600, 
                "Invalid JSON-RPC version"
            )
        
        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params", {})
        
        if method == "initialize":
            return self.handle_initialize(request_id, params)
        elif method == "tools/list":
            return self.handle_tools_list(request_id)
        elif method == "tools/call":
            return self.handle_tools_call(request_id, params)
        elif method == "ping":
            return create_success_response(request_id, {})
        else:
            return create_error_response(request_id, -32601, f"Unknown method: {method}")

    def run(self):
        """Main server loop."""
        self.state = "running"
        sys.stderr.write(f"MCP Server {SERVER_NAME} v{SERVER_VERSION} starting\n")
        sys.stderr.flush()
        
        while self.state == "running":
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    message = json.loads(line)
                except json.JSONDecodeError as e:
                    sys.stderr.write(f"Invalid JSON received: {e}\n")
                    sys.stderr.flush()
                    continue
                
                response = self.handle_message(message)
                if response:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                sys.stderr.write(f"Unhandled error: {e}\n")
                sys.stderr.flush()
        
        self.state = "closed"

if __name__ == "__main__":
    server = MCPServer()
    server.run()
