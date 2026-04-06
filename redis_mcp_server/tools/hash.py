"""Hash tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import List


class HashSetArgs(BaseModel):
    """Arguments for hash_set tool."""
    key: str = Field(..., description="The key of the hash")
    field: str = Field(..., description="The field to set")
    value: str = Field(..., description="The value to set")


class HashGetArgs(BaseModel):
    """Arguments for hash_get tool."""
    key: str = Field(..., description="The key of the hash")
    field: str = Field(..., description="The field to get")


class HashGetAllArgs(BaseModel):
    """Arguments for hash_get_all tool."""
    key: str = Field(..., description="The key of the hash")


class HashExistsArgs(BaseModel):
    """Arguments for hash_exists tool."""
    key: str = Field(..., description="The key of the hash")
    field: str = Field(..., description="The field to check")


class HashDeleteArgs(BaseModel):
    """Arguments for hash_delete tool."""
    key: str = Field(..., description="The key of the hash")
    fields: List[str] = Field(..., description="The fields to delete")


class HashKeysArgs(BaseModel):
    """Arguments for hash_keys tool."""
    key: str = Field(..., description="The key of the hash")


class HashValuesArgs(BaseModel):
    """Arguments for hash_values tool."""
    key: str = Field(..., description="The key of the hash")


class HashLengthArgs(BaseModel):
    """Arguments for hash_length tool."""
    key: str = Field(..., description="The key of the hash")


class HashIncrementArgs(BaseModel):
    """Arguments for hash_increment tool."""
    key: str = Field(..., description="The key of the hash")
    field: str = Field(..., description="The field to increment")
    amount: float = Field(1.0, description="The amount to increment by")


@server.tool("hash_set")
def hash_set(args: HashSetArgs, context: RedisContext) -> str:
    """Set the value of a field in a hash."""
    try:
        result = context.redis.hset(args.key, args.field, args.value)
        return f"Set field '{args.field}' in hash '{args.key}' to '{args.value}'. Result: {result}"
    except Exception as e:
        return f"Error setting hash field: {e}"


@server.tool("hash_get")
def hash_get(args: HashGetArgs, context: RedisContext) -> str:
    """Get the value of a field in a hash."""
    try:
        result = context.redis.hget(args.key, args.field)
        if result is None:
            return f"Field '{args.field}' does not exist in hash '{args.key}'"
        return f"Value of field '{args.field}' in hash '{args.key}': {result.decode('utf-8') if isinstance(result, bytes) else result}"
    except Exception as e:
        return f"Error getting hash field: {e}"


@server.tool("hash_get_all")
def hash_get_all(args: HashGetAllArgs, context: RedisContext) -> str:
    """Get all fields and values in a hash."""
    try:
        result = context.redis.hgetall(args.key)
        if not result:
            return f"Hash '{args.key}' is empty or does not exist"
        decoded_result = {k.decode('utf-8') if isinstance(k, bytes) else k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in result.items()}
        return f"All fields and values in hash '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting all hash fields: {e}"


@server.tool("hash_exists")
def hash_exists(args: HashExistsArgs, context: RedisContext) -> str:
    """Check if a field exists in a hash."""
    try:
        result = context.redis.hexists(args.key, args.field)
        return f"Field '{args.field}' exists in hash '{args.key}': {bool(result)}"
    except Exception as e:
        return f"Error checking hash field existence: {e}"


@server.tool("hash_delete")
def hash_delete(args: HashDeleteArgs, context: RedisContext) -> str:
    """Delete one or more fields from a hash."""
    try:
        result = context.redis.hdel(args.key, *args.fields)
        return f"Deleted {result} fields from hash '{args.key}'"
    except Exception as e:
        return f"Error deleting hash fields: {e}"


@server.tool("hash_keys")
def hash_keys(args: HashKeysArgs, context: RedisContext) -> str:
    """Get all field names in a hash."""
    try:
        result = context.redis.hkeys(args.key)
        decoded_result = [k.decode('utf-8') if isinstance(k, bytes) else k for k in result]
        return f"Fields in hash '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting hash keys: {e}"


@server.tool("hash_values")
def hash_values(args: HashValuesArgs, context: RedisContext) -> str:
    """Get all values in a hash."""
    try:
        result = context.redis.hvals(args.key)
        decoded_result = [v.decode('utf-8') if isinstance(v, bytes) else v for v in result]
        return f"Values in hash '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting hash values: {e}"


@server.tool("hash_length")
def hash_length(args: HashLengthArgs, context: RedisContext) -> str:
    """Get the number of fields in a hash."""
    try:
        result = context.redis.hlen(args.key)
        return f"Number of fields in hash '{args.key}': {result}"
    except Exception as e:
        return f"Error getting hash length: {e}"


@server.tool("hash_increment")
def hash_increment(args: HashIncrementArgs, context: RedisContext) -> str:
    """Increment the number value of a field in a hash."""
    try:
        result = context.redis.hincrbyfloat(args.key, args.field, args.amount)
        return f"Incremented field '{args.field}' in hash '{args.key}' by {args.amount}. New value: {result}"
    except Exception as e:
        return f"Error incrementing hash field: {e}"
