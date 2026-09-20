from research_cost_engine import CostConfig, round_trip_cost, net_pnl


def test_delivery_stt_on_both_sides():
    cfg = CostConfig(brokerage_per_order=20)
    costs = round_trip_cost(100000, 100000, 'delivery', cfg)
    assert abs(costs['stt'] - 200.0) < 1e-9
    assert abs(costs['stamp'] - 15.0) < 1e-9


def test_intraday_stt_only_sell_side():
    cfg = CostConfig(brokerage_per_order=20)
    costs = round_trip_cost(100000, 100000, 'intraday', cfg)
    assert abs(costs['stt'] - 25.0) < 1e-9
    assert abs(costs['stamp'] - 3.0) < 1e-9


def test_slippage_is_explicit():
    cfg = CostConfig(brokerage_per_order=20, spread_bps_per_leg=2.0, slippage_bps_per_leg=3.0)
    costs = round_trip_cost(100000, 100000, 'intraday', cfg)
    assert abs(costs['spread'] - 40.0) < 1e-9
    assert abs(costs['slippage'] - 60.0) < 1e-9


def test_net_pnl_is_gross_less_costs():
    cfg = CostConfig(brokerage_per_order=20)
    costs = round_trip_cost(100000, 100000, 'intraday', cfg)
    assert abs(net_pnl(1000, 100000, 100000, 'intraday', cfg) - (1000 - costs['total'])) < 1e-9
