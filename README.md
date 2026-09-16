# A/B Testing & Statistical Decision Framework: Landing Page Conversion Analysis

An end-to-end A/B testing project analyzing whether a new landing page design improves conversion rate over the existing control page. The analysis combines pre-experiment power analysis, a two-proportion z-test, and a business decision framework, visualized in an interactive Looker Studio dashboard.

## Project Overview

This project evaluates the statistical significance of a landing page redesign using real experiment data collected over 23 days. It walks through the full lifecycle of an A/B test — from calculating the required sample size before running the experiment, to validating the collected data against that requirement, to running the hypothesis test and translating the statistical result into a clear "launch / do not launch" business recommendation.

**Result:** The test failed to reach statistical significance (p = 0.1899, α = 0.05). The business recommendation is to **retain the control page** and not launch the treatment.

## Hypotheses

- **H₀ (Null):** The new page has no effect on conversion rate.
- **H₁ (Alternative):** The new page produces a statistically significant difference in conversion rate.

## Methodology

1. **Pre-Experiment Power Analysis**
   Calculated the minimum sample size required per group before data collection, using Cohen's h effect size for a baseline conversion rate of 12.0% and a minimum detectable effect of 0.35%, at α = 0.05 and 80% power. Required sample size: **137,015 users per group**.

2. **Sample Size Validation**
   Verified the collected dataset met or exceeded the required sample size before proceeding with the test (145,274 control / 145,310 treatment — sufficiently powered).

3. **Two-Proportion Z-Test**
   Ran a two-proportion z-test comparing conversion rates between control and treatment groups, with a 95% confidence interval on the difference in proportions.

4. **Business Decision Framework**
   Translated the statistical result into a plain-language recommendation, including next steps if the result is inconclusive or non-significant.

## Key Results

| Metric | Control (A) | Treatment (B) |
|---|---|---|
| Sample Size | 145,274 | 145,310 |
| Conversions | 17,489 | 17,264 |
| Conversion Rate | 12.0386% | 11.8808% |
| Absolute Lift | – | -0.1578% |
| Relative Lift | – | -1.31% |
| Z-Statistic | – | -1.3109 |
| p-value | – | 0.1899 |
| 95% CI | – | [-0.3938%, +0.0781%] |
| Statistically Significant? | – | No |

**Decision:** Fail to reject the null hypothesis. **Recommendation:** Do not launch the new page — no statistically significant lift detected. Retain control.

## Dashboard

An interactive Looker Studio dashboard visualizes the daily and cumulative conversion trends between groups, alongside the final statistical verdict:

- **KPI Scorecards** — Control rate, treatment rate, absolute lift, and p-value at a glance, each with a comparison-to-baseline indicator
- **Daily Conversion Rate** — time series comparing control vs. treatment conversion rate across the 23-day test window
- **Cumulative Conversion Rate** — shows how the test result stabilizes as sample size accumulates over time
- **Total Conversions by Group** — bar chart comparing raw conversion volume
- **Decision Banner** — plain-language recommendation and next steps, color-coded to the test outcome

## Project Structure

```
ecommerce-ab-testing-looker/
├── data/
│   ├── raw/                              # Original unprocessed data
│   └── processed/                        # Cleaned, user-level data used in the notebooks
├── EDA/
│   └── statistical_testing.ipynb         # Power analysis, z-test, decision framework
├── notebooks/
│   ├── eda_and_cleaning.ipynb            # Exploratory analysis and data cleaning
│   └── requirements.txt                  # Python dependencies
├── reports/
│   ├── ab_stats_summary.csv              # Wide-format stats summary (for dashboard scorecards)
│   └── ab_test_statistical_summary.csv   # Long-format statistical results export
├── src/
│   └── ab_testing.py                     # evaluate_ab_test() — z-test + CI calculation
├── debug.log
├── package.json
├── package-lock.json
└── README.md
```

## Tech Stack

- **Python** — pandas, numpy, statsmodels, scipy
- **Jupyter Notebook** — analysis and reporting
- **Google Looker Studio** — interactive dashboard

## How to Reproduce

1. Clone the repository and install dependencies:
   ```bash
   pip install -r notebooks/requirements.txt
   ```
2. Run `notebooks/eda_and_cleaning.ipynb` first to produce the cleaned, processed dataset.
3. Open `EDA/statistical_testing.ipynb` and run all cells in order. This will:
   - Run the pre-experiment power analysis
   - Load and validate the cleaned dataset
   - Execute the two-proportion z-test
   - Export the statistical summary to `reports/ab_test_statistical_summary.csv`
4. Import `reports/ab_stats_summary.csv` and `reports/ab_test_statistical_summary.csv` into Looker Studio to rebuild the dashboard.

## Key Takeaways

- A rigorous A/B test requires committing to a sample size **before** running the experiment (power analysis), not just testing until a result "looks" significant.
- Statistical significance and business impact are two different questions — this test was adequately powered and still returned a non-significant, slightly negative result, which is itself a valid and actionable outcome.
- "Do not launch" is not a failed experiment — it's a successful test that prevented shipping a change with no measurable benefit (and a point estimate that trended negative).

## Next Steps

- Re-run the test for a longer duration or with a larger minimum detectable effect threshold
- Test a different treatment variant
- Segment results by user cohort (e.g., device type, traffic source) to check for heterogeneous treatment effects masked in the aggregate result
