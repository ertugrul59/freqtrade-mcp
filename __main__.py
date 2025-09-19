"""
Freqtrade MCP Server

This module provides an MCP (Model Context Protocol) server that integrates
with the Freqtrade cryptocurrency trading bot via its REST API, enabling
seamless AI agent interaction for automated trading operations.

The server provides tools for market data retrieval, trade execution,
bot control, and performance monitoring.
"""

import os
import json
from typing import List, AsyncIterator, Dict, Any
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context

# Import Freqtrade REST client
from freqtrade_client.ft_rest_client import FtRestClient

# Configuration loaded from environment variables
FREQTRADE_API_URL = os.getenv("FREQTRADE_API_URL", "http://127.0.0.1:8080")
USERNAME = os.getenv("FREQTRADE_USERNAME", "Freqtrader")
PASSWORD = os.getenv("FREQTRADE_PASSWORD", "SuperSecret1!")
TRADING_MODE = os.getenv("FREQTRADE_TRADING_MODE", "futures")  # "futures" or "spot"


# Lifecycle management for the Freqtrade client
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:  # pylint: disable=unused-argument
    """Manage the lifecycle of the Freqtrade REST client."""
    try:
        client = FtRestClient(FREQTRADE_API_URL, USERNAME, PASSWORD)
        # Test API connectivity
        if client.ping():
            print(f"✅ Connected to Freqtrade API (Trading Mode: {TRADING_MODE})")
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
        # Use REST API directly since client.config() doesn't exist
        import requests

        # Try the correct config endpoint
        try:
            r = requests.get(
                f"{FREQTRADE_API_URL.rstrip('/')}/api/v1/show_config",
                auth=(USERNAME, PASSWORD),
                timeout=10,
                headers={"Accept": "application/json"},
            )
            if r.ok and r.text:
                await ctx.info(f"fetch_config via /api/v1/show_config -> {r.status_code}")
                return r.text  # already JSON
            else:
                await ctx.info(
                    f"fetch_config /api/v1/show_config failed -> {r.status_code}: {r.text}"
                )
        except Exception as e:
            await ctx.info(f"fetch_config /api/v1/show_config error: {e}")

        # Fallback so callers can still infer mode/leverage from status
        status = client.status()
        await ctx.info("fetch_config fell back to /status")
        return json.dumps(
            {"note": "no /show_config endpoint; returned status fallback", "status": status}
        )
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error fetching config: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        try:
            print(f"[FreqtradeMCP] fetch_config error: {e}")
        except Exception:
            pass
        return str({"error": f"Failed to fetch config: {e}"})


@mcp.tool()
async def get_trading_mode(ctx: Context) -> str:
    """
    Get the current trading mode configuration.

    Parameters:
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: JSON response with current trading mode and configuration.
    """
    return str(
        {
            "trading_mode": TRADING_MODE,
            "description": "futures" if TRADING_MODE == "futures" else "spot",
            "symbol_format": "BASE/USDT:USDT" if TRADING_MODE == "futures" else "BASE/USDT",
            "environment_variable": "FREQTRADE_TRADING_MODE",
            "note": "Set FREQTRADE_TRADING_MODE=futures or FREQTRADE_TRADING_MODE=spot to change mode",
        }
    )


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


def _convert_symbol_format(symbol: str) -> str:
    """
    Convert symbol from various formats to Freqtrade format based on trading mode.

    Handles conversions:
    - KMNOUSDT -> KMNO/USDT:USDT (futures) or KMNO/USDT (spot)
    - BTCUSDT -> BTC/USDT:USDT (futures) or BTC/USDT (spot)
    - BTC/USDT -> BTC/USDT:USDT (futures) or BTC/USDT (spot)
    - BTC/USDT:USDT -> BTC/USDT:USDT (futures) or BTC/USDT (spot)

    Args:
        symbol: Input symbol in various formats

    Returns:
        Symbol in appropriate Freqtrade format based on TRADING_MODE
    """
    # Already in correct format for futures
    if "/USDT:USDT" in symbol:
        if TRADING_MODE == "spot":
            return symbol.replace(":USDT", "")  # Remove :USDT for spot
        return symbol

    # Handle formats like BTC/USDT -> BTC/USDT:USDT (futures) or BTC/USDT (spot)
    if "/USDT" in symbol and ":USDT" not in symbol:
        if TRADING_MODE == "futures":
            return f"{symbol}:USDT"
        return symbol

    # Handle Bybit format like KMNOUSDT, BTCUSDT
    if symbol.endswith("USDT") and "/" not in symbol and ":" not in symbol:
        # Extract base currency by removing USDT suffix
        base_currency = symbol[:-4]  # Remove 'USDT'
        if TRADING_MODE == "futures":
            return f"{base_currency}/USDT:USDT"
        else:
            return f"{base_currency}/USDT"

    # Fallback: assume it needs :USDT suffix for futures
    if TRADING_MODE == "futures" and ":USDT" not in symbol:
        return f"{symbol}:USDT"

    return symbol


