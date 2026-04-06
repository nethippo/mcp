# Copyright Redis MCP Server. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""List operations for Redis MCP Server."""

from redis_mcp_server.common.server import mcp
from redis_mcp_server.context import Context
from typing import Any


@mcp.tool()
async def list_push(key: str, values: list[Any], left: bool = True) -> str:
    """Push values to a list.

    Args:
        key: The name of the key
        values: Values to push
        left: Push to left (LPUSH) or right (RPUSH)

    Returns:
        Success message or error message
    """
    if Context.readonly_mode():
        return 'Error: Cannot modify list in readonly mode'

    try:
        r = Context.get_redis_client()
        if left:
            result = r.lpush(key, *values)
        else:
            result = r.rpush(key, *values)
        return f"Successfully pushed to list '{key}', new length: {result}"
    except Exception as e:
        return f"Error pushing to list '{key}': {str(e)}"


@mcp.tool()
async def list_pop(key: str, left: bool = True) -> str:
    """Pop value from a list.

    Args:
        key: The name of the key
        left: Pop from left (LPOP) or right (RPOP)

    Returns:
        Popped value or error message
    """
    if Context.readonly_mode():
        return 'Error: Cannot modify list in readonly mode'

    try:
        r = Context.get_redis_client()
        if left:
            result = r.lpop(key)
        else:
            result = r.rpop(key)
        if result is None:
            return f"List '{key}' is empty"
        return str(result)
    except Exception as e:
        return f"Error popping from list '{key}': {str(e)}"
