"""HyperLogLog tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import List


class HyperLogLogAddArgs(BaseModel):
    """Arguments for hyperloglog_add tool."""
    key: str = Field(..., description="The key of the HyperLogLog")
    elements: List[str] = Field(..., description="The elements to add")


class HyperLogLogCountArgs(BaseModel):
    """Arguments for hyperloglog_count tool."""
    keys: List[str] = Field(..., description="The keys of the HyperLogLogs to count")


class HyperLogLogMergeArgs(BaseModel):
    """Arguments for hyperloglog_merge tool."""
    dest_key: str = Field(..., description="The destination key for the merged HyperLogLog")
    source_keys: List[str] = Field(..., description="The source keys to merge")


@server.tool("hyperloglog_add")
def hyperloglog_add(args: HyperLogLogAddArgs, context: RedisContext) -> str:
    """Add elements to a HyperLogLog."""
    try:
        result = context.redis.pfadd(args.key, *args.elements)
        return f"Added elements to HyperLogLog '{args.key}'. Changed: {bool(result)}"
    except Exception as e:
        return f"Error adding to HyperLogLog: {e}"


@server.tool("hyperloglog_count")
def hyperloglog_count(args: HyperLogLogCountArgs, context: RedisContext) -> str:
    """Get the approximated cardinality of one or more HyperLogLogs."""
    try:
        result = context.redis.pfcount(*args.keys)
        return f"Approximated cardinality of HyperLogLog(s) {args.keys}: {result}"
    except Exception as e:
        return f"Error counting HyperLogLog: {e}"


@server.tool("hyperloglog_merge")
def hyperloglog_merge(args: HyperLogLogMergeArgs, context: RedisContext) -> str:
    """Merge multiple HyperLogLogs into a single one."""
    try:
        result = context.redis.pfmerge(args.dest_key, *args.source_keys)
        return f"Merged HyperLogLogs {args.source_keys} into '{args.dest_key}': {result}"
    except Exception as e:
        return f"Error merging HyperLogLogs: {e}"