def _validate_symbol_in_whitelist(client, symbol: str) -> tuple[str, bool]:
    """
    Validate if symbol exists in Freqtrade whitelist and return the correct format.

    Args:
        client: Freqtrade REST client
        symbol: Symbol to validate

    Returns:
        Tuple of (corrected_symbol, is_valid)
    """
    # Get whitelist - if this fails, we'll use basic conversion
    whitelist = []
    try:
        whitelist_response = client.whitelist()
        if isinstance(whitelist_response, dict) and "whitelist" in whitelist_response:
            whitelist = whitelist_response["whitelist"]
    except Exception:
        pass  # Will use basic conversion below

    # Check if symbol is in whitelist as-is
    if whitelist and symbol in whitelist:
        return symbol, True

    # Handle Bybit format symbols (e.g., KMNOUSDT -> KMNO/USDT:USDT or KMNO/USDT)
    if "/" not in symbol and ":" not in symbol and symbol.endswith("USDT"):
        base = symbol[:-4]  # Remove 'USDT' suffix

        # Convert based on trading mode
        if TRADING_MODE == "futures":
            primary_format = f"{base}/USDT:USDT"
            fallback_formats = [
                f"{base}/USDT",  # Spot format fallback
                f"{base}USDT:USDT",  # Alternative futures format
            ]
        else:  # spot mode
            primary_format = f"{base}/USDT"
            fallback_formats = [
                f"{base}/USDT:USDT",  # Futures format fallback
                f"{base}USDT:USDT",  # Alternative futures format
            ]

        # If we have whitelist, check if it's valid
        if whitelist:
            if primary_format in whitelist:
                return primary_format, True

            # Try fallback formats
            for fmt in fallback_formats:
                if fmt in whitelist:
                    return fmt, True

            # Not found in whitelist
            return primary_format, False
        else:
            # No whitelist available, assume conversion is correct
            return primary_format, True

    # For other formats, use basic conversion
    converted = _convert_symbol_format(symbol)
    if whitelist:
        return converted, converted in whitelist
    else:
        return converted, True


