from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset we're interested in
        self.ticker = "SPY"

    @property
    def assets(self):
        # The assets method specifies which assets we are trading
        return [self.ticker]

    @property
    def interval(self):
        # Interval set to 5min for high-frequency trading approach
        return "5min"

    def run(self, data):
        # Retrieve the latest 20 EMA values for SPY
        ema_values = EMA(self.ticker, data["ohlcv"], length=20)
        
        if ema_values is None or len(ema_values) < 1:
            # If there's no data, we cannot make a decision
            log("EMA data unavailable for trading decision.")
            return TargetAllocation({})
        
        # Get the latest EMA value
        latest_ema = ema_values[-1]
        # Get the latest closing price of SPY
        latest_close = data["ohlcv"][-1][self.ticker]["close"]
        
        # Allocate 100% to SPY if the latest price is above the 20-period EMA
        # Otherwise, hold no position (could be interpreted as selling if already holding)
        if latest_close > latest_ema:
            log(f"SPY price {latest_close} is above EMA {latest_ema}, buying.")
            return TargetAllocation({self.ticker: 1.0})
        else:
            log(f"SPY price {latest_close} is below EMA {latest_ema}, not buying.")
            return TargetAllocation({self.ticker: 0.0})