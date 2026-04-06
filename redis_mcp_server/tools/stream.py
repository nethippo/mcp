"""Stream tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class StreamAddArgs(BaseModel):
    """Arguments for stream_add tool."""
    key: str = Field(..., description="The key of the stream")
    fields: Dict[str, str] = Field(..., description="The fields to add as a new entry")
    id: Optional[str] = Field("*", description="The ID for the new entry (default: auto-generate)")


class StreamReadArgs(BaseModel):
    """Arguments for stream_read tool."""
    key: str = Field(..., description="The key of the stream")
    count: Optional[int] = Field(10, description="Maximum number of entries to read")
    start_id: Optional[str] = Field("0", description="Start reading from this ID")


class StreamRangeArgs(BaseModel):
    """Arguments for stream_range tool."""
    key: str = Field(..., description="The key of the stream")
    start_id: str = Field("-", description="Start ID (inclusive)")
    end_id: str = Field("+", description="End ID (inclusive)")
    count: Optional[int] = Field(None, description="Maximum number of entries to return")


class StreamTrimArgs(BaseModel):
    """Arguments for stream_trim tool."""
    key: str = Field(..., description="The key of the stream")
    max_len: int = Field(..., description="Maximum length to trim to")
    approximate: bool = Field(True, description="Use approximate trimming for better performance")


class StreamLengthArgs(BaseModel):
    """Arguments for stream_length tool."""
    key: str = Field(..., description="The key of the stream")


class StreamDeleteArgs(BaseModel):
    """Arguments for stream_delete tool."""
    key: str = Field(..., description="The key of the stream")
    ids: List[str] = Field(..., description="The IDs of entries to delete")


@server.tool("stream_add")
def stream_add(args: StreamAddArgs, context: RedisContext) -> str:
    """Add a new entry to a stream."""
    try:
        result = context.redis.xadd(args.key, args.fields, id=args.id)
        return f"Added entry with ID '{result}' to stream '{args.key}'"
    except Exception as e:
        return f"Error adding to stream: {e}"


@server.tool("stream_read")
def stream_read(args: StreamReadArgs, context: RedisContext) -> str:
    """Read entries from a stream."""
    try:
        result = context.redis.xread({args.key: args.start_id}, count=args.count)
        if not result:
            return f"No entries found in stream '{args.key}' starting from ID '{args.start_id}'"

        # Decode the result
        decoded_result = []
        for stream_key, entries in result:
            stream_key = stream_key.decode('utf-8') if isinstance(stream_key, bytes) else stream_key
            decoded_entries = []
            for entry_id, fields in entries:
                entry_id = entry_id.decode('utf-8') if isinstance(entry_id, bytes) else entry_id
                decoded_fields = {k.decode('utf-8') if isinstance(k, bytes) else k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in fields.items()}
                decoded_entries.append((entry_id, decoded_fields))
            decoded_result.append((stream_key, decoded_entries))

        return f"Read entries from stream '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error reading from stream: {e}"


@server.tool("stream_range")
def stream_range(args: StreamRangeArgs, context: RedisContext) -> str:
    """Get a range of entries from a stream."""
    try:
        result = context.redis.xrange(args.key, args.start_id, args.end_id, count=args.count)
        if not result:
            return f"No entries found in stream '{args.key}' between IDs '{args.start_id}' and '{args.end_id}'"

        decoded_result = []
        for entry_id, fields in result:
            entry_id = entry_id.decode('utf-8') if isinstance(entry_id, bytes) else entry_id
            decoded_fields = {k.decode('utf-8') if isinstance(k, bytes) else k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in fields.items()}
            decoded_result.append((entry_id, decoded_fields))

        return f"Range of entries from stream '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting stream range: {e}"


@server.tool("stream_trim")
def stream_trim(args: StreamTrimArgs, context: RedisContext) -> str:
    """Trim a stream to a maximum length."""
    try:
        result = context.redis.xtrim(args.key, maxlen=args.max_len, approximate=args.approximate)
        return f"Trimmed stream '{args.key}' to maximum length {args.max_len}. Removed {result} entries."
    except Exception as e:
        return f"Error trimming stream: {e}"


@server.tool("stream_length")
def stream_length(args: StreamLengthArgs, context: RedisContext) -> str:
    """Get the number of entries in a stream."""
    try:
        result = context.redis.xlen(args.key)
        return f"Number of entries in stream '{args.key}': {result}"
    except Exception as e:
        return f"Error getting stream length: {e}"


@server.tool("stream_delete")
def stream_delete(args: StreamDeleteArgs, context: RedisContext) -> str:
    """Delete entries from a stream."""
    try:
        result = context.redis.xdel(args.key, *args.ids)
        return f"Deleted {result} entries from stream '{args.key}'"
    except Exception as e:
        return f"Error deleting from stream: {e}"
