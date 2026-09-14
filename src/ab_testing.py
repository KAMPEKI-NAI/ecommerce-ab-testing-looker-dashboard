import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def check_srm(control_count: int, treatment_count: int, expected_ratio: float = 0.50, alpha: float = 0.01) -> dict:
    """
    Performs a Chi-Square Goodness-of-Fit test to detect Sample Ratio Mismatch (SRM).
    """
    total = control_count + treatment_count
    expected_control = total * expected_ratio
    expected_treatment = total * (1.0 - expected_ratio)
    
    observed = np.array([control_count, treatment_count])
    expected = np.array([expected_control, expected_treatment])
    
    chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    has_srm = p_value < alpha
    
    return {
        "control_count": control_count,
        "treatment_count": treatment_count,
        "chi2_stat": chi2_stat,
        "p_value": p_value,
        "has_srm": has_srm,
        "status": "FAIL (SRM Detected)" if has_srm else "PASS (No SRM)"
    }


def evaluate_ab_test(trials_a: int, conversions_a: int, trials_b: int, conversions_b: int, alpha: float = 0.05) -> pd.DataFrame:
    """
    Evaluates a two-proportion Z-test and computes 95% Confidence Intervals.
    """
    cr_a = conversions_a / trials_a
    cr_b = conversions_b / trials_b
    absolute_lift = cr_b - cr_a
    relative_lift = (cr_b - cr_a) / cr_a

    count = np.array([conversions_b, conversions_a])
    nobs = np.array([trials_b, trials_a])
    z_stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')

    se_diff = np.sqrt((cr_a * (1 - cr_a) / trials_a) + (cr_b * (1 - cr_b) / trials_b))
    z_critical = stats.norm.ppf(1 - alpha / 2)
    ci_lower = absolute_lift - z_critical * se_diff
    ci_upper = absolute_lift + z_critical * se_diff

    return pd.DataFrame({
        "Metric": [
            "Sample Size", "Conversions", "Conversion Rate", 
            "Absolute Lift", "Relative Lift", "Z-Statistic", 
            "p-value", "95% CI Lower", "95% CI Upper", "Statistically Significant?"
        ],
        "Control (A)": [
            trials_a, conversions_a, f"{cr_a:.4%}", 
            "-", "-", "-", "-", "-", "-", "-"
        ],
        "Treatment (B)": [
            trials_b, conversions_b, f"{cr_b:.4%}", 
            f"{absolute_lift:+.4%}", f"{relative_lift:+.2%}", 
            f"{z_stat:.4f}", f"{p_value:.4f}", f"{ci_lower:+.4%}", f"{ci_upper:+.4%}", 
            str(p_value < alpha)
        ]
    })