# MuNRa dataset schema report

**Important:** This report is *functional/technical* profiling only.
It does **not** assign physical meaning definitively. Any 'possible role' is a hypothesis.

- Rows: **304**
- Columns: **10**

## Column summary

| column | dtype | nunique | min | max | % zeros | monotonic | const/low-card | possible role (hypothesis) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| col_0 | int64 | 304 | 38 | 343 | 0.00% | monotonic_increasing | varies | counter or time-like variable (monotonic) |
| col_1 | int64 | 304 | 1.409e+04 | 1.265e+05 | 0.00% | monotonic_increasing | varies | counter or time-like variable (monotonic) |
| col_2 | int64 | 94 | 76 | 3962 | 0.00% | not_monotonic | varies | unknown |
| col_3 | int64 | 272 | 602 | 4095 | 0.00% | not_monotonic | varies | unknown |
| col_4 | float64 | 46 | 0.5 | 953.6 | 0.00% | not_monotonic | varies | unknown |
| col_5 | float64 | 71 | 7.298e+04 | 7.3e+04 | 0.00% | not_monotonic | varies | unknown |
| col_6 | float64 | 2 | 29.4 | 29.5 | 0.00% | not_monotonic | near_constant(nunique=2, range=0.1) | near-constant reading (low variation) |
| col_7 | int64 | 243 | 5301 | 1.494e+05 | 0.00% | not_monotonic | varies | unknown |
| col_8 | int64 | 1 | 0 | 0 | 100.00% | not_monotonic | constant(0) | constant sensor/setting (e.g., fixed parameter) |
| col_9 | object | 1 |  |  | n/a | n/a | constant(COSMIC) | label/type (constant category) |

## Notes / next steps

- If a column is monotonic increasing, it is often a counter or timestamp-like field.
- If a column is constant (or low-cardinality), it may be a fixed sensor reading or a configuration parameter.
- If a column is mostly zeros, it may be a flag/channel not used in this measurement setup.
- Definitive physical mapping should be done by comparing with device documentation and checking expected units/ranges.
