from typing import List, Callable

from tqdm import tqdm


def margin_of_vector(numbers: List[float]) -> float:
    if len(numbers) < 2:
        raise ValueError("Each vector must have at least two elements")
    sorted_vector = sorted(numbers, reverse=True)
    return sorted_vector[0] / sorted_vector[1]


def second_largest(numbers: List[float]) -> float:
    if len(numbers) < 2:
        raise ValueError("List must contain at least two elements")
    sorted_vector = sorted(numbers, reverse=True)
    return sorted_vector[1]


def sort_callable_values(vectors: List[List[float]],
                         func: Callable[[List[float]], float],
                         debug: bool = False) -> List[float]:
    # Apply the callable to each vector and store the results in a list
    results = [func(vector) for vector in tqdm(vectors, desc="Evaluating images")]
    if debug:
        print("Results:", results)
    # Remove duplicates and sort the list of results
    sorted_results = sorted(set(results))
    return sorted_results


if __name__ == "__main__":
    # Example usage:
    vectors_ = [
        [2.0, 2.0, 1.0],
        [1.0, 1.0, 3.0],
        [4.0, 5.0, 6.0],
        [1.5, 2.5, 3.5]
    ]

    # Get the sorted list of values
    sorted_values = sort_callable_values(vectors_, margin_of_vector, debug=True)
    print("Margins:", sorted_values)  # Output will be: [6.0, 10.5, 15.0]

    # Get the sorted list of values
    sorted_values = sort_callable_values(vectors_, second_largest, debug=True)
    print("Second largest values:", sorted_values)  # Output will be: [6.0, 10.5, 15.0]
