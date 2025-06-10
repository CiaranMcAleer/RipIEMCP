import json
import subprocess
import sys
import os
import time

def send_mcp_message(message):
    """Sends a message to the MCP server via stdin and reads the response."""
    # This function simulates sending a message to the MCP server and getting a response.
    # For testing, we'll directly call the server script and capture its stdout.
    
    server_path = os.path.join(os.getcwd(), 'rip-ie-server', 'rip_ie_server.py')

    try:
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        json_message = json.dumps(message) + '\n'
        stdout, stderr = process.communicate(input=json_message, timeout=10)
        
        if stderr:
            print(f"Server stderr: {stderr}", file=sys.stderr)
        
        if stdout:
            # Assuming the server outputs one JSON object per line
            for line in stdout.strip().split('\n'):
                if line:
                    return json.loads(line)
        return None
        
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print(f"Server timed out. Stderr: {stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: Server script not found at {server_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error running server process: {e}", file=sys.stderr)
        return None

def call_mcp_tool(tool_name, arguments):
    """Constructs and sends an MCP tool_code message."""
    message = {
        "type": "tool_code",
        "toolName": tool_name,
        "arguments": arguments,
        "callId": f"test-call-{int(time.time())}" # Unique ID for the call
    }
    print(f"Calling MCP tool: {tool_name} with args: {arguments}")
    response = send_mcp_message(message)
    if response and response.get("type") == "tool_output":
        if response.get("isError"):
            print(f"Error from MCP tool {tool_name}: {response.get('result', {}).get('content', [{}])[0].get('text', 'Unknown error')}")
        else:
            print(f"Result from MCP tool {tool_name}:")
            for content_block in response.get("result", {}).get("content", []):
                if content_block.get("type") == "text":
                    print(content_block.get("text"))
    else:
        print(f"Unexpected response from MCP server for tool {tool_name}: {response}")
    return response

if __name__ == "__main__":
    print("--- Testing Rip.ie MCP Server Tools ---")

    # Test 1: get_counties
    print("\n--- Testing get_counties ---")
    call_mcp_tool("get_counties", {})

    # Test 2: get_counties_for_filters (with search)
    print("\n--- Testing get_counties_for_filters (search 'Dublin') ---")
    call_mcp_tool("get_counties_for_filters", {"input": {"search": "Dublin"}})

    # Test 3: get_towns_for_filters (for County Dublin, ID 10)
    print("\n--- Testing get_towns_for_filters (County ID 10 - Dublin) ---")
    call_mcp_tool("get_towns_for_filters", {"countyId": 10, "input": {"page": 1, "records": 5}})


    # Test 5: search_death_notices (recent notices, adjust dates as needed)
    # NOTE: Adjust dates to a recent range for actual results
    print("\n--- Testing search_death_notices (recent notices) ---")
    today = time.strftime("%Y-%m-%d")
    one_month_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 30 * 24 * 60 * 60))
    call_mcp_tool("search_death_notices", {
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

    # Test 6: get_death_notice_full (use an ID from a recent search if possible)
    # For demonstration, using a known ID from the analysis.md 
    print("\n--- Testing get_death_notice_full (ID 596530) ---")
    call_mcp_tool("get_death_notice_full", {"deathNoticeId": 596530})

    # Test 7: get_death_notice_fd_info (use an ID from a recent search if possible)
    # For demonstration, using a known ID from the analysis.md
    print("\n--- Testing get_death_notice_fd_info (ID 596530) ---")
    call_mcp_tool("get_death_notice_fd_info", {"deathNoticeId": 596530})