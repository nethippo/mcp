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

"""Basic tests for Redis MCP Server."""

from redis_mcp_server.common.server import server
from redis_mcp_server.context import RedisContext
from redis_mcp_server.main import main
from unittest.mock import Mock, patch


class TestRedisContext:
    """Test RedisContext functionality."""

    def test_context_initialization(self):
        """Test that RedisContext can be initialized."""
        with patch('redis.Redis') as mock_redis:
            RedisContext.initialize(host='localhost', port=6379, db=0)
            mock_redis.assert_called_once_with(
                host='localhost',
                port=6379,
                password=None,
                db=0,
                decode_responses=True
            )

    def test_get_redis_client(self):
        """Test getting Redis client instance."""
        with patch('redis.Redis') as mock_redis:
            RedisContext.initialize()
            client = RedisContext.get_redis_client()
            assert client is not None
            mock_redis.assert_called_once()


class TestServerInitialization:
    """Test server initialization and basic functionality."""

    def test_server_import(self):
        """Test that the server can be imported."""
        assert server is not None

    def test_main_function_exists(self):
        """Test that main function exists."""
        assert callable(main)


class TestToolsImport:
    """Test that all tools can be imported."""

    def test_string_tools_import(self):
        """Test string tools can be imported."""
        from redis_mcp_server.tools import string
        assert string is not None

    def test_bitmap_tools_import(self):
        """Test bitmap tools can be imported."""
        from redis_mcp_server.tools import bitmap
        assert bitmap is not None

    def test_tools_init_import(self):
        """Test tools __init__.py can be imported."""
        from redis_mcp_server import tools
        assert tools is not None


class TestStringTools:
    """Test string tool functionality."""

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_set_success(self, mock_get_client):
        """Test successful string set operation."""
        mock_client = Mock()
        mock_client.set.return_value = True
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringSetArgs, string_set

        args = StringSetArgs(key="test_key", value="test_value")
        result = string_set(args)

        assert "Set key 'test_key' to 'test_value': True" in result
        mock_client.set.assert_called_once_with("test_key", "test_value", ex=None, px=None, nx=False, xx=False)

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_get_success(self, mock_get_client):
        """Test successful string get operation."""
        mock_client = Mock()
        mock_client.get.return_value = b"test_value"
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringGetArgs, string_get

        args = StringGetArgs(key="test_key")
        result = string_get(args)

        assert "Value of key 'test_key': test_value" in result
        mock_client.get.assert_called_once_with("test_key")

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_get_none(self, mock_get_client):
        """Test string get when key doesn't exist."""
        mock_client = Mock()
        mock_client.get.return_value = None
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringGetArgs, string_get

        args = StringGetArgs(key="nonexistent_key")
        result = string_get(args)

        assert "Key 'nonexistent_key' does not exist" in result

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_append_success(self, mock_get_client):
        """Test successful string append operation."""
        mock_client = Mock()
        mock_client.append.return_value = 10
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringAppendArgs, string_append

        args = StringAppendArgs(key="test_key", value="test_value")
        result = string_append(args)

        assert "Appended to key 'test_key', new length: 10" in result
        mock_client.append.assert_called_once_with("test_key", "test_value")

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_increment_success(self, mock_get_client):
        """Test successful string increment operation."""
        mock_client = Mock()
        mock_client.incrbyfloat.return_value = 5.5
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringIncrementArgs, string_increment

        args = StringIncrementArgs(key="test_key", amount=2.5)
        result = string_increment(args)

        assert "Incremented key 'test_key' by 2.5, new value: 5.5" in result
        mock_client.incrbyfloat.assert_called_once_with("test_key", 2.5)


class TestBitmapTools:
    """Test bitmap tool functionality."""

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_bitmap_set_success(self, mock_get_client):
        """Test successful bitmap set operation."""
        mock_client = Mock()
        mock_client.setbit.return_value = 0
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.bitmap import BitmapSetArgs, bitmap_set

        args = BitmapSetArgs(key="test_bitmap", offsets=[0, 1], values=[1, 0])
        result = bitmap_set(args)

        assert "Set bits in bitmap 'test_bitmap'" in result
        assert mock_client.setbit.call_count == 2

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_bitmap_get_success(self, mock_get_client):
        """Test successful bitmap get operation."""
        mock_client = Mock()
        mock_client.getbit.return_value = 1
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.bitmap import BitmapGetArgs, bitmap_get

        args = BitmapGetArgs(key="test_bitmap", offset=5)
        result = bitmap_get(args)

        assert "Bit at offset 5 in bitmap 'test_bitmap': 1" in result
        mock_client.getbit.assert_called_once_with("test_bitmap", 5)

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_bitmap_count_success(self, mock_get_client):
        """Test successful bitmap count operation."""
        mock_client = Mock()
        mock_client.bitcount.return_value = 42
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.bitmap import BitmapCountArgs, bitmap_count

        args = BitmapCountArgs(key="test_bitmap")
        result = bitmap_count(args)

        assert "Number of set bits in bitmap 'test_bitmap' (bytes 0 to -1): 42" in result
        mock_client.bitcount.assert_called_once_with("test_bitmap", 0, -1)


class TestErrorHandling:
    """Test error handling in tools."""

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_string_set_error(self, mock_get_client):
        """Test error handling in string set."""
        mock_client = Mock()
        mock_client.set.side_effect = Exception("Redis connection error")
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.string import StringSetArgs, string_set

        args = StringSetArgs(key="test_key", value="test_value")
        result = string_set(args)

        assert "Error setting string: Redis connection error" in result

    @patch('redis_mcp_server.context.RedisContext.get_redis_client')
    def test_bitmap_set_error(self, mock_get_client):
        """Test error handling in bitmap set."""
        mock_client = Mock()
        mock_client.setbit.side_effect = Exception("Redis connection error")
        mock_get_client.return_value = mock_client

        from redis_mcp_server.tools.bitmap import BitmapSetArgs, bitmap_set

        args = BitmapSetArgs(key="test_bitmap", offsets=[0], values=[1])
        result = bitmap_set(args)

        assert "Error setting bitmap bits: Redis connection error" in result
