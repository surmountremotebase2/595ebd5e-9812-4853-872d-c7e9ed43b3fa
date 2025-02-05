from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Defines the ticker symbol for trading.
        self.ticker = "SPY"

    @property
    def assets(self):
        # Specifies that we're trading SPY.
        return [self.ticker]

    @property
    def interval(self):
        # Use 1-minute interval for analysis.
        return "1min"

    def run(self, data):
        """
        Execute the trading strategy based on RSI values.

        :param data: A dictionary containing the asset's data, including price and technical indicators.
        :return: TargetAllocation indicating what proportion of our portfolio should be in SPY.
        """
        # Initialize the allocation towards SPY as 0.
        spy_stake = 0

        # Calculate the RSI for SPY.
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)  # Using a window of 14 periods for RSI calculation.

        if rsi_values is not None and len(rsi_values) > 0:
            # Get the most recent RSI value.
            current_rsi = rsi_values[-1]

            if current_rsi < 30:
                # RSI < 30 suggests SPY is potentially undervalued; buy signal.
                spy_stake = 1  # Allocate 100% of the portfolio to SPY.
            elif current_rsi > 70:
                # RSI > 70 suggests SPY is potentially overvalued; sell signal.
                spy_stake = 0  # Allocate 0% of the portfolio to SPY, effectively selling it.

        # Log the decision for auditing.
        log(f"RSI for {self.ticker}: {current_rsi}, allocation: {spy_stake}")

        # Return the target allocation.
        return TargetAllocation({self.ticker: spy_stake})