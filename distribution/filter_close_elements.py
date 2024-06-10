from typing import List

from tqdm import tqdm


def filter_close_elements(values: List[float], precision: float) -> List[float]:
    if not values:
        return []

    # Sort the input list to ensure close elements are adjacent
    values.sort()
    filtered_values = [values[0]]

    for value in tqdm(values[1:], desc="Filtering close elements"):
        if abs(value - filtered_values[-1]) >= precision:
            filtered_values.append(value)

    return filtered_values


if __name__ == "__main__":
    # Example usage
    input_list = [1.01, 1.02, 2.03, 2.05, 2.01, 3.0, 3.02]
    precision_ = 0.02
    result = filter_close_elements(input_list, precision_)
    print(result)  # Output will be a list of elements that are not too close to each other
