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

"""String tools for Redis MCP Server."""

from ..common.server import server
from ..context import RedisContext
from pydantic import BaseModel, Field
from typing import Any, Optional


class StringSetArgs(BaseModel):
    """Arguments for string_set tool."""
    key: str = Field(..., description="The key to set")
    value: Any = Field(..., description="The value to set")
    ex: Optional[int] = Field(None, description="Set the specified expire time, in seconds")
    px: Optional[int] = Field(None, description="Set the specified expire time, in milliseconds")
    nx: bool = Field(False, description="Only set the key if it does not already exist")
    xx: bool = Field(False, description="Only set the key if it already exists")


class StringGetArgs(BaseModel):
    """Arguments for string_get tool."""
    key: str = Field(..., description="The key to get")


class StringAppendArgs(BaseModel):
    """Arguments for string_append tool."""
    key: str = Field(..., description="The key to append to")
    value: str = Field(..., description="The value to append")


class StringIncrementArgs(BaseModel):
    """Arguments for string_increment tool."""
    key: str = Field(..., description="The key to increment")
    amount: float = Field(1.0, description="The amount to increment by")


@server.tool("string_set")
def string_set(args: StringSetArgs) -> str:
    """Set the value of a key."""
    try:
        result = RedisContext.get_redis_client().set(args.key, args.value, ex=args.ex, px=args.px, nx=args.nx, xx=args.xx)
        return f"Set key '{args.key}' to '{args.value}': {result}"
    except Exception as e:
        return f"Error setting string: {e}"


@server.tool("string_get")
def string_get(args: StringGetArgs) -> str:
    """Get the value of a key."""
    try:
        result = RedisContext.get_redis_client().get(args.key)
        if result is None:
            return f"Key '{args.key}' does not exist"
        return f"Value of key '{args.key}': {result.decode('utf-8') if isinstance(result, bytes) else result}"
    except Exception as e:
        return f"Error getting string: {e}"


@server.tool("string_append")
def string_append(args: StringAppendArgs) -> str:
    """Append a value to a key."""
    try:
        result = RedisContext.get_redis_client().append(args.key, args.value)
        return f"Appended to key '{args.key}', new length: {result}"
    except Exception as e:
        return f"Error appending to string: {e}"


@server.tool("string_increment")
def string_increment(args: StringIncrementArgs) -> str:
    """Increment the number value stored at key."""
    try:
        result = RedisContext.get_redis_client().incrbyfloat(args.key, args.amount)
        return f"Incremented key '{args.key}' by {args.amount}, new value: {result}"
    except Exception as e:
        return f"Error incrementing string: {e}"