@mcp.tool()
async def place_trade(
    pair: str,
    side: str,
    ctx: Context,
    price: float | None = None,
    enter_tag: str | None = None,
    stake_amount: float | None = None,  # kept for backward compatibility (ignored)
) -> str:
    """
    Place or close a position using the official Freqtrade REST API endpoints.

    According to the Freqtrade REST API docs, new positions are opened via
    `forceenter(pair, side, price?)` and closed via `forceexit(pair)`.
    Reference: https://www.freqtrade.io/en/stable/rest-api/

    Parameters:
        pair (str): Trading pair in any format (e.g., "KMNOUSDT", "BTC/USDT", "BTC/USDT:USDT").
                   Will be automatically converted to Freqtrade futures format.
        side (str): One of ["buy", "long", "enter_long", "short", "enter_short",
                     "sell", "exit", "close"]. Long/short will open a position via
                     forceenter. Sell/exit/close will close via forceexit.
        price (float | None): Optional limit price for `forceenter`. If omitted, market will be used.
        enter_tag (str | None): Optional enter tag passed to `forceenter` for auditability.
        stake_amount (float | None): Ignored. Position sizing is controlled by Freqtrade config
                                     (e.g., stake_amount, balance ratio). Kept for compatibility.

    Returns:
        str: Stringified JSON response with trade result, or error message if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    # Convert and validate symbol format
    original_pair = pair
    pair, is_valid = _validate_symbol_in_whitelist(client, pair)

    if original_pair != pair:
        await ctx.info(
            f"✅ Symbol format conversion: {original_pair} -> {pair} (mode: {TRADING_MODE})"
        )

    if not is_valid:
        await ctx.info(f"⚠️ Symbol {pair} not found in whitelist")
        return str(
            {
                "error": f"Symbol {pair} not found in Freqtrade whitelist. Check fetch_whitelist for available symbols.",
                "original_symbol": original_pair,
                "converted_symbol": pair,
                "trading_mode": TRADING_MODE,
            }
        )

    # Normalize side
    normalized = side.strip().lower()
    open_long_aliases = {"buy", "long", "enter_long"}
    open_short_aliases = {"short", "enter_short"}
    close_aliases = {"sell", "exit", "close", "exit_long", "exit_short"}

    if normalized not in open_long_aliases | open_short_aliases | close_aliases:
        return str(
            {
                "error": "Invalid side. Use one of: buy/long/enter_long, short/enter_short, sell/exit/close"
            }
        )

    # Basic validation for price (limit orders)
    if price is not None:
        try:
            price = float(price)
        except (TypeError, ValueError):
            return str({"error": "price must be a number if provided"})
        if price <= 0:
            return str({"error": "price must be greater than 0"})

    try:
        if normalized in open_long_aliases or normalized in open_short_aliases:
            desired_side = "long" if normalized in open_long_aliases else "short"

            if hasattr(client, "forceenter"):
                # Call with keywords to be future-proof: `price` and `enter_tag` are optional
                kwargs: Dict[str, Any] = {}
                if price is not None:
                    kwargs["price"] = price
                # Auto-tag orders so it's clear if they were market or limit
                auto_tag = None
                if price is not None:
                    auto_tag = "mcp-limit"
                else:
                    auto_tag = "mcp-market"
                kwargs["enter_tag"] = enter_tag if enter_tag is not None else auto_tag
                response = client.forceenter(pair, desired_side, **kwargs)
                await ctx.info(
                    f"Entered {desired_side} on {pair} via forceenter"
                    + (f" @ {price}" if price is not None else "")
                )
            else:
                return str({"error": "No supported 'forceenter' method available on client"})
        else:  # close / exit
            if hasattr(client, "forceexit"):
                # Price is not applicable for exits; ignore if provided
                try:
                    # Try to resolve trade_id from current open trades
                    trade_id = None
                    try:
                        current_status = client.status()
                        if isinstance(current_status, (list, tuple)):
                            # Normalize candidate pairs
                            candidates = {pair}
                            if ":USDT" not in pair and "USDT" in pair:
                                candidates.add(f"{pair}:USDT")
                            if pair.endswith(":USDT"):
                                candidates.add(pair.replace(":USDT", "/USDT"))
                            for t in current_status:
                                tp = str(t.get("pair") or "")
                                if tp in candidates and t.get("is_open"):
                                    trade_id = t.get("trade_id")
                                    break
                    except Exception:
                        trade_id = None

                    if trade_id is not None:
                        response = client.forceexit(tradeid=trade_id)
                        await ctx.info(f"Exited trade_id {trade_id} via forceexit")
                    else:
                        # Fall back to pair-based exit with futures pair normalization
                        exit_pair = pair
                        if ":USDT" not in pair and "USDT" in pair:
                            exit_pair = f"{pair}:USDT"
                        response = client.forceexit(pair=exit_pair)
                        await ctx.info(f"Exited position on {exit_pair} via forceexit")
                except Exception as exit_error:
                    # If forceexit fails, try alternative approach
                    await ctx.info(f"Forceexit failed: {exit_error}, trying alternative method")
                    try:
                        response = client.forceexit(pair=pair)
                        await ctx.info(f"Exited position on {pair} via forceexit (retry)")
                    except Exception as retry_error:
                        await ctx.info(f"All exit methods failed: {retry_error}")
                        return str({"error": f"Failed to exit position: {retry_error}"})
            else:
                return str({"error": "No supported 'forceexit' method available on client"})

        # Normalize success payloads so callers don't need to parse exchange-specific quirks
        await ctx.info("Action completed successfully")

        # Helper to coerce response into a dict-like shape for richer metadata
        def to_text(val: Any) -> str:
            try:
                return str(val)
            except Exception:  # pylint: disable=broad-except
                return ""

        resp_text = to_text(response)

        # Detect common "already open" condition from Freqtrade which still implies success
        already_open = "already open" in resp_text.lower()

        # Detect the known "forceexit invalid argument" text that occurs even on successful exit
        forceexit_invalid_arg = (
            "forceexit" in resp_text.lower() and "invalid argument" in resp_text.lower()
        )

        if normalized in open_long_aliases or normalized in open_short_aliases:
            normalized_payload = {
                "status": "ok",
                "action": "enter",
                "side": "long" if normalized in open_long_aliases else "short",
                "pair": pair,
                "price": price,
                "enter_tag": kwargs.get("enter_tag") if "kwargs" in locals() else enter_tag,
                "already_open": already_open,
                "raw": response,
            }
            return str(normalized_payload)
        else:
            # Exit path
            if forceexit_invalid_arg:
                normalized_payload = {
                    "status": "ok",
                    "action": "exit",
                    "pair": pair,
                    "note": "forceexit returned 'invalid argument' but exit signal was sent",
                    "raw": response,
                }
                return str(normalized_payload)

            # Default: return a normalized ok envelope
            normalized_payload = {
                "status": "ok",
                "action": "exit",
                "pair": pair,
                "raw": response,
            }
            return str(normalized_payload)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error placing trade: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to place trade: {e}"})


@mcp.tool()
async def close_position(pair: str, ctx: Context) -> str:
    """
    Close a specific position by pair name.

    This tool provides an alternative method to close positions using
    trade_id resolution to avoid invalid-argument errors.

    Parameters:
        pair (str): Trading pair to close in any format (e.g., "KMNOUSDT", "BTC/USDT").
                   Will be automatically converted to Freqtrade futures format.
        ctx (Context): MCP context object for logging and client access.

    Returns:
        str: Stringified JSON response with close result, or error message if failed.
    """
    client: FtRestClient = ctx.request_context.lifespan_context["client"]
    if not client:
        return str({"error": "Freqtrade client not connected"})

    try:
        # Convert and validate symbol format
        original_pair = pair
        pair, is_valid = _validate_symbol_in_whitelist(client, pair)

        if original_pair != pair:
            await ctx.info(f"Symbol format conversion for close: {original_pair} -> {pair}")

        if not is_valid:
            await ctx.info(f"⚠️ Symbol {pair} not found in whitelist for close operation")

        # Normalize candidate pair formats (keep original logic for robustness)
        candidates = {pair}
        if ":USDT" not in pair and "USDT" in pair:
            candidates.add(f"{pair}:USDT")
        if pair.endswith(":USDT"):
            candidates.add(pair.replace(":USDT", "/USDT"))

        # Resolve trade_id from current open trades
        trade_id = None
        try:
            status = client.status()
            if isinstance(status, (list, tuple)):
                for t in status:
                    tp = str(t.get("pair") or "")
                    if t.get("is_open") and tp in candidates:
                        trade_id = t.get("trade_id")
                        break
        except Exception as e:
            await ctx.info(f"Failed to read status for trade_id: {e}")

        if trade_id is not None:
            response = client.forceexit(tradeid=trade_id)
            await ctx.info(f"Exited trade_id {trade_id} via forceexit")
            return str(
                {"status": "ok", "action": "close_position", "trade_id": trade_id, "raw": response}
            )

        # Fallback: try pair-based exit last (may fail on some client versions)
        last_error = None
        for p in list(candidates):
            try:
                response = client.forceexit(p)
                await ctx.info(f"Exited position on {p} via forceexit (fallback)")
                return str({"status": "ok", "action": "close_position", "pair": p, "raw": response})
            except Exception as e:
                last_error = e
                await ctx.info(f"Fallback close failed for {p}: {e}")
                continue

        return str(
            {
                "error": f"Failed to close position. No trade_id found and pair-based exit failed: {last_error}"
            }
        )
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to close position: {e}"})


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
        # Use the correct method name from Freqtrade client
        if hasattr(client, "start"):
            response = client.start()
        elif hasattr(client, "start_bot"):
            response = client.start_bot()
        else:
            return str({"error": "No supported 'start' method available on client"})

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
        # Use the correct method name from Freqtrade client
        if hasattr(client, "stop"):
            response = client.stop()
        elif hasattr(client, "stop_bot"):
            response = client.stop_bot()
        else:
            return str({"error": "No supported 'stop' method available on client"})

        await ctx.info("Freqtrade bot stopped")
        return str(response)
    except (ConnectionError, TimeoutError) as e:
        return str({"error": f"Connection error stopping bot: {e}"})
    except Exception as e:  # pylint: disable=broad-except
        return str({"error": f"Failed to stop bot: {e}"})


# @mcp.tool()
# async def reload_config(ctx: Context) -> str:
#     """
#     Reload the bot configuration.

