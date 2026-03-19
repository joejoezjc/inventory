"""
Specialty Packaging Corporation (SPC) - Demand Forecasting
Case Study: Forecast quarterly demand for clear and black plastic containers
for Years 6 to 8 using multiplicative seasonal model with linear trend.

Method Selection: Multiplicative Seasonal Model with Linear Trend (Winters' method /
decomposition approach) is chosen because the data exhibits:
1. An upward linear trend over the 5-year period
2. Strong seasonal (quarterly) patterns that repeat each year
3. Seasonal amplitude that grows with the level (multiplicative seasonality)
"""

import numpy as np

# =============================================================================
# Historical Data (Table 6-4) - Demand in 000 lb
# =============================================================================
# Columns: Year, Quarter, Black Plastic Demand, Clear Plastic Demand

data = [
    (1, 1, 2250, 3200),
    (1, 2, 1737, 7658),
    (1, 3, 2412, 4420),
    (1, 4, 7269, 2384),
    (2, 1, 3514, 3654),
    (2, 2, 2143, 8680),
    (2, 3, 3459, 5695),
    (2, 4, 7056, 1953),
    (3, 1, 4120, 4742),
    (3, 2, 2766, 13673),
    (3, 3, 2556, 6640),
    (3, 4, 8253, 2737),
    (4, 1, 5491, 3486),
    (4, 2, 4382, 13186),
    (4, 3, 4315, 5448),
    (4, 4, 12035, 3485),
    (5, 1, 5648, 7728),
    (5, 2, 3696, 16591),
    (5, 3, 4843, 8236),
    (5, 4, 13097, 3316),
]

years = np.array([d[0] for d in data])
quarters = np.array([d[1] for d in data])
black_demand = np.array([d[2] for d in data], dtype=float)
clear_demand = np.array([d[3] for d in data], dtype=float)

# Time period index: 1 through 20
t = np.arange(1, 21, dtype=float)


def forecast_with_seasonal_decomposition(demand, name):
    """
    Multiplicative Seasonal Decomposition with Linear Trend.

    Steps:
    1. Compute 4-quarter centered moving average (CMA) to estimate trend-cycle
    2. Compute seasonal ratios (actual / CMA)
    3. Average seasonal ratios by quarter to get seasonal indices
    4. Normalize seasonal indices to sum to 4.0
    5. Deseasonalize data by dividing by seasonal indices
    6. Fit linear trend to deseasonalized data
    7. Forecast by multiplying trend projection by seasonal index
    """
    n = len(demand)

    # Step 1: Centered Moving Average (CMA)
    # 4-quarter MA then center by averaging two consecutive MAs
    cma = np.full(n, np.nan)
    for i in range(2, n - 1):
        # Centered 2x4 MA
        ma4_prev = np.mean(demand[i-2:i+2])
        ma4_next = np.mean(demand[i-1:i+3])
        cma[i] = (ma4_prev + ma4_next) / 2.0

    # Step 2: Seasonal ratios
    seasonal_ratios = demand / cma  # NaN where CMA is NaN

    # Step 3: Average seasonal ratios by quarter
    raw_indices = []
    for q in range(1, 5):
        mask = (quarters == q) & ~np.isnan(seasonal_ratios)
        raw_indices.append(np.mean(seasonal_ratios[mask]))

    # Step 4: Normalize so they sum to 4.0
    raw_sum = sum(raw_indices)
    seasonal_indices = [(idx / raw_sum) * 4.0 for idx in raw_indices]

    print(f"\n{'='*60}")
    print(f"  {name} Plastic Containers - Forecast Analysis")
    print(f"{'='*60}")
    print(f"\nSeasonal Indices:")
    for q in range(4):
        print(f"  Quarter {q+1}: {seasonal_indices[q]:.4f}")

    # Step 5: Deseasonalize
    deseasonalized = np.zeros(n)
    for i in range(n):
        q = quarters[i] - 1
        deseasonalized[i] = demand[i] / seasonal_indices[q]

    # Step 6: Linear regression on deseasonalized data
    # y = a + b*t
    t_mean = np.mean(t)
    d_mean = np.mean(deseasonalized)
    b = np.sum((t - t_mean) * (deseasonalized - d_mean)) / np.sum((t - t_mean)**2)
    a = d_mean - b * t_mean

    print(f"\nLinear Trend (deseasonalized): y = {a:.2f} + {b:.2f} * t")

    # Step 7: Compute fitted values and errors for accuracy assessment
    fitted = np.zeros(n)
    for i in range(n):
        q = quarters[i] - 1
        fitted[i] = (a + b * t[i]) * seasonal_indices[q]

    errors = demand - fitted
    mae = np.mean(np.abs(errors))
    mape = np.mean(np.abs(errors / demand)) * 100
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)

    print(f"\nForecast Error Metrics (in-sample):")
    print(f"  MAE  = {mae:.0f} (000 lb)")
    print(f"  RMSE = {rmse:.0f} (000 lb)")
    print(f"  MAPE = {mape:.1f}%")

    # Forecast Years 6-8 (t = 21 to 32)
    print(f"\nForecasted Demand (000 lb):")
    print(f"  {'Year':<6} {'Quarter':<9} {'Forecast':>10}")
    print(f"  {'-'*27}")

    forecasts = []
    for year in range(6, 9):
        for q in range(1, 5):
            t_future = (year - 1) * 4 + q
            trend_value = a + b * t_future
            forecast = trend_value * seasonal_indices[q - 1]
            forecasts.append((year, q, forecast))
            print(f"  {year:<6} {q:<9} {forecast:>10,.0f}")

    return seasonal_indices, a, b, forecasts, mae, mape, rmse


