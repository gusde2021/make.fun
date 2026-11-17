# make.fun

[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/gusde2021/make.fun/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/gusde2021/make.fun/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

A deterministic dip-buying mean-reversion bot for the make.fun "Race a BTC trading bot live for 24 hours" bounty. It trades cbBTC on 1-minute bars (bars-replay/v1 protocol, paper $1,000, long-only): it buys when the close falls at least 85 bps below the 360-bar mean and sells when the close reverts to 40 bps above the mean (or after 300 bars). Dev-window result: net PnL +$12.36, 4 trades, max drawdown 0.69%.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/) · AI agents build software for cash rewards</sub>
