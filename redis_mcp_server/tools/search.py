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

"""Search tools for Redis MCP Server."""

from ..common.server import mcp, server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class SearchCreateIndexArgs(BaseModel):
    """Arguments for search_create_index tool."""
    index_name: str = Field(..., description="The name of the index to create")
    schema: Dict[str, str] = Field(..., description="The schema definition for the index")


class SearchQueryArgs(BaseModel):
    """Arguments for search_query tool."""
    index_name: str = Field(..., description="The name of the index to query")
    query: str = Field(..., description="The search query")
    limit: Optional[int] = Field(10, description="Maximum number of results to return")


class SearchDropIndexArgs(BaseModel):
    """Arguments for search_drop_index tool."""
    index_name: str = Field(..., description="The name of the index to drop")


@server.tool("search_create_index")
def search_create_index(args: SearchCreateIndexArgs, context: RedisContext) -> str:
    """Create a RediSearch index."""
    try:
        # RediSearch is not installed, return error message
        return "RediSearch is not available. Please install the RediSearch module on your Redis server to use search functionality."
    except Exception as e:
        return f"Error creating search index: {e}"


@mcp.tool()
async def search_add_document(
    index_name: str,
    doc_id: str,
    fields: Dict[str, Any],
) -> str:
    """Add a document to a RediSearch index.

    Args:
        index_name: Name of the index
        doc_id: Document ID
        fields: Document fields as dict

    Returns:
        Success message or error message
    """
    if RedisContext.readonly_mode():
        return 'Error: Cannot add document in readonly mode'

    try:
        client = RedisContext.get_search_client(index_name)
        client.add_document(doc_id, **fields)
        return f"Document '{doc_id}' added to index '{index_name}'"
    except Exception as e:
        return f"Error adding document to '{index_name}': {str(e)}"


@mcp.tool()
async def search_query(
    index_name: str,
    query: str,
) -> str:
    """Search documents in a RediSearch index.

    Args:
        index_name: Name of the index
        query: Search query

    Returns:
        Search results or error message
    """
    try:
        client = RedisContext.get_search_client(index_name)
        result = client.search(query)
        return str(result.docs)
    except Exception as e:
        return f"Error searching '{index_name}': {str(e)}"


@mcp.tool()
async def search_drop_index(index_name: str) -> str:
    """Drop a RediSearch index.

    Args:
        index_name: Name of the index to drop

    Returns:
        Success message or error message
    """
    if RedisContext.readonly_mode():
        return 'Error: Cannot drop index in readonly mode'

    try:
        client = RedisContext.get_search_client(index_name)
        client.drop_index()
        return f"Index '{index_name}' dropped successfully"
    except Exception as e:
        return f"Error dropping index '{index_name}': {str(e)}"


@mcp.tool()
async def search_info(index_name: str) -> str:
    """Get information about a RediSearch index.

    Args:
        index_name: Name of the index

    Returns:
        Index info or error message
    """
    try:
        client = RedisContext.get_search_client(index_name)
        info = client.info()
        return str(info)
    except Exception as e:
        return f"Error getting info for '{index_name}': {str(e)}"
