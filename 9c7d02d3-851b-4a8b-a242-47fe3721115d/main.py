from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the symbol for the SPY ETF
        self.ticker = "SPY"
        
    @property
    def assets(self):
        # Specifies that we are only interested in trading SPY
        return [self.ticker]

    @property
    def interval(self):
        # Closest possible approximation to the requested interval
        return "5min"

    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {self.ticker: 0}
        # Check if there is enough RSI data
        if len(data["ohlcv"]) > 9:  # Ensuring there are enough data points for RSI calculation
            rsi_values = RSI(self.ticker, data["ohlcv"], length=9)
            
            if rsi_values:  # Check if RSI calculation was successful
                current_rsi = rsi_values[-1]  # Most recent RSI value
                previous_rsi = rsi_values[-2]  # Previous RSI value to detect movement
                
                # Buy signal: RSI moves up from below 30
                if current_rsi > 30 and previous_rsi <= 30:
                    log("Buy signal detected.")
                    allocation_dict[self.ticker] = 1  # Allocating 100% to SPY
                
                # Sell signal: RSI drops from above 70
                elif current_rsi < 70 and previous_rsi >= 70:
                    log("Sell signal detected.")
                    allocation_dict[self.ticker] = 0  # Reducing allocation to 0% for SPY
        
        # Return the allocation decision
        return TargetAllocation(allocation_dict)