from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the ticker you are interested in
        self.ticker = "SPY"

    @property
    def assets(self):
        # List of assets the strategy will trade
        return [self.ticker]
    
    @property
    def interval(self):
        # Data interval for each candlestick
        return "5min"

    def run(self, data):
        # Initialize the allocation with no position
        allocation_dict = {self.ticker: 0.0}

        # Calculating RSI for the specified ticker
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)

        if rsi_values is not None and len(rsi_values) > 0:
            # Get the last RSI value
            current_rsi = rsi_values[-1]  
            log(f"Current RSI: {current_rsi}")

            # Check if RSI crosses below 30, indicating a potential buy signal
            if current_rsi < 30:
                log("RSI below 30, buying signal")
                allocation_dict[self.ticker] = 1.0  # Buy (or increase allocation to) SPY

            # Check if RSI crosses above 70, indicating a potential sell signal
            elif current_rsi > 70:
                log("RSI above 70, selling signal")
                allocation_dict[self.ticker] = 0.0  # Sell (or decrease allocation to) SPY

        return TargetAllocation(allocation_dict)