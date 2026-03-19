# Specialty Packaging Corporation (SPC) — Demand Forecasting Report

## 1. Introduction

Specialty Packaging Corporation (SPC) manufactures recyclable/disposable food containers from polystyrene resin. The company produces two product types — **clear plastic** and **black plastic** containers — each with distinct seasonal demand patterns. This report presents a quarterly demand forecast for Years 6 through 8, developed using 5 years of historical demand data (Table 6-4).

---

## 2. Data Analysis

### 2.1 Historical Demand Summary (000 lb)

| Year | Quarter | Black Plastic | Clear Plastic |
|------|---------|--------------|---------------|
| 1    | I       | 2,250        | 3,200         |
| 1    | II      | 1,737        | 7,658         |
| 1    | III     | 2,412        | 4,420         |
| 1    | IV      | 7,269        | 2,384         |
| 2    | I       | 3,514        | 3,654         |
| 2    | II      | 2,143        | 8,680         |
| 2    | III     | 3,459        | 5,695         |
| 2    | IV      | 7,056        | 1,953         |
| 3    | I       | 4,120        | 4,742         |
| 3    | II      | 2,766        | 13,673        |
| 3    | III     | 2,556        | 6,640         |
| 3    | IV      | 8,253        | 2,737         |
| 4    | I       | 5,491        | 3,486         |
| 4    | II      | 4,382        | 13,186        |
| 4    | III     | 4,315        | 5,448         |
| 4    | IV      | 12,035       | 3,485         |
| 5    | I       | 5,648        | 7,728         |
| 5    | II      | 3,696        | 16,591        |
| 5    | III     | 4,843        | 8,236         |
| 5    | IV      | 13,097       | 3,316         |

### 2.2 Key Observations

1. **Upward Trend**: Both product types show consistently increasing demand over the five-year period. Annual totals for black plastic grew from 13,668 (Year 1) to 27,284 (Year 5). Clear plastic grew from 17,662 (Year 1) to 35,871 (Year 5).

2. **Strong Seasonality**:
   - **Black plastic** demand peaks sharply in **Quarter IV (fall)** and is lowest in Quarter II.
   - **Clear plastic** demand peaks in **Quarter II (summer)** and is lowest in Quarter IV.

3. **Growing Seasonal Amplitude**: The magnitude of seasonal peaks increases over time (e.g., black Q4 went from 7,269 to 13,097), indicating **multiplicative** rather than additive seasonality.

---

## 3. Forecasting Method Selection

### 3.1 Method Chosen: Multiplicative Seasonal Decomposition with Linear Trend

### 3.2 Justification

The following methods were considered:

| Method | Suitable? | Reason |
|--------|-----------|--------|
| Simple Moving Average | No | Cannot capture trend or seasonality |
| Simple Exponential Smoothing | No | Handles level changes but ignores trend and seasonality |
| Holt's (Double Exponential Smoothing) | Partially | Captures trend but not seasonality |
| **Multiplicative Decomposition** | **Yes** | **Captures both linear trend and multiplicative seasonal patterns** |
| Additive Decomposition | No | Seasonal swings grow with demand level, so multiplicative is more appropriate |

**The multiplicative seasonal decomposition model** is selected because:

- The data clearly exhibits **both trend and seasonality** — two components that simpler methods cannot handle simultaneously.
- The seasonal fluctuations **grow proportionally** with the overall demand level, making a multiplicative model (Forecast = Trend × Seasonal Index) more appropriate than an additive model (Forecast = Trend + Seasonal Component).
- The method produces interpretable seasonal indices that can be communicated to production planners.
- Demand is expected to continue growing through Year 8, consistent with a linear trend assumption.

### 3.3 Methodology Steps

1. **Compute Centered Moving Average (CMA)**: A 4-quarter centered moving average smooths out seasonal fluctuations to reveal the underlying trend-cycle.
2. **Calculate Seasonal Ratios**: Divide actual demand by CMA to isolate the seasonal component (Ratio = Actual ÷ CMA).
3. **Determine Seasonal Indices**: Average the seasonal ratios for each quarter across all years, then normalize so they sum to 4.0.
4. **Deseasonalize the Data**: Divide actual demand by the corresponding seasonal index to remove seasonality.
5. **Fit Linear Trend**: Apply least-squares linear regression to the deseasonalized data (ŷ = a + b·t).
6. **Generate Forecasts**: Multiply the projected trend value by the appropriate seasonal index.

---

## 4. Results

### 4.1 Seasonal Indices

