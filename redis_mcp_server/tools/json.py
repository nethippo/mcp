"""JSON tools for Redis MCP Server."""

import json
from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import Any, List


class JsonSetArgs(BaseModel):
    """Arguments for json_set tool."""
    key: str = Field(..., description="The key to store the JSON")
    path: str = Field("$", description="The JSON path to set (default: root)")
    json_value: Any = Field(..., description="The JSON value to set")


class JsonGetArgs(BaseModel):
    """Arguments for json_get tool."""
    key: str = Field(..., description="The key of the JSON")
    path: str = Field("$", description="The JSON path to get (default: root)")


class JsonDeleteArgs(BaseModel):
    """Arguments for json_delete tool."""
    key: str = Field(..., description="The key of the JSON")
    path: str = Field("$", description="The JSON path to delete (default: root)")


class JsonTypeArgs(BaseModel):
    """Arguments for json_type tool."""
    key: str = Field(..., description="The key of the JSON")
    path: str = Field("$", description="The JSON path to check type (default: root)")


class JsonArrayAppendArgs(BaseModel):
    """Arguments for json_array_append tool."""
    key: str = Field(..., description="The key of the JSON array")
    path: str = Field("$", description="The JSON path to the array")
    values: List[Any] = Field(..., description="The values to append to the array")


@server.tool("json_set")
def json_set(args: JsonSetArgs, context: RedisContext) -> str:
    """Set a JSON value at a specific path."""
    try:
        # For simplicity, store the entire JSON as a string
        # In a real RedisJSON implementation, this would use JSON.SET
        json_str = json.dumps(args.json_value)
        result = context.redis.set(f"{args.key}:{args.path}", json_str)
        return f"Set JSON at path '{args.path}' in key '{args.key}': {result}"
    except Exception as e:
        return f"Error setting JSON: {e}"


@server.tool("json_get")
def json_get(args: JsonGetArgs, context: RedisContext) -> str:
    """Get a JSON value from a specific path."""
    try:
        # For simplicity, retrieve the stored JSON string
        # In a real RedisJSON implementation, this would use JSON.GET
        result = context.redis.get(f"{args.key}:{args.path}")
        if result is None:
            return f"No JSON found at path '{args.path}' in key '{args.key}'"
        json_value = json.loads(result.decode('utf-8'))
        return f"JSON at path '{args.path}' in key '{args.key}': {json_value}"
    except Exception as e:
        return f"Error getting JSON: {e}"


@server.tool("json_delete")
def json_delete(args: JsonDeleteArgs, context: RedisContext) -> str:
    """Delete a JSON value at a specific path."""
    try:
        # For simplicity, delete the stored JSON
        # In a real RedisJSON implementation, this would use JSON.DEL
        result = context.redis.delete(f"{args.key}:{args.path}")
        return f"Deleted JSON at path '{args.path}' in key '{args.key}': {result} keys deleted"
    except Exception as e:
        return f"Error deleting JSON: {e}"


@server.tool("json_type")
def json_type(args: JsonTypeArgs, context: RedisContext) -> str:
    """Get the type of a JSON value at a specific path."""
    try:
        # For simplicity, get the stored JSON and check its type
        # In a real RedisJSON implementation, this would use JSON.TYPE
        result = context.redis.get(f"{args.key}:{args.path}")
        if result is None:
            return f"No JSON found at path '{args.path}' in key '{args.key}'"
        json_value = json.loads(result.decode('utf-8'))
        json_type = type(json_value).__name__
        return f"Type of JSON at path '{args.path}' in key '{args.key}': {json_type}"
    except Exception as e:
        return f"Error getting JSON type: {e}"


@server.tool("json_array_append")
def json_array_append(args: JsonArrayAppendArgs, context: RedisContext) -> str:
    """Append values to a JSON array at a specific path."""
    try:
        # For simplicity, get the current array, append, and store back
        # In a real RedisJSON implementation, this would use JSON.ARRAPPEND
        current_key = f"{args.key}:{args.path}"
        result = context.redis.get(current_key)
        if result is None:
            current_array = []
        else:
            current_array = json.loads(result.decode('utf-8'))
            if not isinstance(current_array, list):
                return f"Value at path '{args.path}' is not an array"

        current_array.extend(args.values)
        json_str = json.dumps(current_array)
        context.redis.set(current_key, json_str)
        return f"Appended {len(args.values)} values to JSON array at path '{args.path}' in key '{args.key}'"
    except Exception as e:
        return f"Error appending to JSON array: {e}"
