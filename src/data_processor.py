import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from scipy.integrate import quad
import matplotlib.pyplot as plt


class DataProcessor:
    def __init__(self):
        self.data = None

    def load_data(self, data_path=None):
        """Load or generate sample data."""
        if data_path:
            self.data = pd.read_csv(data_path)
        else:
            # Generate sample data if no path is provided
            np.random.seed(42)
            n = 1000
            x = np.random.normal(0, 1, n)
            y = 2 * x + np.random.normal(0, 0.5, n)
            self.data = pd.DataFrame({"x": x, "y": y})
        return self.data

    def statistical_analysis(self):
        """Perform basic statistical analysis using SciPy."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load data first.")

        # Descriptive statistics
        stats_summary = {
            "mean_x": self.data["x"].mean(),
            "mean_y": self.data["y"].mean(),
            "std_x": self.data["x"].std(),
            "std_y": self.data["y"].std(),
        }

        # Correlation test
        correlation, p_value = stats.pearsonr(self.data["x"], self.data["y"])
        stats_summary["correlation"] = correlation
        stats_summary["p_value"] = p_value

        # Normality test
        _, p_norm_x = stats.normaltest(self.data["x"])
        _, p_norm_y = stats.normaltest(self.data["y"])
        stats_summary["normality_x"] = p_norm_x
        stats_summary["normality_y"] = p_norm_y

        return stats_summary

    def optimize_function(self, fn=lambda x: x[0] ** 2 + x[1] ** 2, x0=(1, 1)):
        """
        Optimize(minimize) input 2-dim function using SciPy's BFGS method.

        Args:
            fn (callable): The function to minimize.
            x0 (tuple): Initial guess for the variables.

        Returns:
            dict: A dictionary containing the optimization result.
        """
        result = minimize(fn, x0=[1, 1], method="BFGS")
        return {
            "success": result.success,
            "optimized_values": result.x.tolist(),
            "minimum_value": result.fun,
        }

    def numerical_integration(self, fn=lambda x: x**2, interval=(0, 1)):
        """
        Numerical integration of input function on interval.

        Args:
            fn (callable): The function to integrate.
            interval (tuple): The interval over which to integrate.

        Returns:
            dict: the integral value and error.
        """
        result, error = quad(fn, 0, 1)
        return {"integral_value": result, "error": error}

    def generate_plot(self, save_path="plot.png"):
        """Generate a plot of the data."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load data first.")

        plt.figure(figsize=(10, 6))
        plt.scatter(self.data["x"], self.data["y"], alpha=0.6)
        plt.title("Scatter Plot of Data")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.savefig(save_path)
        plt.close()
        return save_path

    def advanced_statistics(self):
        """Advanced statistical analysis."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load data first.")

        from scipy import stats

        # Perform additional statistical tests
        results = {
            "skewness_x": stats.skew(self.data["x"]),
            "skewness_y": stats.skew(self.data["y"]),
            "kurtosis_x": stats.kurtosis(self.data["x"]),
            "kurtosis_y": stats.kurtosis(self.data["y"]),
        }
        return results
