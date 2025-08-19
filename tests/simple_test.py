#!/usr/bin/env python3
"""
Simple test for Freqtrade MCP Server
====================================

This script provides a simple way to test the MCP server functionality
without complex MCP client setup.
"""

import subprocess
import time
import sys


def test_server_startup():
    """Test if server can start and show help"""
    print("\n1️⃣ Testing server startup...")
    try:
        result = subprocess.run(
            ["python", "start_server.py", "--config"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode == 0:
            print("✅ Server configuration test passed")
            print("   Output:", result.stdout.strip())
            return True

        print("❌ Server configuration test failed")
        print("   Error:", result.stderr.strip())
        return False

    except subprocess.TimeoutExpired:
        print("❌ Server startup timed out")
        return False
    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Server startup test failed: {e}")
        return False


def test_main_server():
    """Test if main server can start briefly"""
    print("\n2️⃣ Testing main server startup...")
    try:
        # Start server in background
        with subprocess.Popen(
            ["python", "start_server.py", "--demo"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:

            # Give it a moment to start
            time.sleep(3)

            # Check if it's still running
            if process.poll() is None:
                print("✅ Main server started successfully")
                # Terminate it
                process.terminate()
                process.wait(timeout=5)
                return True

            print("❌ Main server failed to start")
            stdout, stderr = process.communicate()
            print("   Stdout:", stdout.strip())
            print("   Stderr:", stderr.strip())
            return False

    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Main server test failed: {e}")
        return False


def test_mcp_server():
    """Test the MCP server by running it and checking output"""
    print("🧪 Testing Freqtrade MCP Server...")

    # Test 1: Check if server can start and show help
    if not test_server_startup():
        return False

    # Test 2: Check if main server can start (briefly)
    if not test_main_server():
        return False

    print("\n🎉 All tests passed!")
    return True


def show_usage():
    """Show usage information"""
    print("\n📖 Freqtrade MCP Server Usage:")
    print("=" * 50)
    print("1. Start server in demo mode:")
    print("   python start_server.py --demo")
    print()
    print("2. Start server in HTTP mode:")
    print("   python start_server.py --transport streamable-http --port 8005")
    print()
    print("3. Show configuration:")
    print("   python start_server.py --config")
    print()
    print("4. Test server functionality:")
    print("   python simple_test.py")
    print()
    print("5. For MCP client integration:")
    print("   Use the server with stdio transport in your MCP client config")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_usage()
    else:
        test_success = test_mcp_server()
        if not test_success:
            print("\n❌ Some tests failed!")
            sys.exit(1)
        else:
            print("\n✅ Server is ready for use!")
            show_usage()


if __name__ == "__main__":
    main()
