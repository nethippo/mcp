"""Bitmap tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import List, Optional


class BitmapSetArgs(BaseModel):
    """Arguments for bitmap_set tool."""
    key: str = Field(..., description="The key of the bitmap")
    offsets: List[int] = Field(..., description="The bit offsets to set")
    values: List[int] = Field(..., description="The bit values (0 or 1) to set")


class BitmapGetArgs(BaseModel):
    """Arguments for bitmap_get tool."""
    key: str = Field(..., description="The key of the bitmap")
    offset: int = Field(..., description="The bit offset to get")


class BitmapCountArgs(BaseModel):
    """Arguments for bitmap_count tool."""
    key: str = Field(..., description="The key of the bitmap")
    start: Optional[int] = Field(0, description="Start byte offset")
    end: Optional[int] = Field(-1, description="End byte offset")


class BitmapAndArgs(BaseModel):
    """Arguments for bitmap_and tool."""
    dest_key: str = Field(..., description="The destination key for the result")
    keys: List[str] = Field(..., description="The keys of the bitmaps to AND")


class BitmapOrArgs(BaseModel):
    """Arguments for bitmap_or tool."""
    dest_key: str = Field(..., description="The destination key for the result")
    keys: List[str] = Field(..., description="The keys of the bitmaps to OR")


class BitmapXorArgs(BaseModel):
    """Arguments for bitmap_xor tool."""
    dest_key: str = Field(..., description="The destination key for the result")
    keys: List[str] = Field(..., description="The keys of the bitmaps to XOR")


class BitmapNotArgs(BaseModel):
    """Arguments for bitmap_not tool."""
    dest_key: str = Field(..., description="The destination key for the result")
    key: str = Field(..., description="The key of the bitmap to NOT")


@server.tool("bitmap_set")
def bitmap_set(args: BitmapSetArgs) -> str:
    """Set bits at specified offsets in a bitmap."""
    try:
        if len(args.offsets) != len(args.values):
            return "Error: offsets and values lists must have the same length"

        results = []
        for offset, value in zip(args.offsets, args.values):
            if value not in (0, 1):
                return f"Error: bit value must be 0 or 1, got {value}"
            result = RedisContext.get_redis_client().setbit(args.key, offset, value)
            results.append(f"offset {offset}: {result}")

        return f"Set bits in bitmap '{args.key}': {', '.join(results)}"
    except Exception as e:
        return f"Error setting bitmap bits: {e}"


@server.tool("bitmap_get")
def bitmap_get(args: BitmapGetArgs) -> str:
    """Get the bit value at a specific offset in a bitmap."""
    try:
        result = RedisContext.get_redis_client().getbit(args.key, args.offset)
        return f"Bit at offset {args.offset} in bitmap '{args.key}': {result}"
    except Exception as e:
        return f"Error getting bitmap bit: {e}"


@server.tool("bitmap_count")
def bitmap_count(args: BitmapCountArgs) -> str:
    """Count the number of set bits (population count) in a bitmap."""
    try:
        result = RedisContext.get_redis_client().bitcount(args.key, args.start, args.end)
        return f"Number of set bits in bitmap '{args.key}' (bytes {args.start} to {args.end}): {result}"
    except Exception as e:
        return f"Error counting bitmap bits: {e}"


@server.tool("bitmap_and")
def bitmap_and(args: BitmapAndArgs) -> str:
    """Perform bitwise AND operation on multiple bitmaps."""
    try:
        result = RedisContext.get_redis_client().bitop('AND', args.dest_key, *args.keys)
        return f"Performed AND operation on bitmaps {args.keys}, result stored in '{args.dest_key}' (length: {result} bytes)"
    except Exception as e:
        return f"Error performing bitmap AND: {e}"


@server.tool("bitmap_or")
def bitmap_or(args: BitmapOrArgs) -> str:
    """Perform bitwise OR operation on multiple bitmaps."""
    try:
        result = RedisContext.get_redis_client().bitop('OR', args.dest_key, *args.keys)
        return f"Performed OR operation on bitmaps {args.keys}, result stored in '{args.dest_key}' (length: {result} bytes)"
    except Exception as e:
        return f"Error performing bitmap OR: {e}"


@server.tool("bitmap_xor")
def bitmap_xor(args: BitmapXorArgs) -> str:
    """Perform bitwise XOR operation on multiple bitmaps."""
    try:
        result = RedisContext.get_redis_client().bitop('XOR', args.dest_key, *args.keys)
        return f"Performed XOR operation on bitmaps {args.keys}, result stored in '{args.dest_key}' (length: {result} bytes)"
    except Exception as e:
        return f"Error performing bitmap XOR: {e}"


@server.tool("bitmap_not")
def bitmap_not(args: BitmapNotArgs) -> str:
    """Perform bitwise NOT operation on a bitmap."""
    try:
        result = RedisContext.get_redis_client().bitop('NOT', args.dest_key, args.key)
        return f"Performed NOT operation on bitmap '{args.key}', result stored in '{args.dest_key}' (length: {result} bytes)"
    except Exception as e:
        return f"Error performing bitmap NOT: {e}"
