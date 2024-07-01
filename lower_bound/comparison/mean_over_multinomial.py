from typing import Callable, Tuple

from numpy import random, mean, isclose


def mean_over_multinomial(f: Callable[[Tuple[float, ...]], float],
                          n: int,
                          p: Tuple[float, ...],
                          num_samples: int = 10000) -> float:
    """
    Computes the mean of a callable over a multinomial distribution.

    Parameters:
    - f: Callable[[Tuple[float, ...]], float] - function to compute the mean of
    - n: int - number of trials
    - p: Tuple[float, ...] - probabilities of each outcome (should sum to 1)
    - num_samples: int - number of samples to draw from the multinomial distribution

    Returns:
    - float - the mean of the callable over the multinomial distribution
    """
    # Check that the probabilities sum to 1
    assert isclose(sum(p), 1), "Probabilities must sum to 1"

    # Draw samples from the multinomial distribution
    samples = random.multinomial(n, p, size=num_samples)

    # Apply the function to each sample and compute the mean
    results = [f(tuple(sample)) for sample in samples]
    mean_value = mean(results)

    return mean_value


if __name__ == "__main__":
    # Example usage:
    # Define a simple function that takes a tuple and returns the sum of its elements
    def example_function(sample: Tuple[float, ...]) -> float:
        return sum(sample)


    # Number of trials
    n_ = 10
    # Probabilities for each outcome
    p_ = (0.2, 0.3, 0.5)

    # Compute the mean of the example_function over the multinomial distribution
    mean_result = mean_over_multinomial(example_function, n_, p_)
    print("Mean over multinomial distribution:", mean_result)
