import matplotlib.pyplot as plt
from numpy import linspace

from lower_bound.generate_list import generate_list
from lower_bound.multinomial_max_cdf_inverse import multinomial_max_cdf_inverse


def get_quantile(alpha: float, q: float, n: int, m: int) -> float:
    """
    Calculate the lower bound of the maximum observed frequency.

    Parameters:
    alpha (float): The significance level.
    q (float): The expected probability for the first category.
    n (int): The total number of trials.

    Returns:
    float: The lower bound of the maximum observed frequency.
    """
    p = generate_list(m=m, q=q)
    quantile = multinomial_max_cdf_inverse(prob=1 - alpha, n=n, p=p)
    return quantile


if __name__ == "__main__":
    # Example usage:
    alpha_ = 0.05  # significance level
    q_ = 0.21  # expected probability for the first category
    n_ = 10  # total number of trials
    m_ = 5  # number of elements in the list

    lower_bound = get_quantile(alpha_, q_, n_, m_)
    print(f"Lower Bound: {lower_bound}")

    # Plotting the lower bound for different values of q
    q_values = linspace(0.21, 0.99, 10)
    lower_bounds = [get_quantile(alpha_, q, n_, m_) for q in q_values]

    plt.plot(q_values, lower_bounds, label=f'n={n_}')
    plt.xlabel('Expected Probability (q)')
    plt.ylabel('Lower Bound of Max Observed Frequency')
    plt.title('Lower Bound of Maximum Observed Frequency vs. Expected Probability')
    plt.legend()
    plt.grid(True)
    plt.show()
