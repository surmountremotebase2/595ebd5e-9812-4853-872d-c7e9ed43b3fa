from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        return ["AAPL"]
    
    @property
    def interval(self):
        # Changed the interval to 5 minutes for this strategy
        return "5min"
    
    def run(self, data):
        """Execute the trading strategy based on MACD indicator.
        
        - Buys (allocates 100% to) AAPL when the MACD line crosses above the signal line,
        indicating a bullish signal.
        - Sells (allocates 0% to) AAPL when the MACD line crosses below the signal line,
        indicating a bearish signal.
        """
        
        aapl_macd = MACD("AAPL", data["ohlcv"], fast=12, slow=26)
        
        # Ensure we have enough data points to evaluate MACD and its signal line
        if not aapl_macd or len(aapl_macd['MACD']) < 2:
            log("Not enough data for MACD.")
            return TargetAllocation({"AAPL": 0})
        
        # Determine MACD line and signal line positions
        macd_line_current = aapl_macd['MACD'][-1]
        macd_line_previous = aapl_macd['MACD'][-2]
        signal_line_current = aapl_macd['signal'][-1]
        signal_line_previous = aapl_macd['signal'][-2]
        
        # Buy signal: MACD crosses above Signal line
        if macd_line_previous < signal_line_previous and macd_line_current > signal_line_current:
            log("MACD bullish crossover detected. Buying AAPL.")
            return TargetAllocation({"AAPL": 1})
        
        # Sell signal: MACD crosses below Signal line
        elif macd_line_previous > signal_line_previous and macd_line_current < signal_line_current:
            log("MACD bearish crossover detected. Selling AAPL.")
            return TargetAllocation({"AAPL": 0})
        
        # If neither condition is met, maintain current allocation
        else:
            log("No MACD crossover detected. No action taken.")
            # This example does not address maintaining current positions;
            # in a live strategy, consider accessing current holdings to make this decision.
            return TargetAllocation({"AAPL": 0})