import os
import sys
from collections import deque

# Add vendor to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"
N = 360
DIP_BPS = 85
EXIT_BPS = 40
MAX_HOLD = 300
SIZE_FRAC = 0.95

class Strategy:
    def __init__(self):
        self.closes = deque(maxlen=1500)
        self.held_bars = 0

    def on_batch(self, state, batch):
        bar = state.latest.get(SYMBOL)
        if not bar:
            return []

        c = int(bar["c"])
        self.closes.append(c)

        if len(self.closes) < N or state.warming_up:
            return []

        last_n = list(self.closes)[-N:]
        sma = sum(last_n) / N

        orders = []
        holding = state.positions.get(SYMBOL)
        is_holding = holding is not None and holding.qty > 0

        if not is_holding:
            self.held_bars = 0
            if c * 10000 <= sma * (10000 - DIP_BPS):
                notional = int(state.cash * SIZE_FRAC)
                min_notional = int(state.hello["fees"]["min_notional_quote_units"])
                if notional >= min_notional:
                    orders.append({
                        "side": "buy",
                        "symbol": SYMBOL,
                        "notional_quote_units": notional,
                        "max_slippage_bps": 200
                    })
        else:
            self.held_bars += 1
            if c * 10000 >= sma * (10000 + EXIT_BPS) or self.held_bars >= MAX_HOLD:
                qty = holding.qty
                if qty > 0:
                    orders.append({
                        "side": "sell",
                        "symbol": SYMBOL,
                        "qty": qty,
                        "max_slippage_bps": 200
                    })
                self.held_bars = 0

        return orders

strat = Strategy()

def on_batch(state, batch):
    return strat.on_batch(state, batch)

if __name__ == "__main__":
    makefun_bars.run(on_batch)
