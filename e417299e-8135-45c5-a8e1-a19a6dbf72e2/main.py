from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SPY"

    @property
    def interval(self):
        # Trading on a 1-minute interval as required
        return "1min"

    @property
    def assets(self):
        # Focus on the SPY asset for this strategy
        return [self.ticker]

    @property
    def data(self):
        # No external data needed apart from price for this strategy
        return []

    def leman_trend_indicator(self, data, periods):
        """
        Calculate Leman Trend Indicator using Exponential Moving Averages (EMA)
        for different periods and figure out the trading signal.
        :param data: Data dictionary containing open, high, low, close, volume
        :param periods: List of periods for EMA calculation
        :return: Signal string ('buy', 'sell', or 'hold')
        """
        # Calculating EMAs for given periods
        emas = {p: EMA(self.ticker, data, p) for p in periods}
        # Determining signals based on EMA crossovers
        if emas[periods[0]][-1] > emas[periods[1]][-1] and emas[periods[1]][-1] > emas[periods[2]][-1]:
            return 'buy'
        elif emas[periods[0]][-1] < emas[periods[1]][-1] and emas[periods[1]][-1] < emas[periods[2]][-1]:
            return 'sell'
        else:
            return 'hold'

    def run(self, data):
        # Define EMA periods for the strategy
        minPeriod, midPeriod, maxPeriod = 13, 21, 34
        periods = [minPeriod, midPeriod, maxPeriod]
        
        # Calculate the signal
        signal = self.leman_trend_indicator(data["ohlcv"], periods)
        log(f"Trading signal for {self.ticker}: {signal}")
        
        # Determine allocation based on the signal
        allocation = 0 if signal == 'sell' else 1 if signal == 'buy' else 0.5
        return TargetAllocation({self.ticker: allocation})