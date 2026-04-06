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

"""Context management for Redis MCP Server."""

import redis


class RedisContext:
    """Context class for Redis MCP Server."""

    _host = 'localhost'
    _port = 6379
    _password = None
    _db = 0
    _readonly = False
    _redis_client = None

    @classmethod
    def initialize(cls, host='localhost', port=6379, password=None, db=0, readonly=False):
        """Initialize the context.

        Args:
            host: Redis host
            port: Redis port
            password: Redis password
            db: Redis database
            readonly: Whether to run in readonly mode
        """
        cls._host = host
        cls._port = port
        cls._password = password
        cls._db = db
        cls._readonly = readonly

        # Initialize Redis client
        cls._redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True
        )

    @classmethod
    def get_redis_client(cls):
        """Get Redis client instance."""
        if cls._redis_client is None:
            cls.initialize()
        return cls._redis_client

    @classmethod
    def readonly_mode(cls) -> bool:
        """Check if the server is running in readonly mode.

        Returns:
            True if readonly mode is enabled, False otherwise
        """
        return cls._readonly
