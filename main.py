import os
import sys
from collections import deque

# Add vendor to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"

ENTRY_N = 120
EXIT_N = 20
TRAIL_BPS = 45
COOLDOWN = 120
SIZE_FRAC = 0.95

class Strategy:
    def __init__(self):
        self.highs = deque(maxlen=200)
        self.lows = deque(maxlen=200)
        self.closes = deque(maxlen=200)
        self.in_position = False
        self.peak_close = 0
        self.bars_since_exit = COOLDOWN

    def on_batch(self, state, batch):
        bar = state.latest.get(SYMBOL)
        if not bar:
            return []

        h = int(bar["h"])
        l = int(bar["l"])
        c = int(bar["c"])

        self.highs.append(h)
        self.lows.append(l)
        self.closes.append(c)

        if len(self.highs) < ENTRY_N:
            return []

        orders = []
        holding = state.positions.get(SYMBOL)

        if not self.in_position:
            hist_highs = list(self.highs)[:-1]
            entry_high = max(hist_highs[-ENTRY_N:])
            
            if self.bars_since_exit >= COOLDOWN and c > entry_high:
                notional = int(state.cash * SIZE_FRAC)
                if notional >= int(state.hello["fees"]["min_notional_quote_units"]):
                    orders.append({
                        "side": "buy",
                        "symbol": SYMBOL,
                        "notional_quote_units": notional,
                        "max_slippage_bps": 200
                    })
                    self.in_position = True
                    self.peak_close = c
            else:
                self.bars_since_exit += 1
        else:
            self.peak_close = max(self.peak_close, c)
            hist_lows = list(self.lows)[:-1]
            exit_low = min(hist_lows[-EXIT_N:])
            
            if c < exit_low or (c * 10000 < self.peak_close * (10000 - TRAIL_BPS)):
                qty = holding.qty if holding else 0
                if qty > 0:
                    orders.append({
                        "side": "sell",
                        "symbol": SYMBOL,
                        "qty": qty,
                        "max_slippage_bps": 200
                    })
                self.in_position = False
                self.bars_since_exit = 0

        return orders

strat = Strategy()

def on_batch(state, batch):
    return strat.on_batch(state, batch)

if __name__ == "__main__":
    makefun_bars.run(on_batch)
