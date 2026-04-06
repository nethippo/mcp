# Redis MCP Server

> **Note**: This software is a fork of the AWS MCP server project, refactored and specialized for Redis 8. It has been completely restructured to remove all AWS dependencies and focus exclusively on Redis operations.

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

## uvx Registration

This project can be published to Astral `uvx` so users can install it directly with `uvx`.

1. Choose a uvx package name, for example `yourorg.redis-mcp-server`.
2. Confirm `pyproject.toml` contains the project metadata and entry point:
   - `name = "redis-mcp-server"`
   - `project.scripts` includes `"redis-mcp-server" = "redis_mcp_server.main:main"`
3. Publish the package to `uvx` using your Astral account and workflow.
   - Example: `uvx publish --name yourorg.redis-mcp-server --source .`
4. After publishing, install it through `uvx`:

```bash
uvx yourorg.redis-mcp-server@latest
```

### uvx in Claude Desktop

Once the package is registered in `uvx`, use this configuration in Claude Desktop:

```json
{
  "mcpServers": {
    "redis": {
      "command": "uvx",
      "args": [
        "yourorg.redis-mcp-server@latest"
      ],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "REDIS_READONLY": "false"
      }
    }
  }
}
```

## Claude Desktop Integration

You can integrate this Redis MCP server with Claude Desktop to use Redis operations directly in your conversations.

### Quick Setup (Recommended)

1. **Install Claude Desktop** from [Anthropic's website](https://docs.anthropic.com/claude/docs/desktop)

2. **Create MCP Configuration File**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. **Install the Redis MCP Server** from git and add to your configuration:

```bash
# Install from git repository
uv pip install git+https://github.com/your-username/redis-mcp-server.git
```

4. **Add the Redis MCP Server** to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "redis": {
      "command": "redis-mcp-server",
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "REDIS_READONLY": "false"
      }
    }
  }
}
```

**Replace `your-username` with your actual GitHub username or organization name.**

### Alternative: Direct Execution (Development)

For development or testing, you can run directly from the git repository:

```bash
# Clone the repository
git clone https://github.com/your-username/redis-mcp-server.git
cd redis-mcp-server

# Install dependencies
uv sync
```

Then use this configuration:

```json
{
  "mcpServers": {
    "redis": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/your/local/redis-mcp-server",
        "redis-mcp-server"
      ],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "REDIS_READONLY": "false"
      }
    }
  }
}
```

Replace `/path/to/your/redis-mcp-server` with the actual path to your cloned repository.

### Configuration Options

You can customize the Redis connection through environment variables:

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis server hostname |
| `REDIS_PORT` | `6379` | Redis server port |
| `REDIS_DB` | `0` | Redis database number |
| `REDIS_PASSWORD` | (none) | Redis password (if required) |
| `REDIS_READONLY` | `false` | Enable readonly mode |

### Example Configurations

**Basic Local Redis**:
```json
{
  "mcpServers": {
    "redis": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/redis-mcp-server", "redis-mcp-server"]
    }
  }
}
```

**Remote Redis with Authentication**:
```json
{
  "mcpServers": {
    "redis": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/redis-mcp-server", "redis-mcp-server"],
      "env": {
        "REDIS_HOST": "redis.example.com",
        "REDIS_PORT": "6379",
        "REDIS_PASSWORD": "your-password",
        "REDIS_DB": "1"
      }
    }
  }
}
```

**Readonly Mode for Safe Operations**:
```json
{
  "mcpServers": {
    "redis": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/redis-mcp-server", "redis-mcp-server"],
      "env": {
        "REDIS_READONLY": "true"
      }
    }
  }
}
```

### Testing the Integration

1. Save the configuration file
2. Restart Claude Desktop
3. Start a new conversation
4. You should see Redis tools available in the tool picker

### Troubleshooting

- **Server won't start**: Ensure `uv` is installed and the project path is correct
- **Connection failed**: Check Redis server is running and credentials are correct
- **Tools not appearing**: Restart Claude Desktop after configuration changes
- **Permission issues**: Ensure Claude Desktop has access to the project directory

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