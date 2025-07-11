import json
import subprocess
import sys
import os
import time

class MCPTestClient:
    def __init__(self):
        self.process = None
        self.request_id = 1

    def start_server(self):
        """Start the MCP server process."""
        server_path = os.path.join(os.getcwd(), 'rip-ie-server', 'rip_ie_server.py')
        try:
            self.process = subprocess.Popen(
                [sys.executable, server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            return True
        except Exception as e:
            print(f"Error starting server: {e}", file=sys.stderr)
            return False

    def send_message(self, message):
        """Send a message to the server and read the response."""
        if not self.process:
            return None
        
        try:
            json_message = json.dumps(message) + '\n'
            self.process.stdin.write(json_message)
            self.process.stdin.flush()
            
            response_line = self.process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
        except Exception as e:
            print(f"Error communicating with server: {e}", file=sys.stderr)
        return None

    def stop_server(self):
        """Stop the server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()

    def initialize_server(self):
        """Initialize the MCP server connection."""
        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        self.request_id += 1
        print("Initializing MCP server...")
        response = self.send_message(message)
        if response and response.get("result"):
            print("Server initialized successfully")
            return True
        else:
            print(f"Failed to initialize server: {response}")
            return False

    def list_tools(self):
        """List available tools from the server."""
        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list"
        }
        self.request_id += 1
        print("Listing available tools...")
        response = self.send_message(message)
        if response and response.get("result"):
            tools = response["result"]["tools"]
            print(f"Available tools: {len(tools)}")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            return True
        else:
            print(f"Failed to list tools: {response}")
            return False

    def call_tool(self, tool_name, arguments):
        """Call a tool on the server."""
        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        self.request_id += 1
        print(f"Calling MCP tool: {tool_name} with args: {arguments}")
        response = self.send_message(message)
        
        if response and "result" in response:
            print(f"Result from MCP tool {tool_name}:")
            content = response["result"].get("content", [])
            for content_block in content:
                if content_block.get("type") == "text":
                    print(content_block.get("text"))
        elif response and "error" in response:
            error = response["error"]
            print(f"Error from MCP tool {tool_name}: [{error.get('code')}] {error.get('message')}")
        else:
            print(f"Unexpected response from MCP server for tool {tool_name}: {response}")
        return response
if __name__ == "__main__":
    print("--- Testing Rip.ie MCP Server ---")
    
    client = MCPTestClient()
    
    try:
        # Start the server
        print("\n--- Starting MCP Server ---")
        if not client.start_server():
            print("Failed to start server, exiting")
            sys.exit(1)

        # Initialize the server
        print("\n--- Initializing MCP Server ---")
        if not client.initialize_server():
            print("Failed to initialize server, exiting")
            sys.exit(1)

        # List tools
        print("\n--- Listing Available Tools ---")
        if not client.list_tools():
            print("Failed to list tools")

        # Test tools
        print("\n--- Testing get_counties ---")
        client.call_tool("get_counties", {})

        print("\n--- Testing get_counties_for_filters (search 'Dublin') ---")
        client.call_tool("get_counties_for_filters", {"input": {"search": "Dublin"}})

        print("\n--- Testing get_towns_for_filters (County ID 10 - Dublin) ---")
        client.call_tool("get_towns_for_filters", {"countyId": 10, "input": {"page": 1, "records": 5}})

        print("\n--- Testing search_death_notices (recent notices) ---")
        today = time.strftime("%Y-%m-%d")
        one_month_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 30 * 24 * 60 * 60))
        client.call_tool("search_death_notices", {
            "list": {
                "page": 1,
                "records": 5,
                "searchFields": [],
                "filters": [
                    {"field": "a.createdAt", "operator": "gte", "value": f"{one_month_ago} 00:00:00"},
                    {"field": "a.createdAt", "operator": "lte", "value": f"{today} 23:59:59"}
                ],
                "orders": [
                    {"field": "a.createdAtCastToDate", "type": "DESC"},
                    {"field": "a.escapedSurname", "type": "DESC"}
                ]
            },
            "isTiledView": False
        })

        print("\n--- Testing get_death_notice_full (ID 596530) ---")
        client.call_tool("get_death_notice_full", {"deathNoticeId": 596530})

        print("\n--- Testing get_death_notice_fd_info (ID 596530) ---")
        client.call_tool("get_death_notice_fd_info", {"deathNoticeId": 596530})

    finally:
        # Clean up
        client.stop_server()