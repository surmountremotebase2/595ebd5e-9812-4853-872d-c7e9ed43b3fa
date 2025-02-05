from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for SPY ETF
        self.ticker = "SPY"
        # Initialize any other required variables here

    @property
    def assets(self):
        # List of assets this strategy will trade
        return [self.ticker]

    @property
    def interval(self):
        # Defines the interval for data; for this strategy, we're using 5 minutes
        return "5min"

    @property
    def data(self):
        # Define the data requirements for the strategy; in this case, RSI computation
        # doesn't directly require adding external data here because it will be computed
        # from price data
        return []

    def run(self, data):
        # Implement the trading logic
        current_rsi = RSI(self.ticker, data['ohlcv'], length=14)[-1]  # Calculate the latest RSI with standard period 14

        allocation_dict = {}
        
        if current_rsi < 30:
            # RSI is below 30, indicating a potential oversold condition. Buy.
            allocation_dict[self.ticker] = 1  # full allocation to SPY
            log(f"Buying {self.ticker} as RSI is below 30: RSI={current_rsi}")
        elif current_rsi > 70:
            # RSI is above 70, indicating a potential overbought condition. Sell.
            allocation_dict[self.ticker] = 0  # no allocation to SPY
            log(f"Selling {self.ticker} as RSI is above 70: RSI={current_rsi}")
        else:
            # If RSI is between 30 and 70, maintain current position without change.
            # Here you might need to access current holdings to decide smartly. For 
            # simplicity, we assume no action is needed, so the allocation remains unchanged.
            # This illustrative code doesn't show how to preserve current state or access holdings.
            log(f"RSI for {self.ticker} is between 30 and 70: RSI={current_rsi}. No action taken.")

        return TargetAllocation(allocation_dict)

# Note: Proper handling of the current position (whether you hold the stock or not) is crucial
# to apply buy/sell decisions effectively. This requires tracking state over execution cycles,
# possibly through external state management or by inferring the current position from the last
# allocation and market data, which is not explicitly covered in this simplified example.