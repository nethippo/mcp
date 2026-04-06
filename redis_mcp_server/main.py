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

"""Redis MCP Server implementation."""

import argparse
from redis_mcp_server.common.server import server
from redis_mcp_server.context import RedisContext
from starlette.responses import Response


# Add a health check route directly to the MCP server
@server.custom_route('/health', methods=['GET'])
async def health_check(request):
    """Simple health check endpoint.

    Always returns 200 OK to indicate the service is running.
    """
    return Response(content='healthy', status_code=200, media_type='text/plain')


class RedisMCPServer:
    """Redis MCP Server wrapper."""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Redis MCP Server')
    parser.add_argument('--host', default='localhost', help='Redis host')
    parser.add_argument('--port', type=int, default=6379, help='Redis port')
    parser.add_argument('--password', help='Redis password')
    parser.add_argument('--db', type=int, default=0, help='Redis database')
    parser.add_argument('--readonly', action='store_true', help='Run in readonly mode')

    args = parser.parse_args()

    # Initialize context
    RedisContext.initialize(
        host=args.host,
        port=args.port,
        password=args.password,
        db=args.db,
        readonly=args.readonly
    )

    # Run the MCP server
    server.run()


if __name__ == '__main__':
    main()
