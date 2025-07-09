from src.data_processor import DataProcessor
import json

def main():
    processor = DataProcessor()
    
    # Load or generate data
    data = processor.load_data()
    print(f"Data Loaded: {len(data)} points")
    
    # Perform statistical analysis
    stats_summary = processor.statistical_analysis()
    print("Statistical Analysis Summary:")
    print(json.dumps(stats_summary, indent=2))
    
    # Optimize a function
    optimization_result = processor.optimize_function()
    print("\nOptimization Result:")
    print(json.dumps(optimization_result, indent=2))
    
    # Perform numerical integration
    integration_result = processor.numerical_integration()
    print("\nNumerical Integration Result:")
    print(json.dumps(integration_result, indent=2))

    # Generate plot
    plot_path = processor.generate_plot()
    print(f"\nPlot saved to: {plot_path}")

if __name__ == "__main__":
    main()