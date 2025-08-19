"""
Freqtrade MCP Server

This module provides an MCP (Model Context Protocol) server that integrates
with the Freqtrade cryptocurrency trading bot via its REST API, enabling
seamless AI agent interaction for automated trading operations.

The server provides tools for market data retrieval, trade execution,
bot control, and performance monitoring.
"""

import os
from typing import List, AsyncIterator, Dict, Any
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context

# Import Freqtrade REST client
from freqtrade_client.ft_rest_client import FtRestClient

# Configuration loaded from environment variables
FREQTRADE_API_URL = os.getenv("FREQTRADE_API_URL", "http://127.0.0.1:8080")
USERNAME = os.getenv("FREQTRADE_USERNAME", "Freqtrader")
PASSWORD = os.getenv("FREQTRADE_PASSWORD", "SuperSecret1!")


# Lifecycle management for the Freqtrade client
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:  # pylint: disable=unused-argument
    """Manage the lifecycle of the Freqtrade REST client."""
    try:
        client = FtRestClient(FREQTRADE_API_URL, USERNAME, PASSWORD)
        # Test API connectivity
        if client.ping():
            print("✅ Connected to Freqtrade API")
        else:
            print("⚠️ Failed to connect to Freqtrade API - client will be None")
            client = None
        yield {"client": client}
    except (ConnectionError, TimeoutError) as e:
        print(f"⚠️ Freqtrade connection failed: {e} - client will be None")
        yield {"client": None}
    except Exception as e:  # pylint: disable=broad-except
        print(f"⚠️ Unexpected error during Freqtrade setup: {e} - client will be None")
        yield {"client": None}
    finally:
        print("🔄 Freqtrade API client lifecycle completed")


# Initialize MCP server (only once, with lifespan)
mcp = FastMCP("FreqtradeMCP", dependencies=["freqtrade-client"], lifespan=app_lifespan)


# Tools (Converted from resources and actions)
@mcp.tool()
async def fetch_market_data(pair: str, timeframe: str, ctx: Context) -> str:
    """
    Fetch OHLCV data for a specified trading pair and timeframe.

    Parameters:
        pair (str): Trading pair (e.g., "BTC/USDT").
        timeframe (str): Timeframe for the data (e.g., "1h", "5m").
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response containing OHLCV data, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    await ctx.info(f"Fetching market data for {pair} with timeframe {timeframe}")
    try:
        return str(client.pair_candles(pair=pair, timeframe=timeframe))
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching market data: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch market data: {e}"})


@mcp.tool()
async def fetch_bot_status(ctx: Context) -> str:
    """
    Retrieve the current status of open trades.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with open trade status, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.status())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching bot status: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch bot status: {e}"})


@mcp.tool()
async def fetch_profit(ctx: Context) -> str:
    """
    Get profit summary for the trading bot.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with profit summary, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.profit())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching profit: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch profit: {e}"})


@mcp.tool()
async def fetch_balance(ctx: Context) -> str:
    """
    Fetch the account balance.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with account balance, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.balance())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching balance: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch balance: {e}"})


@mcp.tool()
async def fetch_performance(ctx: Context) -> str:
    """
    Retrieve trading performance metrics.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with performance metrics, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.performance())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching performance: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch performance: {e}"})


@mcp.tool()
async def fetch_whitelist(ctx: Context) -> str:
    """
    Get the current whitelist of trading pairs.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with whitelist data, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.whitelist())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching whitelist: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch whitelist: {e}"})


@mcp.tool()
async def fetch_blacklist(ctx: Context) -> str:
    """
    Get the current blacklist of trading pairs.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with blacklist data, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.blacklist())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching blacklist: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch blacklist: {e}"})


@mcp.tool()
async def fetch_trades(ctx: Context) -> str:
    """
    Fetch the history of closed trades.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with trade history, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.trades())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching trades: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch trades: {e}"})