#     Parameters:
#         ctx (Context): MCP context object for logging and client access.

#     Returns:
#         str: Stringified JSON response or success message, or error if failed.
#     """
#     client: FtRestClient = ctx.request_context.lifespan_context["client"]
#     if not client:
#         return str({"error": "Freqtrade client not connected"})

#     try:
#         response = client.reload_config()
#         await ctx.info("Configuration reloaded")
#         return str(response)
#     except (ConnectionError, TimeoutError) as e:
#         return str({"error": f"Connection error reloading config: {e}"})
#     except Exception as e:  # pylint: disable=broad-except
#         return str({"error": f"Failed to reload config: {e}"})


# @mcp.tool()
# async def update_config_param(param: str, value: Any, ctx: Context) -> str:
#     """
#     Update a specific configuration parameter in Freqtrade.

#     This tool allows dynamic updates to Freqtrade configuration without
#     manually editing the config file. It updates the file and then
#     reloads the configuration to apply changes immediately.

#     Parameters:
#         param (str): Configuration parameter to update (e.g., "stake_amount", "leverage")
#         value (Any): New value for the parameter
#         ctx (Context): MCP context object for logging and client access.

#     Returns:
#         str: JSON response with success status or error message.

#     Examples:
#         - update_config_param("stake_amount", 150)  # Set stake to 150 USDT
#         - update_config_param("leverage", 5)        # Set leverage to 5x
#     """
#     client: FtRestClient = ctx.request_context.lifespan_context["client"]
#     if not client:
#         return json.dumps({"error": "Freqtrade client not connected"})

