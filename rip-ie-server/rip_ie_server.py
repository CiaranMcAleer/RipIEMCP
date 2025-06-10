#!/usr/bin/env python3
import json
import sys
import os
import requests

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

def send_graphql_request(operation_name, variables, query):
    """Sends a GraphQL request to the Rip.ie API."""
    payload = {
        "operationName": operation_name,
        "variables": variables,
        "query": query,
    }
    try:
        response = requests.post(RIP_IE_GRAPHQL_URL, headers=COMMON_HEADERS, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"errors": [{"message": f"HTTP Request failed: {e}"}]}

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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


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
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            message = json.loads(line)
            
            if message["type"] == "tool_code":
                tool_name = message["toolName"]
                arguments = message["arguments"]
                
                response = {"type": "tool_output", "toolName": tool_name, "callId": message["callId"]}
                
                try:
                    if tool_name == "get_counties_for_filters":
                        result = handle_get_counties_for_filters(arguments.get("input", {}))
                    elif tool_name == "get_towns_for_filters":
                        result = handle_get_towns_for_filters(arguments["countyId"], arguments.get("input", {}))
                    elif tool_name == "search_death_notices":
                        result = handle_search_death_notices(arguments["list"], arguments["isTiledView"])
                    elif tool_name == "get_death_notice_fd_info":
                        result = handle_get_death_notice_fd_info(arguments["deathNoticeId"])
                    elif tool_name == "get_counties":
                        result = handle_get_counties()
                    elif tool_name == "get_death_notice_full":
                        result = handle_get_death_notice_full(arguments["deathNoticeId"])
                    else:
                        raise ValueError(f"Unknown tool: {tool_name}")
                    
                    response["result"] = result
                except Exception as e:
                    response["isError"] = True
                    response["result"] = {"content": [{"type": "text", "text": f"Error executing tool {tool_name}: {e}"}]}
                
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            
            elif message["type"] == "ping":
                sys.stdout.write(json.dumps({"type": "pong"}) + "\n")
                sys.stdout.flush()

        except json.JSONDecodeError:
            sys.stderr.write("Error: Invalid JSON input\n")
            sys.stderr.flush()
        except Exception as e:
            sys.stderr.write(f"Unhandled error: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()