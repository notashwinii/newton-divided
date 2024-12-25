
# Newton's Divided Difference Interpolation in Python
# This program demonstrates the implementation of Newton's divided difference interpolation 
# for estimating the value of a function at a given point.

# Function to calculate the divided differences table
def divided_difference_table(x, y):
    """
    Calculate the divided difference table.
    :param x: List of x-coordinates of data points.
    :param y: List of y-coordinates of data points (function values).
    :return: Divided difference table.
    """
    n = len(x)
    # Create a table initialized with zeros
    table = [[0 for _ in range(n)] for _ in range(n)]

    # The first column is filled with the given y values
    for i in range(n):
        table[i][0] = y[i]

    # Calculate divided differences
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])

    return table

# Function to perform Newton's interpolation
def newton_interpolation(x, y, value):
    """
    Perform Newton's divided difference interpolation.
    :param x: List of x-coordinates of data points.
    :param y: List of y-coordinates of data points (function values).
    :param value: The x-value at which interpolation is performed.
    :return: Interpolated value at the given x.
    """
    table = divided_difference_table(x, y)

    # Extract the first row (divided differences of order 0, 1, 2, ...)
    coeffs = [table[0][j] for j in range(len(x))]

    # Compute the interpolated value
    result = coeffs[0]
    product_term = 1
    for i in range(1, len(coeffs)):
        product_term *= (value - x[i - 1])
        result += coeffs[i] * product_term

    return result

# Main function to demonstrate the algorithm
def main():
    """Demonstrates Newton's divided difference interpolation."""
    print("Enter the data points (x and y) as space-separated values.")
    print("Example: For x = 5, 6, 9, 11 and y = 12, 13, 14, 16, input '5 6 9 11' and '12 13 14 16' respectively.")
    
    # Input x and y values from the user
    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != len(y):
        print("Error: The number of x and y values must be the same.")
        return

    # Input the value to interpolate
    value_to_interpolate = float(input("Enter the value of x to interpolate: "))

    # Perform interpolation
    interpolated_value = newton_interpolation(x, y, value_to_interpolate)

    print(f"The interpolated value at x = {value_to_interpolate} is {interpolated_value:.4f}")

# Run the program
if __name__ == "__main__":
    main()
