from functions import *

# API call

openai.api_key = open('API_KEY.txt', 'r').read()

functions = [
    {
    "name": "get_stock_price", "description": "Gets the latest stock price given the ticker symbol of a company.",
     "parameters": {'type': 'object', 'properties': {'ticker': {'type': 'string',
                                                                'description': 'The stock ticker symbol for a company (for example: AAPL for Apple).'}},
                    'required': ['ticker']}}, {"name": "calculate_SMA",
                                               "description": "Calculate the simple moving average for a given stock ticker and a window.",
                                               "parameters": {'type': 'object', 'properties': {
                                                   'ticker': {'type': 'string',
                                                              'description': 'The stock ticker symbol for a company (for example: AAPL for Apple)'},
                                                   'window': {'type': 'integer',
                                                              'description': 'The timeframe to consider when calculating the SMA'}},
                                                              'required': ['ticker', 'window'], }, },
    {"name": "calculate_EMA",
     "description": "Calculate the exponential moving average for a given stock ticker and a window.",
     "parameters": {"type": "object", "properties": {
         "ticker": {"type": "string", "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)", },
         "window": {"type": "integer", "description": "The timeframe to consider when calculating the EMA"}},
                    "required": ["ticker", "window"], }, },
    {"name": "calculate_RSI", "description": "Calculate the RSI for a given stock ticker.",
     "parameters": {"type": "object", "properties": {"ticker": {"type": "string",
                                                                "description": "The stock ticker symbol for a company (e.g. AAPL for Apple)", }, },
                    "required": ["ticker"], }, },
    {"name": "calculate_MACD", "description": "Calculate the MACD for a given stock ticker.",
     "parameters": {"type": "object", "properties": {"ticker": {"type": "string",
                                                                "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)", }, },
                    "required": ["ticker"], }, }, {"name": "plot_stock_price",
                                                   "description": "Plot the stock price for the last year given the ticker symbol of a company.",
                                                   "parameters": {"type": "object", "properties": {
                                                       "ticker": {"type": "string",
                                                                  "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)", }, },
                                                                  "required": ["ticker"], }, },

    {
        "name": "plot_multiple_stock_prices",
        "description": "Gets the latest stock prices given a list of ticker symbols for multiple companies.",
        "parameters": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "A list of stock ticker symbols for multiple companies (e.g., ['AAPL', 'GOOGL'])."
                    }
                }
            },
            "required": ["tickers"]
        }
    }
     ]



# ChatGPT Function Calling
available_functions = {'get_stock_price': get_stock_price, 'calculate_SMA': calculate_SMA,
                       'calculate_EMA': calculate_EMA, 'calculate_RSI': calculate_RSI, 'calculate_MACD': calculate_MACD,
                       'plot_stock_price': plot_stock_price, 'plot_multiple_stock_prices': plot_multiple_stock_prices,
                       #'calculate_Bollinger_Bands': calculate_Bollinger_Bands,
                       }

functions2 = [
    {"name": "name", "description": "none.",
     "parameters": {'type': 'object', 'properties': {'none': {'type': 'none',
                                                                'description': 'none'}},
                    'required': ['none']}}
]

