from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ohlcv
from surmount.technical_indicators import EMA  # Using EMA as a basis for Lemantrend
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # We are trading SPY on a 5 min interval
        self.ticker = "SPY"

    @property
    def interval(self):
        # Set the interval for data collection to 5 minutes
        return "5min"

    @property
    def assets(self):
        # Define the asset we're interested in trading
        return [self.ticker]

    def run(self, data):
        # Implement a basic Lemantrend-like indicator using a fast and slow EMA to determine trend direction
        fast_ema_period = 12  # Short term
        slow_ema_period26  # Long term

        # Assuming data["ohlcv"] provides a list of ohlcv dictionaries
        # We need to have sufficient data points, ideally more than slow_ema_period
        if len(data["ohlcv"]) < slow_ema_period:
            return TargetAllocation({self.ticker: 0})  # Not enough data to make a decision

        # Calculate fast and slow EMAs
        fast_ema = EMA(self.ticker, data["ohlcv"], fast_ema_period)
        slow_ema = EMA(self.ticker, data["ohlcv"], slow_ema_period)

        # Determine the trading signal of the EMAs
        if fast_ema[-1] > slow_ema[-1]:
            # Fast EMA crosses EMA, indicating an upt            allocation = 1  # Fully invest in SPY
        elif fast_ema[-1] < slow_ema[-1]:
            # Fast EMA crosses below slow EMA, indicating a downtrend
            allocation0  # Exit
        else:
            # If there with the current allocation (This is a simplification)
            allocation = data["holdings"].get(self.ticker, 0)

        # Log the decision for debugging purposes
        log_msg = f"Trading decision for {self.ticker}: Allocation -> {allocation}"
        log(log_msg)

        return TargetAllocation({self.ticker: allocation})