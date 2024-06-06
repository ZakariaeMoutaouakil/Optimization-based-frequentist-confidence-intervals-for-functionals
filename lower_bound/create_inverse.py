from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


def create_inverse(f: Callable[[float], float]) -> Callable[[float], float]:
    """
    Create the inverse of a non-decreasing function f.

    Parameters:
    f (Callable[[float], float]): A non-decreasing function from float (0, 1) to float.
    threshold (float): The point from which the function is non-decreasing.

    Returns:
    Callable[[float], float]: The inverse function of f.
    """

    def inverse(y: float, tol: float = 1e-5, max_iter: int = 100) -> float:
        """
        The inverse function using the bisection method.

        Parameters:
        y (float): The input value to the inverse function.
        tol (float): The tolerance level for the solution.
        max_iter (int): The maximum number of iterations for the bisection method.

        Returns:
        float: The output value from the inverse function.
        """

        # Ensure the input is within the expected range of the original function
        if y < f(0) or y > f(1):
            raise ValueError("Input is out of bounds for the inverse function.")

        # Define the bisection method
        def bisect_method(y_: float, a: float = 0, b: float = 1, tol_: float = tol, max_iter_: int = max_iter) -> float:
            fa, fb = f(a) - y_, f(b) - y_
            if fa * fb > 0:
                raise ValueError("The function must have different signs at a and b.")

            for _ in range(max_iter_):
                c = (a + b) / 2
                fc = f(c) - y_
                if np.abs(fc) < tol_:
                    return c
                if fa * fc < 0:
                    b, fb = c, fc
                else:
                    a, fa = c, fc
            return (a + b) / 2

        return bisect_method(y)

    return inverse


if __name__ == "__main__":
    # Example usage
    def example_function(x: float) -> float:
        return x ** 2 if x < 0.5 else 0.5 + (x - 0.5) * 2


    inv_function = create_inverse(example_function)

    # Test the inverse function and plot
    x_vals = np.linspace(0, 1, 100)
    y_vals = [example_function(x) for x in x_vals]
    x_inv_vals = [inv_function(y) for y in y_vals]

    # Plotting the original function and its inverse
    plt.figure(figsize=(12, 6))

    # Plot the original function
    plt.subplot(1, 2, 1)
    plt.plot(x_vals, y_vals, label='f(x)', color='blue')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Original Function')
    plt.legend()

    # Plot the inverse function
    plt.subplot(1, 2, 2)
    plt.plot(y_vals, x_inv_vals, label='f_inv(y)', color='red')
    plt.xlabel('y')
    plt.ylabel('f_inv(y)')
    plt.title('Inverse Function')
    plt.legend()

    plt.tight_layout()
    plt.show()
