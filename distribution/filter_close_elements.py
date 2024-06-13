from typing import Tuple

from tqdm import tqdm


def filter_close_elements(values: Tuple[float, ...], precision: float) -> Tuple[float, ...]:
    if not values:
        return ()

    # Sort the input list to ensure close elements are adjacent
    sorted_values = sorted(values)
    filtered_values = [sorted_values[0]]

    for value in tqdm(sorted_values[1:], desc="Filtering close elements"):
        if abs(value - filtered_values[-1]) >= precision:
            filtered_values.append(value)

    return tuple(filtered_values)


if __name__ == "__main__":
    # Example usage
    input_list = (1.01, 1.02, 2.03, 2.05, 2.01, 3.0, 3.02)
    precision_ = 0.02
    result = filter_close_elements(input_list, precision_)
    print(result)  # Output will be a tuple of elements that are not too close to each other
