"""Set tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import List, Optional


class SetAddArgs(BaseModel):
    """Arguments for set_add tool."""
    key: str = Field(..., description="The key of the set")
    members: List[str] = Field(..., description="The members to add to the set")


class SetRemoveArgs(BaseModel):
    """Arguments for set_remove tool."""
    key: str = Field(..., description="The key of the set")
    members: List[str] = Field(..., description="The members to remove from the set")


class SetMembersArgs(BaseModel):
    """Arguments for set_members tool."""
    key: str = Field(..., description="The key of the set")


class SetIsMemberArgs(BaseModel):
    """Arguments for set_is_member tool."""
    key: str = Field(..., description="The key of the set")
    member: str = Field(..., description="The member to check")


class SetLengthArgs(BaseModel):
    """Arguments for set_length tool."""
    key: str = Field(..., description="The key of the set")


class SetRandomMemberArgs(BaseModel):
    """Arguments for set_random_member tool."""
    key: str = Field(..., description="The key of the set")
    count: Optional[int] = Field(1, description="The number of random members to return")


class SetPopArgs(BaseModel):
    """Arguments for set_pop tool."""
    key: str = Field(..., description="The key of the set")
    count: Optional[int] = Field(1, description="The number of members to pop")


class SetUnionArgs(BaseModel):
    """Arguments for set_union tool."""
    keys: List[str] = Field(..., description="The keys of the sets to union")


class SetIntersectionArgs(BaseModel):
    """Arguments for set_intersection tool."""
    keys: List[str] = Field(..., description="The keys of the sets to intersect")


class SetDifferenceArgs(BaseModel):
    """Arguments for set_difference tool."""
    keys: List[str] = Field(..., description="The keys of the sets (first minus others)")


@server.tool("set_add")
def set_add(args: SetAddArgs, context: RedisContext) -> str:
    """Add one or more members to a set."""
    try:
        result = context.redis.sadd(args.key, *args.members)
        return f"Added {result} members to set '{args.key}'"
    except Exception as e:
        return f"Error adding to set: {e}"


@server.tool("set_remove")
def set_remove(args: SetRemoveArgs, context: RedisContext) -> str:
    """Remove one or more members from a set."""
    try:
        result = context.redis.srem(args.key, *args.members)
        return f"Removed {result} members from set '{args.key}'"
    except Exception as e:
        return f"Error removing from set: {e}"


@server.tool("set_members")
def set_members(args: SetMembersArgs, context: RedisContext) -> str:
    """Get all members of a set."""
    try:
        result = context.redis.smembers(args.key)
        decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        return f"Members of set '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting set members: {e}"


@server.tool("set_is_member")
def set_is_member(args: SetIsMemberArgs, context: RedisContext) -> str:
    """Check if a member exists in a set."""
    try:
        result = context.redis.sismember(args.key, args.member)
        return f"Member '{args.member}' exists in set '{args.key}': {bool(result)}"
    except Exception as e:
        return f"Error checking set membership: {e}"


@server.tool("set_length")
def set_length(args: SetLengthArgs, context: RedisContext) -> str:
    """Get the number of members in a set."""
    try:
        result = context.redis.scard(args.key)
        return f"Number of members in set '{args.key}': {result}"
    except Exception as e:
        return f"Error getting set length: {e}"


@server.tool("set_random_member")
def set_random_member(args: SetRandomMemberArgs, context: RedisContext) -> str:
    """Get one or more random members from a set."""
    try:
        result = context.redis.srandmember(args.key, args.count)
        if isinstance(result, list):
            decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        else:
            decoded_result = result.decode('utf-8') if isinstance(result, bytes) else result
        return f"Random member(s) from set '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting random set member: {e}"


@server.tool("set_pop")
def set_pop(args: SetPopArgs, context: RedisContext) -> str:
    """Remove and return one or more random members from a set."""
    try:
        result = context.redis.spop(args.key, args.count)
        if isinstance(result, set):
            decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        else:
            decoded_result = result.decode('utf-8') if isinstance(result, bytes) else result
        return f"Popped member(s) from set '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error popping from set: {e}"


@server.tool("set_union")
def set_union(args: SetUnionArgs, context: RedisContext) -> str:
    """Get the union of multiple sets."""
    try:
        result = context.redis.sunion(*args.keys)
        decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        return f"Union of sets {args.keys}: {decoded_result}"
    except Exception as e:
        return f"Error getting set union: {e}"


@server.tool("set_intersection")
def set_intersection(args: SetIntersectionArgs, context: RedisContext) -> str:
    """Get the intersection of multiple sets."""
    try:
        result = context.redis.sinter(*args.keys)
        decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        return f"Intersection of sets {args.keys}: {decoded_result}"
    except Exception as e:
        return f"Error getting set intersection: {e}"


@server.tool("set_difference")
def set_difference(args: SetDifferenceArgs, context: RedisContext) -> str:
    """Get the difference of multiple sets (first minus others)."""
    try:
        result = context.redis.sdiff(*args.keys)
        decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        return f"Difference of sets {args.keys}: {decoded_result}"
    except Exception as e:
        return f"Error getting set difference: {e}"