#     try:
#         # Resolve the config file path robustly
#         env_path = os.getenv("FREQTRADE_CONFIG_PATH")
#         resolved_path = None
#         if env_path:
#             candidate = os.path.abspath(env_path)
#             if os.path.exists(candidate):
#                 resolved_path = candidate
#         if resolved_path is None:
#             # Project root is 2 levels up from this file
#             here = os.path.dirname(os.path.abspath(__file__))
#             project_root = os.path.abspath(os.path.join(here, os.pardir, os.pardir))
#             candidate = os.path.join(project_root, "freqtrade", "user_data", "config.json")
#             if os.path.exists(candidate):
#                 resolved_path = candidate
#         if resolved_path is None:
#             # Fallback to relative path (for tests)
#             candidate = "freqtrade/user_data/config.json"
#             if os.path.exists(candidate):
#                 resolved_path = candidate

#         if resolved_path is None:
#             return json.dumps(
#                 {
#                     "error": "Config file not found",
#                     "tried": [
#                         env_path or "(no FREQTRADE_CONFIG_PATH)",
#                         os.path.join(
#                             os.path.abspath(
#                                 os.path.join(
#                                     os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir
#                                 )
#                             ),
#                             "freqtrade",
#                             "user_data",
#                             "config.json",
#                         ),
#                         "freqtrade/user_data/config.json",
#                     ],
#                 }
#             )

#         # Read current configuration
#         try:
#             with open(resolved_path, "r", encoding="utf-8") as f:
#                 config = json.load(f)
#         except (json.JSONDecodeError, IOError) as e:
#             return json.dumps({"error": f"Failed to read config file: {e}", "path": resolved_path})

#         # Store old value for logging
#         old_value = config.get(param, "not_set")

#         # Update the parameter with proper data type handling
#         if param in ["stake_amount", "leverage", "max_open_trades", "dry_run_wallet"]:
#             try:
#                 if param == "stake_amount":
#                     config[param] = float(value)
#                 elif param in ["leverage", "max_open_trades"]:
#                     config[param] = int(value)
#                 else:
#                     config[param] = float(value)
#             except (ValueError, TypeError):
#                 config[param] = value
#         else:
#             config[param] = value

#         # Write updated configuration back to file
#         try:
#             with open(resolved_path, "w", encoding="utf-8") as f:
#                 json.dump(config, f, indent=2, ensure_ascii=False)
#         except IOError as e:
#             return json.dumps({"error": f"Failed to write config file: {e}", "path": resolved_path})

#         # Reload configuration to apply changes
#         try:
#             reload_response = client.reload_config()
#             await ctx.info(
#                 f"Configuration parameter '{param}' updated from {old_value} to {value} @ {resolved_path}"
#             )
#             await ctx.info("Configuration reloaded successfully")

#             return json.dumps(
#                 {
#                     "success": True,
#                     "param": param,
#                     "old_value": old_value,
#                     "new_value": value,
#                     "config_path": resolved_path,
#                     "reload_response": str(reload_response),
#                     "message": f"Successfully updated {param} from {old_value} to {value}",
#                 }
#             )

#         except Exception as e:
#             return json.dumps(
#                 {
#                     "success": True,
#                     "param": param,
#                     "old_value": old_value,
#                     "new_value": value,
#                     "config_path": resolved_path,
#                     "warning": f"Parameter updated in file but reload failed: {e}",
#                     "note": "You may need to manually reload the configuration",
#                 }
#             )

#     except Exception as e:  # pylint: disable=broad-except
#         error_msg = f"Failed to update config parameter '{param}': {e}"
#         await ctx.info(f"❌ {error_msg}")
#         return json.dumps({"error": error_msg})


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
