"""Sorted Set tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import List, Tuple


class SortedSetAddArgs(BaseModel):
    """Arguments for sorted_set_add tool."""
    key: str = Field(..., description="The key of the sorted set")
    members_scores: List[Tuple[str, float]] = Field(..., description="List of (member, score) tuples to add")


class SortedSetRemoveArgs(BaseModel):
    """Arguments for sorted_set_remove tool."""
    key: str = Field(..., description="The key of the sorted set")
    members: List[str] = Field(..., description="The members to remove")


class SortedSetScoreArgs(BaseModel):
    """Arguments for sorted_set_score tool."""
    key: str = Field(..., description="The key of the sorted set")
    member: str = Field(..., description="The member to get the score for")


class SortedSetRankArgs(BaseModel):
    """Arguments for sorted_set_rank tool."""
    key: str = Field(..., description="The key of the sorted set")
    member: str = Field(..., description="The member to get the rank for")
    reverse: bool = Field(False, description="If true, get rank from highest to lowest score")


class SortedSetRangeArgs(BaseModel):
    """Arguments for sorted_set_range tool."""
    key: str = Field(..., description="The key of the sorted set")
    start: int = Field(..., description="Start index (0-based)")
    end: int = Field(..., description="End index (-1 for all)")
    with_scores: bool = Field(True, description="Include scores in the result")
    reverse: bool = Field(False, description="If true, return in reverse order")


class SortedSetRangeByScoreArgs(BaseModel):
    """Arguments for sorted_set_range_by_score tool."""
    key: str = Field(..., description="The key of the sorted set")
    min_score: float = Field(..., description="Minimum score")
    max_score: float = Field(..., description="Maximum score")


class SortedSetLengthArgs(BaseModel):
    """Arguments for sorted_set_length tool."""
    key: str = Field(..., description="The key of the sorted set")


class SortedSetIncrementArgs(BaseModel):
    """Arguments for sorted_set_increment tool."""
    key: str = Field(..., description="The key of the sorted set")
    member: str = Field(..., description="The member to increment")
    amount: float = Field(1.0, description="The amount to increment the score by")


@server.tool("sorted_set_add")
def sorted_set_add(args: SortedSetAddArgs, context: RedisContext) -> str:
    """Add one or more members with scores to a sorted set."""
    try:
        # Convert tuples to alternating member, score format
        members_scores = []
        for member, score in args.members_scores:
            members_scores.extend([score, member])
        result = context.redis.zadd(args.key, *members_scores)
        return f"Added {result} members to sorted set '{args.key}'"
    except Exception as e:
        return f"Error adding to sorted set: {e}"


@server.tool("sorted_set_remove")
def sorted_set_remove(args: SortedSetRemoveArgs, context: RedisContext) -> str:
    """Remove one or more members from a sorted set."""
    try:
        result = context.redis.zrem(args.key, *args.members)
        return f"Removed {result} members from sorted set '{args.key}'"
    except Exception as e:
        return f"Error removing from sorted set: {e}"


@server.tool("sorted_set_score")
def sorted_set_score(args: SortedSetScoreArgs, context: RedisContext) -> str:
    """Get the score of a member in a sorted set."""
    try:
        result = context.redis.zscore(args.key, args.member)
        if result is None:
            return f"Member '{args.member}' does not exist in sorted set '{args.key}'"
        return f"Score of member '{args.member}' in sorted set '{args.key}': {result}"
    except Exception as e:
        return f"Error getting sorted set score: {e}"


@server.tool("sorted_set_rank")
def sorted_set_rank(args: SortedSetRankArgs, context: RedisContext) -> str:
    """Get the rank of a member in a sorted set."""
    try:
        if args.reverse:
            result = context.redis.zrevrank(args.key, args.member)
        else:
            result = context.redis.zrank(args.key, args.member)
        if result is None:
            return f"Member '{args.member}' does not exist in sorted set '{args.key}'"
        return f"Rank of member '{args.member}' in sorted set '{args.key}': {result}"
    except Exception as e:
        return f"Error getting sorted set rank: {e}"


@server.tool("sorted_set_range")
def sorted_set_range(args: SortedSetRangeArgs, context: RedisContext) -> str:
    """Get a range of members from a sorted set."""
    try:
        if args.reverse:
            if args.with_scores:
                result = context.redis.zrevrange(args.key, args.start, args.end, withscores=True)
            else:
                result = context.redis.zrevrange(args.key, args.start, args.end)
        else:
            if args.with_scores:
                result = context.redis.zrange(args.key, args.start, args.end, withscores=True)
            else:
                result = context.redis.zrange(args.key, args.start, args.end)

        if args.with_scores:
            decoded_result = [(m.decode('utf-8') if isinstance(m, bytes) else m, s) for m, s in result]
        else:
            decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]

        return f"Range [{args.start}:{args.end}] from sorted set '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting sorted set range: {e}"


@server.tool("sorted_set_range_by_score")
def sorted_set_range_by_score(args: SortedSetRangeByScoreArgs, context: RedisContext) -> str:
    """Get members from a sorted set within a score range."""
    try:
        result = context.redis.zrangebyscore(args.key, args.min_score, args.max_score)
        decoded_result = [m.decode('utf-8') if isinstance(m, bytes) else m for m in result]
        return f"Members with scores between {args.min_score} and {args.max_score} in sorted set '{args.key}': {decoded_result}"
    except Exception as e:
        return f"Error getting sorted set range by score: {e}"


@server.tool("sorted_set_length")
def sorted_set_length(args: SortedSetLengthArgs, context: RedisContext) -> str:
    """Get the number of members in a sorted set."""
    try:
        result = context.redis.zcard(args.key)
        return f"Number of members in sorted set '{args.key}': {result}"
    except Exception as e:
        return f"Error getting sorted set length: {e}"


@server.tool("sorted_set_increment")
def sorted_set_increment(args: SortedSetIncrementArgs, context: RedisContext) -> str:
    """Increment the score of a member in a sorted set."""
    try:
        result = context.redis.zincrby(args.key, args.amount, args.member)
        return f"Incremented score of member '{args.member}' in sorted set '{args.key}' by {args.amount}. New score: {result}"
    except Exception as e:
        return f"Error incrementing sorted set score: {e}"
