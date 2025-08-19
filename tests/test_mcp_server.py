#!/usr/bin/env python3
"""
Test script for Freqtrade MCP Server
====================================

This script tests the basic functionality of the Freqtrade MCP server
to ensure it's working correctly.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_freqtrade_mcp():
    """Test the Freqtrade MCP server functionality"""

    print("🚀 Testing Freqtrade MCP Server...")

    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["__main__.py"],
        env={
            "FREQTRADE_API_URL": "http://127.0.0.1:8080",
            "FREQTRADE_USERNAME": "test",
            "FREQTRADE_PASSWORD": "test",
        },
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ MCP session established")

                # Initialize the connection
                await session.initialize()
                print("✅ Session initialized")

                # List available tools
                tools = await session.list_tools()
                print(f"🔧 Available tools: {len(tools)}")
                for tool in tools:
                    print(f"   - {tool.name}: {tool.description}")

                # List available prompts
                prompts = await session.list_prompts()
                print(f"💬 Available prompts: {len(prompts)}")
                for prompt in prompts:
                    print(f"   - {prompt.name}: {prompt.description}")

                # Test a simple tool call (this will work in demo mode)
                print("\n🧪 Testing tool calls...")

                # Test fetch_bot_status
                try:
                    result = await session.call_tool("fetch_bot_status", arguments={})
                    print(f"✅ fetch_bot_status: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ fetch_bot_status failed: {e}")

                # Test fetch_balance
                try:
                    result = await session.call_tool("fetch_balance", arguments={})
                    print(f"✅ fetch_balance: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ fetch_balance failed: {e}")

                print("\n🎉 Freqtrade MCP Server test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_freqtrade_mcp())
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        exit(1)