@mcp.tool()
async def fetch_config(ctx: Context) -> str:
    """
    Retrieve the current bot configuration.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with configuration data, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.config())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching config: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch config: {e}"})


@mcp.tool()
async def fetch_locks(ctx: Context) -> str:
    """
    Get the current trade locks.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with trade locks data, or None if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        return str(client.locks())
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching locks: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to fetch locks: {e}"})


@mcp.tool()
async def place_trade(pair: str, side: str, stake_amount: float, ctx: Context) -> str:
    """
    Place a trade (buy or sell) with the specified pair and amount.

    Parameters:
        pair (str): Trading pair (e.g., "BTC/USDT").
        side (str): Trade direction, either "buy" or "sell".
        stake_amount (float): Amount to trade in the stake currency.
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with trade result, or error message if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    if side.lower() not in ["buy", "sell"]:
        return str({"error": "Side must be 'buy' or 'sell'"})

    try:
        if side.lower() == "buy":
            response = client.forcebuy(pair=pair, stake_amount=stake_amount)
        else:
            response = client.forcesell(pair=pair, amount=stake_amount)
        await ctx.info(f"Trade placed: {side} {stake_amount} of {pair}")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error placing trade: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to place trade: {e}"})


@mcp.tool()
async def start_bot(ctx: Context) -> str:
    """
    Start the Freqtrade bot.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response or success message, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.start_bot()
        await ctx.info("Freqtrade bot started")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error starting bot: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to start bot: {e}"})


@mcp.tool()
async def stop_bot(ctx: Context) -> str:
    """
    Stop the Freqtrade bot.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response or success message, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.stop_bot()
        await ctx.info("Freqtrade bot stopped")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error stopping bot: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to stop bot: {e}"})


@mcp.tool()
async def reload_config(ctx: Context) -> str:
    """
    Reload the bot configuration.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response or success message, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.reload_config()
        await ctx.info("Configuration reloaded")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error reloading config: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to reload config: {e}"})


@mcp.tool()
async def add_blacklist(pair: str, ctx: Context) -> str:
    """
    Add a pair to the blacklist.

    Parameters:
        pair (str): Trading pair to blacklist (e.g., "ETH/USDT").
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with updated blacklist, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.add_blacklist(pair)
        await ctx.info(f"Added {pair} to blacklist")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error adding to blacklist: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to add to blacklist: {e}"})


@mcp.tool()
async def delete_blacklist(pair: str, ctx: Context) -> str:
    """
    Remove a pair from the blacklist.

    Parameters:
        pair (str): Trading pair to remove from blacklist (e.g., "ETH/USDT").
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with updated blacklist, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.delete_blacklist(pair)
        await ctx.info(f"Removed {pair} from blacklist")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error removing from blacklist: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to remove from blacklist: {e}"})


@mcp.tool()
async def delete_lock(lock_id: int, ctx: Context) -> str:
    """
    Delete a specific trade lock by ID.

    Parameters:
        lock_id (int): ID of the trade lock to delete.
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with updated locks, or error if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        response = client.delete_lock(lock_id)
        await ctx.info(f"Deleted lock with ID {lock_id}")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error deleting lock: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to delete lock: {e}"})


# Prompts (Updated to return list of dicts instead of Message objects)
@mcp.prompt()
def analyze_trade(
    pair: str, timeframe: str, ctx: Context
) -> List[Dict[str, Any]]:  # pylint: disable=unused-argument
    """Generate a prompt to analyze a trading pair's performance."""
    market_data = fetch_market_data(pair, timeframe, ctx)
    return [
        {"role": "user", "content": f"Analyze the recent performance of {pair} over {timeframe}."},
        {"role": "user", "content": f"Market data: {market_data}"},
        {
            "role": "assistant",
            "content": (f"I'll analyze the market data for {pair} and provide insights."),
        },
    ]


@mcp.prompt()
def trading_strategy(ctx: Context) -> str:
    """Generate a prompt for suggesting a trading strategy."""
    return (
        "Based on the current bot status, profit, and market conditions, "
        "suggest a trading strategy."
    )


# Run the server
if __name__ == "__main__":
    mcp.run()
