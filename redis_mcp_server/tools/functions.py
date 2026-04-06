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

"""Functions tools for Redis MCP Server."""

from ..common.server import mcp, server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import Any, List, Optional


class FunctionLoadArgs(BaseModel):
    """Arguments for function_load tool."""
    code: str = Field(..., description="The Lua code for the functions")
    library_name: Optional[str] = Field(None, description="The name of the function library")


class FunctionCallArgs(BaseModel):
    """Arguments for function_call tool."""
    function_name: str = Field(..., description="The name of the function to call")
    args: Optional[List[Any]] = Field(None, description="The arguments to pass to the function")


class FunctionListArgs(BaseModel):
    """Arguments for function_list tool."""
    library_name_pattern: Optional[str] = Field(None, description="Pattern to match library names")


@server.tool("function_load")
def function_load(args: FunctionLoadArgs, context: RedisContext) -> str:
    """Load a Redis Function library."""
    try:
        # Redis Functions require Redis 7.0+ and may not be available in all redis-py versions
        return "Redis Functions are not fully supported in this redis-py version. Please use Redis 7.0+ with appropriate client library."
    except Exception as e:
        return f"Error loading function library: {e}"


@mcp.tool()
async def function_call(function_name: str, args: str) -> str:
    """Call a Redis Function.

    Args:
        function_name: Name of the function to call
        args: Arguments for the function

    Returns:
        Function result or error message
    """
    try:
        r = RedisContext.get_redis_client()
        result = r.fcall(function_name, args or [])
        return str(result)
    except Exception as e:
        return f"Error calling function '{function_name}': {str(e)}"


@mcp.tool()
async def function_list() -> str:
    """List Redis Functions.

    Returns:
        List of functions or error message
    """
    try:
        r = RedisContext.get_redis_client()
        result = r.function_list()
        return str(result)
    except Exception as e:
        return f"Error listing functions: {str(e)}"


@mcp.tool()
async def function_delete(library_name: str) -> str:
    """Delete a Redis Function library.

    Args:
        library_name: Name of the function library to delete

    Returns:
        Success message or error message
    """
    if RedisContext.readonly_mode():
        return 'Error: Cannot delete functions in readonly mode'

    try:
        r = RedisContext.get_redis_client()
        r.function_delete(library_name)
        return f"Function library '{library_name}' deleted successfully"
    except Exception as e:
        return f"Error deleting function library '{library_name}': {str(e)}"