| Quarter | Black Plastic | Clear Plastic | Interpretation |
|---------|--------------|---------------|----------------|
| I       | 0.9362       | 0.7210        | Black near average; Clear below average |
| II      | 0.6113       | 1.9063        | Black low season; **Clear peak season** |
| III     | 0.6830       | 0.9487        | Both near/below average |
| IV      | 1.7695       | 0.4240        | **Black peak season**; Clear low season |
| **Sum** | **4.0000**   | **4.0000**    | Normalized |

**Interpretation**: A seasonal index of 1.7695 for Black Q4 means demand in Q4 is approximately 77% above the deseasonalized trend level. A seasonal index of 0.4240 for Clear Q4 means demand is approximately 58% below the trend level.

### 4.2 Linear Trend Equations (Deseasonalized)

| Product | Trend Equation | Interpretation |
|---------|---------------|----------------|
| Black Plastic | ŷ = 2,492 + 235.3·t | Base of 2,492; grows by ~235,000 lb per quarter |
| Clear Plastic | ŷ = 3,842 + 242.8·t | Base of 3,842; grows by ~243,000 lb per quarter |

Where *t* = time period (t = 1 for Year 1 Q1, t = 2 for Year 1 Q2, etc.)

### 4.3 Forecast Error Metrics (In-Sample Fit)

| Metric | Black Plastic | Clear Plastic |
|--------|--------------|---------------|
| MAE (000 lb) | 475 | 695 |
| RMSE (000 lb) | 592 | 920 |
| MAPE | 10.4% | 12.3% |

**Interpretation**: The model fits historical data with a mean absolute percentage error of approximately 10–12%, which is reasonable for demand forecasting with quarterly data. Users of these forecasts should expect actual demand to deviate from forecasted values by roughly this margin.

### 4.4 Quarterly Demand Forecasts — Years 6 to 8 (000 lb)

| Year | Quarter | Black Plastic | Clear Plastic | Total Demand |
|------|---------|--------------|---------------|-------------|
| **6** | **I**   | **6,959**    | **6,446**     | **13,405**  |
| 6    | II      | 4,687        | 17,504        | 22,191      |
| 6    | III     | 5,398        | 8,941         | 14,339      |
| 6    | IV      | 14,401       | 4,099         | 18,500      |
| **7** | **I**   | **7,840**    | **7,146**     | **14,986**  |
| 7    | II      | 5,263        | 19,355        | 24,618      |
| 7    | III     | 6,041        | 9,862         | 15,903      |
| 7    | IV      | 16,067       | 4,510         | 20,577      |
| **8** | **I**   | **8,721**    | **7,846**     | **16,567**  |
| 8    | II      | 5,838        | 21,206        | 27,044      |
| 8    | III     | 6,684        | 10,783        | 17,467      |
| 8    | IV      | 17,732       | 4,922         | 22,654      |

### 4.5 Annual Forecast Totals (000 lb)

| Year | Black Plastic | Clear Plastic | Total |
|------|--------------|---------------|-------|
| 6    | 31,445       | 36,990        | 68,435 |
| 7    | 35,211       | 40,873        | 76,084 |
| 8    | 39,975       | 44,757        | 84,732 |

---

## 5. Implications for SPC

1. **Production Planning**: The seasonal indices reveal that SPC must manage dramatically different demand profiles for the two products. Production scheduling should account for black plastic peaking in Q4 and clear plastic peaking in Q2.

2. **Inventory Build-Up**: Since extruder capacity is insufficient during peak seasons, SPC should plan inventory accumulation:
   - Build **clear plastic** sheet inventory in Q4 and Q1 (low demand) for the Q2 peak.
   - Build **black plastic** sheet inventory in Q2 and Q3 (low demand) for the Q4 peak.
   - The counter-cyclical nature of the two products is favorable — it allows the extruders to alternate between product types.

3. **Capacity Considerations**: Total demand is projected to reach nearly 85 million lb annually by Year 8. Management should evaluate whether current extruder and thermoforming capacity will be sufficient given this growth trajectory.

4. **Forecast Accuracy**: With MAPE of 10–12%, these forecasts provide directional guidance but should be updated regularly as new demand data becomes available. Collaborative forecasting with key customers (as proposed by the division manager) can further reduce forecast error.

---

## 6. Conclusion

Julie should recommend the **multiplicative seasonal decomposition with linear trend** method for SPC's demand forecasting. This method appropriately captures the two defining characteristics of SPC's demand data — steady growth and strong seasonal patterns with increasing amplitude. The resulting forecasts for Years 6–8 provide actionable planning targets for production scheduling, inventory management, and capacity planning. The expected forecast error (MAPE ~10–12%) is within acceptable ranges for this type of industrial demand forecasting.
