from typing import List


def vector_margins(vectors: List[List[float]]) -> List[float]:
    margins = []
    for vector in vectors:
        if len(vector) < 2:
            raise ValueError("Each vector must have at least two elements")

        sorted_vector = sorted(vector, reverse=True)
        max_value = sorted_vector[0]
        second_max_value = sorted_vector[1]
        margin = max_value / second_max_value
        margins.append(margin)

    return margins


if __name__ == "__main__":
    # Example usage:
    inputs = [
        [1.0, 3.0, 4.0],
        [7.0, 5.0, 2.0],
        [0.5, 0.2, 0.1],
        [10.0, 10.0, 9.9]
    ]

    margins_ = vector_margins(inputs)
    print(margins_)  # Output: [1.3333333333333333, 1.4, 2.5, 1.0101010101010102]
