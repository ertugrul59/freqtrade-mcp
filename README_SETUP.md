# Freqtrade MCP Server Setup Guide

This guide explains how to set up and use the Freqtrade MCP server in your funding rate agent project.

## 🚀 **What This Gives You**

The Freqtrade MCP server provides **paper trading with real market data** - exactly what you wanted! It offers:

- ✅ **Real market data** from exchanges (not synthetic like testnet)
- ✅ **Zero financial risk** (paper trading mode)
- ✅ **Built-in risk management** (stop-loss, take-profit, position sizing)
- ✅ **Professional trading features** (backtesting, strategy optimization)
- ✅ **Mature platform** with thousands of users

## 📋 **Prerequisites**

1. **Python 3.13+** ✅ (You have 3.13.2)
2. **Virtual environment** ✅ (Already set up)
3. **Dependencies installed** ✅ (freqtrade-client, mcp[cli])

## 🔧 **Current Setup Status**

✅ **MCP Server**: Cloned and configured  
✅ **Dependencies**: Installed in virtual environment  
✅ **Configuration**: Working with demo mode  
✅ **Testing**: Server starts successfully

## 🎯 **Next Steps**

### **Option 1: Quick Demo Mode (Recommended for Testing)**

Start the server in demo mode to test functionality:

```bash
cd my-mcp-servers/freqtrade-mcp
source .venv/bin/activate
python start_server.py --demo
```

### **Option 2: HTTP Mode for Integration**

Start the server in HTTP mode for easier integration:

```bash
python start_server.py --transport streamable-http --port 8005
```

### **Option 3: Full Freqtrade Setup**

To use real paper trading with actual exchange data:

1. **Install Freqtrade**:

   ```bash
   pip install freqtrade
   ```

2. **Create Freqtrade configuration**:

   ```bash
   freqtrade create-config --config config.json
   ```

3. **Configure for paper trading**:

   ```json
   {
     "dry_run": true,
     "exchange": {
       "name": "bybit",
       "key": "your_api_key",
       "secret": "your_secret",
       "sandbox": true
     },
     "api_server": {
       "enabled": true,
       "listen_ip_address": "127.0.0.1",
       "listen_port": 8080,
       "username": "Freqtrader",
       "password": "SuperSecret1!"
     }
   }
   ```

4. **Start Freqtrade**:

   ```bash
   freqtrade trade --config config.json
   ```

5. **Connect MCP server**:
   ```bash
   python start_server.py --live
   ```

## 🔗 **Integration with Your Agent**

### **MCP Client Configuration**

Add this to your agent's MCP configuration:

```python
# In your agent's MCP config
freqtrade_config = {
    "freqtrade-mcp": {
        "command": "python",
        "args": ["/path/to/freqtrade-mcp/start_server.py", "--demo"],
        "env": {
            "FREQTRADE_API_URL": "http://127.0.0.1:8080",
            "FREQTRADE_USERNAME": "Freqtrader",
            "FREQTRADE_PASSWORD": "SuperSecret1!"
        }
    }
}
```

### **Available Tools**

The MCP server provides these tools:

- **Market Data**: `fetch_market_data(pair, timeframe)`
- **Trading**: `place_trade(pair, side, amount)`
- **Bot Control**: `start_bot()`, `stop_bot()`
- **Risk Management**: Built into Freqtrade
- **Performance**: `fetch_profit()`, `fetch_performance()`

## 🧪 **Testing**

### **Test Server Configuration**

```bash
python start_server.py --config
```

### **Test Server Functionality**

```bash
python simple_test.py
```

### **Test Demo Mode**

```bash
python start_server.py --demo
# Press Ctrl+C to stop
```

## 🎮 **Demo Mode vs Live Mode**

| Feature         | Demo Mode    | Live Mode             |
| --------------- | ------------ | --------------------- |
| **Market Data** | ✅ Real      | ✅ Real               |
| **Trading**     | ❌ Simulated | ✅ Real (paper)       |
| **Risk**        | ❌ None      | ⚠️ Paper money        |
| **Setup**       | ✅ Simple    | ⚠️ Requires Freqtrade |
| **Testing**     | ✅ Perfect   | ✅ Realistic          |

## 🚨 **Important Notes**

1. **Demo Mode**: Safe for testing, no real trading
2. **Live Mode**: Uses real exchange APIs but paper trading
3. **Risk Management**: Freqtrade handles SL/TP automatically
4. **Position Sizing**: Built into Freqtrade strategies
5. **Backtesting**: Available for strategy validation

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Import Errors**: Make sure you're in the virtual environment
2. **Connection Errors**: Freqtrade API not running (expected in demo mode)
3. **Port Conflicts**: Change port in configuration

### **Getting Help**

- Check Freqtrade documentation: https://www.freqtrade.io/
- MCP server logs will show detailed error information
- Use `--config` flag to verify settings

## 🎉 **Ready to Use!**

Your Freqtrade MCP server is now:

- ✅ **Installed and configured**
- ✅ **Tested and working**
- ✅ **Ready for integration**
- ✅ **Safe for development** (demo mode)

Start with demo mode to test the integration, then move to full Freqtrade setup when you're ready for paper trading with real market data!
