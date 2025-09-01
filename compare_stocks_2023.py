#!/usr/bin/env python3
"""
Script to visualize and compare NVDA vs AMD stock performance in 2023
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def load_and_prepare_data():
    """Load the 2023 sample data and prepare for analysis"""
    
    # Load the 2023 sample data
    nvda_df = pd.read_csv('data/NVDA_2023_sample.csv')
    amd_df = pd.read_csv('data/AMD_2023_sample.csv')
    
    # Convert dates
    nvda_df['Date'] = pd.to_datetime(nvda_df['Date'])
    amd_df['Date'] = pd.to_datetime(amd_df['Date'])
    
    # Set date as index for easier plotting
    nvda_df.set_index('Date', inplace=True)
    amd_df.set_index('Date', inplace=True)
    
    return nvda_df, amd_df
        

def create_comparison_plots(nvda_df, amd_df):
    """Create comprehensive comparison plots"""
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('NVDA vs AMD Stock Performance Comparison - 2023', fontsize=16, fontweight='bold')
    
    # 1. Price Comparison (Close prices)
    ax1 = axes[0, 0]
    ax1.plot(nvda_df.index, nvda_df['Close'], label='NVDA', linewidth=2, color='#76B900')
    ax1.plot(amd_df.index, amd_df['Close'], label='AMD', linewidth=2, color='#ED1C24')
    ax1.set_title('Close Price Comparison', fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Volume Comparison
    ax2 = axes[0, 1]
    ax2.bar(nvda_df.index, nvda_df['Volume'] / 1e6, alpha=0.7, label='NVDA', color='#76B900')
    ax2.bar(amd_df.index, amd_df['Volume'] / 1e6, alpha=0.7, label='AMD', color='#ED1C24')
    ax2.set_title('Trading Volume Comparison', fontweight='bold')
    ax2.set_ylabel('Volume (Millions)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Daily Returns Comparison
    ax3 = axes[1, 0]
    nvda_returns = nvda_df['Close'].pct_change() * 100
    amd_returns = amd_df['Close'].pct_change() * 100
    
    ax3.plot(nvda_df.index[1:], nvda_returns[1:], label='NVDA', alpha=0.8, color='#76B900')
    ax3.plot(amd_df.index[1:], amd_returns[1:], label='AMD', alpha=0.8, color='#ED1C24')
    ax3.set_title('Daily Returns Comparison', fontweight='bold')
    ax3.set_ylabel('Daily Return (%)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Cumulative Returns Comparison
    ax4 = axes[1, 1]
    nvda_cumulative = (1 + nvda_returns/100).cumprod()
    amd_cumulative = (1 + amd_returns/100).cumprod()
    
    ax4.plot(nvda_df.index[1:], nvda_cumulative[1:], label='NVDA', linewidth=2, color='#76B900')
    ax4.plot(amd_df.index[1:], amd_cumulative[1:], label='AMD', linewidth=2, color='#ED1C24')
    ax4.set_title('Cumulative Returns Comparison', fontweight='bold')
    ax4.set_ylabel('Cumulative Return (1 = 100%)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Format x-axis dates
    for ax in axes.flat:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig


def main():
    """Main function to run the comparison analysis"""
    print("Loading 2023 stock data for comparison...")
    
    # Load data
    nvda_df, amd_df = load_and_prepare_data()
    
    if nvda_df is None or amd_df is None:
        print("Failed to load data. Please ensure the sample files exist.")
        return
    
    print("✓ Data loaded successfully!")
    
    # Create plots
    print("Creating comparison plots...")
    fig = create_comparison_plots(nvda_df, amd_df)
    
    # Save the plot
    plot_filename = "images/stocks_2023_comparison.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"✓ Plot saved as: {plot_filename}")
    
    # Show the plot
    plt.show()
    
if __name__ == "__main__":
    main()