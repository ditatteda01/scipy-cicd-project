import pytest
import pandas as pd
import numpy as np
from src.data_processor import DataProcessor
import tempfile
import os

class TestDataProcessor:
    def setup_method(self):
        """Setup method to create a DataProcessor instance."""
        self.processor = DataProcessor()

    def test_load_data_default(self):
        """Test loading default sample data."""
        data = self.processor.load_data()
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 1000
        assert 'x' in data.columns
        assert 'y' in data.columns
        assert not data.isnull().any().any()

    def test_load_data_from_csv(self):
        """Test loading data from CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            # Generate sample data
            num_samples = 10
            np.random.seed(42)
            x = np.random.randint(-10, 10, num_samples)
            y = np.random.randint(-10, 10, num_samples)
            df = pd.DataFrame({
                'x': x,
                'y': y
            })
            df.to_csv(temp_file.name, index=False)
            temp_path = temp_file.name
        
        # Load the data using the processor
        try:
            data = self.processor.load_data(data_path=temp_path)
            assert len(data) == num_samples
            assert 'x' in data.columns
            assert 'y' in data.columns
            assert data['x'].tolist() == x.tolist()
            assert data['y'].tolist() == y.tolist()
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

    def test_statistical_analysis(self):
        """Test statistical analysis on loaded data."""
        self.processor.load_data()
        stats_summary = self.processor.statistical_analysis()

        required_keys = ['mean_x', 'mean_y', 'std_x', 'std_y', 'correlation', 'p_value', 'normality_x', 'normality_y']

        for key in required_keys:
            assert key in stats_summary
            assert isinstance(stats_summary[key], (float, int))

        assert stats_summary['correlation'] > 0.8 # Expecting a strong positive correlation for our generated data

    def test_statistical_analysis_no_data(self):
        """Test statistical analysis raises error when no data is loaded."""
        with pytest.raises(ValueError, match="Data not loaded. Please load data first."):
            self.processor.statistical_analysis()

    def test_optimize_function_default(self):
        """Test optimization of the default function."""
        result = self.processor.optimize_function()
        assert 'success' in result
        assert 'optimized_values' in result
        assert 'minimum_value' in result
        assert result['success'] is True
        # for x^2 + y^2, the minimum is at (0, 0)
        assert len(result['optimized_values']) == 2
        assert isinstance(result['minimum_value'], float)
        assert abs(result['optimized_values'][0]) < 1e-5
        assert abs(result['optimized_values'][1]) < 1e-5
        assert abs(result['minimum_value']) < 1e-10

    def test_optimize_function_custom(self):
        """Test optimization of a custom function."""
        # minimize the function f(x, y) = x^2 + 2y^2 - 4x - 4y
        # The minimum should be at (2, 1) with a minimum value of -6
        custom_function = lambda x: x[0]**2 + 2*x[1]**2 - 4*x[0] - 4*x[1]
        result = self.processor.optimize_function(fn=custom_function, x0=(3, 4))
        assert 'success' in result
        assert 'optimized_values' in result
        assert 'minimum_value' in result
        assert result['success'] is True
        # The minimum for the custom function should be at (2, 1)
        assert len(result['optimized_values']) == 2
        assert abs(result['optimized_values'][0] - 2) < 1e-5
        assert abs(result['optimized_values'][1] - 1) < 1e-5
        assert abs(result['minimum_value'] + 6) < 1e-10
        
    def test_numerical_integration_default(self):
        """Test numerical integration of the default function."""
        result = self.processor.numerical_integration()
        assert 'integral_value' in result
        assert 'error' in result
        # The integral of x^2 from 0 to 1 is 1/3
        assert abs(result['integral_value'] - (1/3)) < 1e-10
        assert isinstance(result['error'], float)
        assert result['error'] < 1e-10

    def test_numerical_integration_custom(self):
        """Test numerical integration of a custom function."""
        # Integrate f(x) = 2x from 0 to 1, which should yield 1
        custom_function = lambda x: 2 * x
        result = self.processor.numerical_integration(fn=custom_function, interval=(0, 1))
        assert 'integral_value' in result
        assert 'error' in result
        assert abs(result['integral_value'] - 1) < 1e-10
        assert isinstance(result['error'], float)
        assert result['error'] < 1e-10

    def test_generate_plot(self):
        """Test generating a plot from the loaded data."""
        self.processor.load_data()

        with tempfile.TemporaryDirectory() as temp_dir:
            plot_path = os.path.join(temp_dir, 'test_plot.png')
            # Generate the plot and save it to the temporary directory
            result_path = self.processor.generate_plot(save_path=plot_path)
            assert result_path == plot_path
            assert os.path.exists(result_path)
            assert os.path.getsize(result_path) > 0
    
    def test_generate_plot_no_data(self):
        """Test generating a plot raises error when no data is loaded."""
        with pytest.raises(ValueError, match="Data not loaded. Please load data first."):
            self.processor.generate_plot(save_path='test_plot.png')

    def test_advanced_statistics(self):
        """Test advanced statistical analysis."""
        self.processor.load_data()
        stats = self.processor.advanced_statistics()

        # Check if the summary contains expected keys
        required_keys = ['skewness_x',
                         'skewness_y',
                         'kurtosis_x',
                         'kurtosis_y']
        for key in required_keys:
            assert key in stats
            assert isinstance(stats[key], float)