def main():
    print("=" * 60)
    print("  SPECIALTY PACKAGING CORPORATION (SPC)")
    print("  Quarterly Demand Forecasting - Years 6 to 8")
    print("=" * 60)

    print("\n" + "-" * 60)
    print("FORECASTING METHOD SELECTION")
    print("-" * 60)
    print("""
The data exhibits two key characteristics:
  1. TREND: Demand for both container types grows over the 5 years
  2. SEASONALITY: Strong quarterly patterns repeat each year
     - Black plastic: peaks in Q4 (fall), lowest in Q2
     - Clear plastic: peaks in Q2 (summer), lowest in Q4

Because the data has both trend and seasonality, simple methods like
moving averages or simple exponential smoothing are inadequate.

SELECTED METHOD: Multiplicative Seasonal Decomposition with Linear Trend

This method:
  - Separates the trend component from seasonal fluctuations
  - Uses multiplicative (not additive) seasonality because the
    seasonal swings grow proportionally with the trend level
  - Allows straightforward projection into future periods
  - Is appropriate when demand is expected to continue growing
    (as stated: growth expected through Year 8)
""")

    black_results = forecast_with_seasonal_decomposition(black_demand, "Black")
    clear_results = forecast_with_seasonal_decomposition(clear_demand, "Clear")

    # Summary table
    print(f"\n{'='*60}")
    print(f"  COMBINED FORECAST SUMMARY (000 lb)")
    print(f"{'='*60}")
    print(f"  {'Year':<6} {'Qtr':<5} {'Black':>10} {'Clear':>10} {'Total':>10}")
    print(f"  {'-'*43}")

    black_forecasts = black_results[3]
    clear_forecasts = clear_results[3]

    for i in range(len(black_forecasts)):
        year = black_forecasts[i][0]
        qtr = black_forecasts[i][1]
        b_val = black_forecasts[i][2]
        c_val = clear_forecasts[i][2]
        print(f"  {year:<6} {qtr:<5} {b_val:>10,.0f} {c_val:>10,.0f} {b_val+c_val:>10,.0f}")


if __name__ == "__main__":
    main()
