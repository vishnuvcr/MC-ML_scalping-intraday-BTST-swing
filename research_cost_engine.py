from dataclasses import dataclass

@dataclass(frozen=True)
class CostConfig:
    brokerage_per_order: float
    brokerage_pct: float = 0.0
    brokerage_cap: float | None = None
    stt_delivery_buy: float = 0.001
    stt_delivery_sell: float = 0.001
    stt_intraday_sell: float = 0.00025
    stamp_delivery_buy: float = 0.00015
    stamp_intraday_buy: float = 0.00003
    sebi_turnover: float = 0.000001
    exchange_txn: float = 0.0000307
    gst: float = 0.18
    spread_bps_per_leg: float = 0.0
    slippage_bps_per_leg: float = 0.0
    dp_charge_per_delivery_sell: float = 0.0


def brokerage(value: float, cfg: CostConfig) -> float:
    fee = max(cfg.brokerage_per_order, value * cfg.brokerage_pct)
    return min(fee, cfg.brokerage_cap) if cfg.brokerage_cap is not None else fee


def leg_cost(value: float, side: str, mode: str, cfg: CostConfig):
    brokerage_fee = brokerage(value, cfg)
    sebi = value * cfg.sebi_turnover
    exchange = value * cfg.exchange_txn
    if mode == 'delivery':
        stt = value * (cfg.stt_delivery_buy if side == 'buy' else cfg.stt_delivery_sell)
        stamp = value * (cfg.stamp_delivery_buy if side == 'buy' else 0.0)
    else:
        stt = value * (cfg.stt_intraday_sell if side == 'sell' else 0.0)
        stamp = value * (cfg.stamp_intraday_buy if side == 'buy' else 0.0)
    gst = cfg.gst * (brokerage_fee + exchange + sebi)
    spread = value * cfg.spread_bps_per_leg / 10000.0
    slippage = value * cfg.slippage_bps_per_leg / 10000.0
    dp = cfg.dp_charge_per_delivery_sell if mode == 'delivery' and side == 'sell' else 0.0
    return {'brokerage': brokerage_fee, 'sebi': sebi, 'exchange': exchange, 'stt': stt,
            'stamp': stamp, 'gst': gst, 'spread': spread, 'slippage': slippage, 'dp': dp}


def round_trip_cost(buy_value: float, sell_value: float, mode: str, cfg: CostConfig):
    buy = leg_cost(buy_value, 'buy', mode, cfg)
    sell = leg_cost(sell_value, 'sell', mode, cfg)
    out = {key: buy[key] + sell[key] for key in buy}
    out['total'] = sum(out.values())
    return out


def net_pnl(gross_pnl: float, buy_value: float, sell_value: float, mode: str, cfg: CostConfig) -> float:
    return gross_pnl - round_trip_cost(buy_value, sell_value, mode, cfg)['total']
