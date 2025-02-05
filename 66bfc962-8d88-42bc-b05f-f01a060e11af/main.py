from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log


class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]
        self.sma_length = 20  # Length of the SMA, it's adjustable

    @property
    def interval(self):
        # The frequency of data to be used, adjust based on your strategy's need
        return "1day"

    @property
    def assets(self):
        # The assets to trade, in this case, SPY
        return self.tickers

    @property
    def data(self):
        # Data required for the strategy, add more if necessary
        return []

    def run(self, data):
        allocation_dict = {}
        
        # Extract closing prices
        close_prices = [i["SPY"]["close"] for i in data["ohlcv"]]
        
        # Ensure we have enough data to compute SMA
        if len(close_prices) >= self.sma_length:
            # Compute the SMA for SPY
            sma_values = SMA("SPY", data["ohlcv"], self.sma_length)
            current_close_price = close_prices[-1]
            current_sma_value = sma_values[-1]
            
            # Decision logic based on 'LemanTrend' indicator
            if current_close_price > current_sma_value:
                log("Trend is up, buying SPY")
                allocation_dict["SPY"] = 1.0  # Full allocation to SPY
            elif current_close_price < current_sma_value:
                log("Trend is down, selling SPY")
                allocation_dict["SPY"] = 0  # No allocation to SPY
            else:
                log("Price equals SMA, hold positions")
                # Keep the allocation unchanged in case of equality; Adjust as needed
                allocation_dict["SPY"] = 0.5  # Example placeholder value
        else:
            log("Not enough data to compute SMA")
            allocation_dict["SPY"] = 0  # Default to no allocation

        return TargetAllocation(allocation_dict)