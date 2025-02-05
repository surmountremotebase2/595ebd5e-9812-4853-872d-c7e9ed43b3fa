from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import ohlcv

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Define which assets this strategy applies to
        return ["SPY"]

    @property
    def interval(self):
        # Interval set as 1min closest to the 10min as per the requirement, adjust if needed
        return "1min"

    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"SPY": 0.0}

        # Calculate RSI for SPY with a 9 period lookback
        rsi_values = RSI("SPY", data["ohlcv"], length=9)

        if rsi_values:
            current_rsi = rsi_values[-1]  # Get the most recent RSI value

            # Check for buy signal (RSI moving above 30 from below)
            if current_rsi > 30 and rsi_values[-2] < 30:
                allocation_dict["SPY"] = 1.0  # Full allocation to SPY

            # Check for sell signal (RSI moving below 70 from above)
            elif current_rsi < 70 and rsi_values[-2] > 70:
                allocation_dict["SPY"] = 0.0  # No allocation to SPY

        return TargetAllocation(allocation_dict)