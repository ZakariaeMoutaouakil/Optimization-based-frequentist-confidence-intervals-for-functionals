from typing import List


def quantile_1_minus_alpha(values: List[float], probabilities: List[float], alpha: float) -> float:
    """
    Calculate the quantile of order 1 - alpha for a discrete random variable with finite support.

    Args:
    - values (List[float]): List of values taken by the discrete random variable.
    - probabilities (List[float]): Corresponding probabilities of each value.
    - alpha (float): The significance level.

    Returns:
    - float: The quantile of order 1 - alpha.
    """

    # Combine values and probabilities, and sort them by value
    value_prob_pairs = sorted(zip(values, probabilities))

    cumulative_probability = 0.0
    quantile_threshold = 1 - alpha

    for value, prob in value_prob_pairs:
        cumulative_probability += prob
        if cumulative_probability >= quantile_threshold:
            return value

    # If the loop completes, return the last value
    return value_prob_pairs[-1][0]


if __name__ == "__main__":
    # Example usage
    vals = [1, 2, 3, 4, 5]
    probas = [0.1, 0.2, 0.3, 0.2, 0.2]
    risk = 0.5

    quantile = quantile_1_minus_alpha(vals, probas, risk)
    print(f"The quantile of order {(1 - risk) * 100:.0f}% is: {quantile}")
