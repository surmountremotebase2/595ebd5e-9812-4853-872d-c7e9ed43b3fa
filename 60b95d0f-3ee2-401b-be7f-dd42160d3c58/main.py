from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Specify the asset ticker you're interested in
        self.tickers = ["SPY"]

    @property
    def assets(self):
        # Return the list of asset tickers
        return self.tickers

    @property
    def interval(self):
        # Set the data interval for RSI calculation; can be 1min, 5min, 1hour, 4hour, 1day
        return "1day"
    
    def run(self, data):
        # Initialize allocation for SPY to 0
        allocation_dict = {"SPY": 0}

        # Calculate RSI for SPY with a period of 9
        rsi_values = RSI("SPY", data["ohlcv"], 9)

        if rsi_values:  # Make sure RSI values are not empty
            latest_rsi = rsi_values[-1]  # Get the latest RSI value

            # Buy signal: RSI crosses above 30 from below (indicating potential recovery from oversold)
            if latest_rsi > 30 and rsi_values[-2] < 30:
                allocation_dict["SPY"] = 1  # Set SPY allocation to 100%
                log("Buying SPY - RSI crossed above 30")

            # Sell signal: RSI drops below 70 from above (indicating potential loss of overbought momentum)
            elif latest_rsi < 70 and rsi_values[-2] > 70:
                allocation_dict["SPY"] = 0  # Set SPY allocation to 0%
                log("Selling SPY - RSI crossed below 70")

        # Return the target allocation
        return TargetAllocation(allocation_dict)