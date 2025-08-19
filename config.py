"""
Configuration for Freqtrade MCP Server
=====================================

This module provides configuration management for the Freqtrade MCP server,
including environment variable handling and default values.
"""

import os
from dataclasses import dataclass


@dataclass
class FreqtradeMCPConfig:
    """Configuration class for Freqtrade MCP Server"""

    # Freqtrade API Configuration
    api_url: str = None
    username: str = None
    password: str = None

    # MCP Server Configuration
    server_name: str = None
    server_version: str = None

    # Transport Configuration
    transport: str = None
    host: str = None
    port: int = None

    # Logging Configuration
    log_level: str = None
    log_dir: str = None

    def __post_init__(self):
        """Initialize configuration from environment variables"""
        # Freqtrade API Configuration
        self.api_url = os.getenv("FREQTRADE_API_URL", "http://127.0.0.1:8080")
        self.username = os.getenv("FREQTRADE_USERNAME", "Freqtrader")
        self.password = os.getenv("FREQTRADE_PASSWORD", "SuperSecret1!")

        # MCP Server Configuration
        self.server_name = os.getenv("MCP_SERVER_NAME", "FreqtradeMCP")
        self.server_version = os.getenv("MCP_SERVER_VERSION", "0.1.0")

        # Transport Configuration
        self.transport = os.getenv("MCP_TRANSPORT", "stdio")  # stdio or streamable-http
        self.host = os.getenv("MCP_HOST", "localhost")
        self.port = int(os.getenv("MCP_PORT", "8005"))

        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_dir = os.getenv("LOG_DIR")

    def get_freqtrade_env(self) -> dict:
        """Get environment variables for Freqtrade client"""
        return {
            "FREQTRADE_API_URL": self.api_url,
            "FREQTRADE_USERNAME": self.username,
            "FREQTRADE_PASSWORD": self.password,
        }

    def get_mcp_env(self) -> dict:
        """Get environment variables for MCP server"""
        return {
            "MCP_SERVER_NAME": self.server_name,
            "MCP_SERVER_VERSION": self.server_version,
            "MCP_TRANSPORT": self.transport,
            "MCP_HOST": self.host,
            "MCP_PORT": str(self.port),
        }

    def print_config(self):
        """Print current configuration"""
        print("🔧 Freqtrade MCP Server Configuration:")
        print(f"   Server: {self.server_name} v{self.server_version}")
        print(f"   Transport: {self.transport}")
        if self.transport == "streamable-http":
            print(f"   HTTP: {self.host}:{self.port}")
        print(f"   Freqtrade API: {self.api_url}")
        print(f"   Username: {self.username}")

        print(f"   Log Level: {self.log_level}")


# Global configuration instance
config = FreqtradeMCPConfig()
