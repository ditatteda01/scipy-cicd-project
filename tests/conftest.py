import pytest
import numpy as np

@pytest.fixture
def sample_data():
    """
    - **Purpose:** This fixture is designed to provide consistent, reproducible sample numerical data
    for use in various test functions.

    - **Data Generation:** It generates a simple dataset (`x` and `y`) where 'y' has a linear
    relationship with 'x', disturbed by a small amount of random noise.
    Specifically:
        - 'x' values are drawn from a standard normal distribution (mean=0, std dev=1).
        - 'y' values are computed as `2 * x + noise`, where `noise` is also drawn from
        a normal distribution (mean=0, std dev=0.5).
    The use of `np.random.seed(42)` ensures that the generated data is identical
    every time the tests are run, guaranteeing test reproducibility.

    - **Usage:** Any test function (or other fixture) that needs this sample data should
    declare 'sample_data' as one of its parameters. Pytest will automatically
    detect this dependency and pass the dictionary returned by the fixture
    to the test function.

    Example:
    ```python
    def test_my_analysis_feature(sample_data):
        # sample_data will be a dictionary like {'x': np.array, 'y': np.array}
        x_data = sample_data['x']
        y_data = sample_data['y']
        # ... perform tests using x_data and y_data ...
    ```
    """
    np.random.seed(42)
    n = 100
    x = np.random.normal(0, 1, n)
    y = 2 * x + np.random.normal(0, 0.5, n)
    return {'x': x, 'y': y}