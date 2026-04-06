# Redis MCP Server

A standalone Model Context Protocol (MCP) server for Redis 8, providing comprehensive Redis operations through MCP tools.

## Features

This MCP server provides tools to operate on all major Redis data types and advanced features. It was restructured from the Valkey MCP server to be a standalone Redis implementation without AWS dependencies.

### Supported Data Types

- **Strings** - Store, retrieve, append, increment, decrement operations
  - `string_set`, `string_get`, `string_append`, `string_increment`

- **Lists** - Manage ordered collections with push/pop operations
  - `list_push`, `list_pop`, `list_range`, `list_length`, `list_trim`, `list_set`, `list_remove`

- **Sets** - Store unique elements with set operations
  - `set_add`, `set_remove`, `set_members`, `set_is_member`, `set_length`, `set_random_member`, `set_pop`, `set_union`, `set_intersection`, `set_difference`

- **Sorted Sets** - Store ordered unique elements with scores
  - `sorted_set_add`, `sorted_set_remove`, `sorted_set_score`, `sorted_set_rank`, `sorted_set_range`, `sorted_set_range_by_score`, `sorted_set_length`, `sorted_set_increment`

- **Hashes** - Store field-value pairs
  - `hash_set`, `hash_get`, `hash_get_all`, `hash_exists`, `hash_delete`, `hash_keys`, `hash_values`, `hash_length`, `hash_increment`

- **Streams** - Log data structure with consumer groups
  - `stream_add`, `stream_read`, `stream_range`, `stream_trim`, `stream_length`, `stream_delete`

- **Bitmaps** - Bitwise operations on strings
  - `bitmap_set`, `bitmap_get`, `bitmap_count`, `bitmap_and`, `bitmap_or`, `bitmap_xor`, `bitmap_not`

- **HyperLogLog** - Probabilistic cardinality estimation
  - `hyperloglog_add`, `hyperloglog_count`, `hyperloglog_merge`

- **JSON** - Store and manipulate JSON documents
  - `json_set`, `json_get`, `json_delete`, `json_type`, `json_array_append`

### Advanced Features

- **Search** - Full-text search and indexing (requires RediSearch module)
  - `search_create_index`, `search_query`, `search_drop_index`

- **Functions** - Server-side scripting with Redis Functions (Redis 7.0+)
  - `function_load`, `function_call`, `function_list`

- **Redis 8 Support** - Compatible with Redis 8 features and optimizations
- **Readonly Mode** - Prevent write operations for data safety
- **Health Check** - Built-in `/health` endpoint for monitoring

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
2. Install Python using `uv python install 3.10`
3. Access to a Redis 8 server (Redis 5.0+ minimum, Redis 7.0+ for Functions, Redis 8 recommended)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd redis-mcp-server

# Install dependencies
uv sync

# Install the package in development mode
uv pip install -e .
```

## Usage

### Basic Usage

```bash
# Start the server with default settings (localhost:6379)
redis-mcp-server

# Connect to a specific Redis instance
redis-mcp-server --host redis.example.com --port 6379 --password mypassword --db 1
```

### Readonly Mode

For safe operations that prevent any data modifications:

```bash
redis-mcp-server --readonly
```

### Health Check

The server provides a health check endpoint:

```bash
curl http://localhost:3000/health
```

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `localhost` | Redis server hostname |
| `--port` | `6379` | Redis server port |
| `--password` | `None` | Redis authentication password |
| `--db` | `0` | Redis database number |
| `--readonly` | `False` | Enable readonly mode |

## Architecture

The server is built using:

- **FastMCP** - Modern MCP server framework
- **Redis Python Client** - Official Redis client library
- **Pydantic** - Data validation and serialization
- **Loguru** - Structured logging

### Project Structure

```
redis-mcp-server/
├── redis_mcp_server/
│   ├── main.py              # CLI entry point and server initialization
│   ├── context.py           # Redis connection management
│   ├── common/
│   │   └── server.py        # MCP server configuration
│   └── tools/               # Redis operation tools
│       ├── string.py        # String operations
│       ├── list.py          # List operations
│       ├── hash.py          # Hash operations
│       ├── set.py           # Set operations
│       ├── sorted_set.py    # Sorted set operations
│       ├── bitmap.py        # Bitmap operations
│       ├── stream.py        # Stream operations
│       ├── json.py          # JSON operations
│       ├── hyperloglog.py   # HyperLogLog operations
│       ├── search.py        # Search operations
│       └── functions.py     # Function operations
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Development Status

This implementation provides comprehensive Redis operations through MCP tools. The server has been restructured from the original Valkey MCP server to be a standalone Redis implementation.

### Current Implementation Status

- ✅ **Strings** - Fully implemented
- ✅ **Bitmaps** - Fully implemented
- ✅ **Lists** - Structure ready, implementation complete
- ✅ **Sets** - Structure ready, implementation complete
- ✅ **Sorted Sets** - Structure ready, implementation complete
- ✅ **Hashes** - Structure ready, implementation complete
- ✅ **Streams** - Structure ready, implementation complete
- ✅ **HyperLogLog** - Structure ready, implementation complete
- ✅ **JSON** - Basic implementation (RedisJSON module recommended for full features)
- ⚠️ **Search** - Structure ready, requires RediSearch module
- ⚠️ **Functions** - Structure ready, requires Redis 7.0+

### Notes

- Search and Functions tools require additional Redis modules to be fully functional
- JSON operations use basic string storage; RedisJSON module provides enhanced JSON support
- All tools include proper error handling and type validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.