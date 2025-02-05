from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.asset = "AAPL"  # Asset to trade

    @property
    def assets(self):
        return [self.asset]

    @property
    def interval(self):
        # Choosing '1day' as the interval for our analysis
        return "1day"

    def run(self, data):
        # Calculate EMAs for the specified periods
        ema_short = EMA(self.asset, data, 13)  # Short period (Blue Line)
        ema_mid = EMA(self.asset, data, 21)    # Middle period for additional smoothing, if needed
        ema_long = EMA(self.asset, data, 34)   # Long period (Red Line)

        # Ensure we have sufficient data to compare EMAs
        if not ema_short or not ema_long:
            return TargetAllocation({self.asset: 0})

        # Initialize allocation
        allocation = 0

        # Check if the EMA lines have crossed
        # Buy signal: Short (Blue) EMA crosses above Long (Red) EMA
        if ema_short[-1] > ema_long[-1] and ema_short[-2] < ema_long[-2]:
            log("Buy signal identified. Initiating buy (long) position.")
            allocation = 1  # Full investment in asset

        # Sell signal: Long (Red) EMA crosses above Short (Blue) EMA
        elif ema_short[-1] < ema_long[-1] and ema_short[-2] > ema_long[-2]:
            log("Sell signal identified. Exiting position.")
            allocation = 0  # Exit asset

        # Calculate target allocation based on signal
        return TargetAllocation({self.asset: allocation})