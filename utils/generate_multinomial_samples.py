from typing import Tuple, Iterable

import numpy as np


def generate_multinomial_samples(n: int, p: Tuple[float, ...], size: int) -> Iterable[Tuple[int, ...]]:
    """
    Generate an iterable of tuples following a multinomial distribution.

    Parameters:
    - n: int, the number of trials.
    - p: list of floats, the probabilities of each outcome. The sum of p must be 1.
    - size: int, the number of samples to generate. Default is 1.

    Returns:
    - iterable of tuples, where each tuple represents the outcome counts of one sample.
    """
    # Generate the samples
    samples = np.random.multinomial(n, p, size)

    # Convert numpy array to an iterable of tuples
    return (tuple(sample) for sample in samples)


if __name__ == "__main__":
    n_ = 25
    p_ = (0.05, 0.05, 0.9)
    size_ = 100

    # Generate samples
    samples_iterable = generate_multinomial_samples(n_, p_, size_)

    # Print samples
    for samp in samples_iterable:
        print(samp, sorted(samp, reverse=True)[0] / n_)
