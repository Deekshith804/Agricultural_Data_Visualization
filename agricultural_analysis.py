import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class AgriculturalDataAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns
        
    def display_basic_info(self):
        print("=" * 50)
        print("AGRICULTURAL DATA ANALYSIS")
        print("=" * 50)
        print(f"Dataset Shape: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        print("\nFirst 5 rows:")
        print(self.df.head())
        
        print("\nDataset Information:")
        print(self.df.info())
        
        print("\nBasic Statistics for Numerical Columns:")
        print(self.df.describe())
        
        print("\nCategorical Variables Summary:")
        for col in self.categorical_cols:
            print(f"\n{col}:")
            print(self.df[col].value_counts())
    
    def analyze_crop_performance(self):
        print("\n" + "="*50)
        print("CROP PERFORMANCE ANALYSIS")
        print("="*50)
        
        # Yield by Crop Type
        crop_yield = self.df.groupby('Crop_Type')['Yield(kg/ha)'].agg(['mean', 'median', 'std'])
        crop_yield.columns = ['Average Yield', 'Median Yield', 'Yield Std Dev']
        print("\nYield by Crop Type (kg/ha):")
        print(crop_yield.round(2))
        
        # Profit by Crop Type
        crop_profit = self.df.groupby('Crop_Type')['Profit(USD/ha)'].agg(['mean', 'median', 'std'])
        crop_profit.columns = ['Average Profit', 'Median Profit', 'Profit Std Dev']
        print("\nProfit by Crop Type (USD/ha):")
        print(crop_profit.round(2))
        
        # Yield by Region
        region_yield = self.df.groupby('Region')['Yield(kg/ha)'].agg(['mean', 'median', 'std'])
        region_yield.columns = ['Average Yield', 'Median Yield', 'Yield Std Dev']
        print("\nYield by Region (kg/ha):")
        print(region_yield.round(2))
        
        # Yield by Farming Practice
        practice_yield = self.df.groupby('Farming_Practice')['Yield(kg/ha)'].agg(['mean', 'median', 'std'])
        practice_yield.columns = ['Average Yield', 'Median Yield', 'Yield Std Dev']
        print("\nYield by Farming Practice (kg/ha):")
        print(practice_yield.round(2))
    
    def analyze_sustainability(self):
        print("\n" + "="*50)
        print("SUSTAINABILITY ANALYSIS")
        print("="*50)
        
        # Carbon emissions by farming practice
        carbon_emissions = self.df.groupby('Farming_Practice')['Carbon_Emissions(kgCO2eq/ha)'].mean()
        print("Average Carbon Emissions by Farming Practice (kg CO2eq/ha):")
        print(carbon_emissions.round(2))
        
        # Biodiversity score by farming practice
        biodiversity = self.df.groupby('Farming_Practice')['Biodiversity_Score'].mean()
        print("\nAverage Biodiversity Score by Farming Practice:")
        print(biodiversity.round(2))
        
        # Water use efficiency by crop type
        water_efficiency = self.df.groupby('Crop_Type')['Water_Use_Efficiency(kg/L)'].mean()
        print("\nAverage Water Use Efficiency by Crop Type (kg/L):")
        print(water_efficiency.round(2))
    
    def analyze_correlations(self):
        print("\n" + "="*50)
        print("CORRELATION ANALYSIS")
        print("="*50)
        
        # Select only numerical columns for correlation
        numerical_df = self.df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numerical_df.corr()
        
        # Find top correlations with yield
        yield_correlations = corr_matrix['Yield(kg/ha)'].sort_values(ascending=False)
        print("Correlations with Yield:")
        for idx, value in yield_correlations.items():
            if idx != 'Yield(kg/ha)':  # Skip self-correlation
                print(f"{idx}: {value:.3f}")
        
        # Find top correlations with profit
        profit_correlations = corr_matrix['Profit(USD/ha)'].sort_values(ascending=False)
        print("\nCorrelations with Profit:")
        for idx, value in profit_correlations.items():
            if idx != 'Profit(USD/ha)':  # Skip self-correlation
                print(f"{idx}: {value:.3f}")
    
    def create_visualizations(self):
        print("\n" + "="*50)
        print("CREATING VISUALIZATIONS")
        print("="*50)
        
        # Create outputs directory if it doesn't exist
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        
        # Set up the figure
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Agricultural Data Analysis', fontsize=16)
        
        # Plot 1: Yield by Crop Type
        crop_yield = self.df.groupby('Crop_Type')['Yield(kg/ha)'].mean().sort_values(ascending=False)
        axes[0, 0].bar(crop_yield.index, crop_yield.values)
        axes[0, 0].set_title('Average Yield by Crop Type')
        axes[0, 0].set_ylabel('Yield (kg/ha)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Profit by Region
        region_profit = self.df.groupby('Region')['Profit(USD/ha)'].mean().sort_values(ascending=False)
        axes[0, 1].bar(region_profit.index, region_profit.values, color=['#4c72b0', '#55a868', '#c44e52', '#8172b2'])
        axes[0, 1].set_title('Average Profit by Region')
        axes[0, 1].set_ylabel('Profit (USD/ha)')
        
        # Plot 3: Carbon Emissions by Farming Practice
        practice_carbon = self.df.groupby('Farming_Practice')['Carbon_Emissions(kgCO2eq/ha)'].mean()
        axes[1, 0].bar(practice_carbon.index, practice_carbon.values, color=['#4c72b0', '#55a868', '#c44e52'])
        axes[1, 0].set_title('Carbon Emissions by Farming Practice')
        axes[1, 0].set_ylabel('CO₂ Emissions (kg/ha)')
        
        # Plot 4: Soil pH Distribution
        axes[1, 1].hist(self.df['Soil_pH'], bins=20, edgecolor='black', alpha=0.7)
        axes[1, 1].set_title('Soil pH Distribution')
        axes[1, 1].set_xlabel('Soil pH')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('outputs/agricultural_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Visualizations saved as 'outputs/agricultural_analysis.png'")
        
        # Create a correlation heatmap
        numerical_df = self.df.select_dtypes(include=[np.number])
        plt.figure(figsize=(12, 10))
        corr_matrix = numerical_df.corr()
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Matrix of Numerical Variables')
        plt.tight_layout()
        plt.savefig('outputs/correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Correlation matrix saved as 'outputs/correlation_matrix.png'")
    
    def run_full_analysis(self):
        self.display_basic_info()
        self.analyze_crop_performance()
        self.analyze_sustainability()
        self.analyze_correlations()
        self.create_visualizations()
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE")
        print("="*50)
        print("Summary of key findings:")
        print("- The dataset contains information about 200 farms across 4 regions")
        print("- Various crop types are represented with different yield and profit levels")
        print("- Different farming practices show variations in sustainability metrics")
        print("- Check the generated visualizations for more insights")

# Main execution
if __name__ == "__main__":
    # Initialize the analyzer with CSV file
    analyzer = AgriculturalDataAnalyzer('Agri_data.csv')
    
    # Run the full analysis
    analyzer.run_full_analysis()