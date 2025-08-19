#!/usr/bin/env python3
"""
Startup script for Freqtrade MCP Server
======================================

This script provides a simple way to start the Freqtrade MCP server
with different transport modes and configurations.
"""
from config import config
import argparse
import importlib.util
import os
import sys


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Start Freqtrade MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default=config.transport,
        help="Transport mode",
    )
    parser.add_argument("--port", type=int, default=config.port, help="Port for HTTP transport")
    parser.add_argument("--host", default=config.host, help="Host for HTTP transport")

    parser.add_argument("--config", action="store_true", help="Show configuration and exit")

    return parser.parse_args()


def update_configuration(args):
    """Update configuration based on command line arguments"""
    config.transport = args.transport
    config.host = args.host
    config.port = args.port


def print_startup_info():
    """Print startup information"""
    print("🚀 Starting Freqtrade MCP Server...")
    config.print_config()

    if config.transport == "streamable-http":
        print(f"🌐 HTTP server will be available at http://{config.host}:{config.port}")
        print("   Use this for integration with other applications")
    else:
        print("📡 Using stdio transport (default for MCP clients)")

    # Trading mode is controlled by Freqtrade's dry_run setting
    print("🎯 Trading mode controlled by Freqtrade configuration")
    print("   Check dry_run setting in freqtrade/user_data/config.json")


def import_mcp_server():
    """Import the MCP server module"""
    # Get the directory where start_server.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(current_dir, "__main__.py")

    spec = importlib.util.spec_from_file_location("freqtrade_mcp", main_py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the mcp instance from the module
    mcp = getattr(module, "mcp")
    return mcp


def start_http_server(mcp_instance):
    """Start the server in HTTP mode"""
    mcp_instance.settings.host = config.host
    mcp_instance.settings.port = config.port
    print(f"\n🔄 Starting HTTP server on {config.host}:{config.port}")
    mcp_instance.run(transport="streamable-http")


def start_stdio_server(mcp_instance):
    """Start the server in stdio mode"""
    print("\n🔄 Starting stdio server")
    mcp_instance.run(transport="stdio")


def main():
    """Main startup function"""
    args = parse_arguments()

    # Update configuration
    update_configuration(args)

    # Show configuration if requested
    if args.config:
        config.print_config()
        return

    # Print startup information
    print_startup_info()

    # Import and run the MCP server
    try:
        mcp_instance = import_mcp_server()

        if config.transport == "streamable-http":
            start_http_server(mcp_instance)
        else:
            start_stdio_server(mcp_instance)

    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
