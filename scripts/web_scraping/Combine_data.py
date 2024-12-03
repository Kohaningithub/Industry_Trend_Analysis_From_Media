import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
# Read a single file to check its structure
base_path = Path("/Users/kohanchen/Documents/Fall 2024/data315-au24/project/Final Project/Data")
sample_df = pd.read_excel(base_path / 'word_frequency_2015.xlsx')

# Display the first few rows and column names
print("Column names:", sample_df.columns.tolist())
print("\nFirst few rows:")
print(sample_df.head())

def combine_frequency_data(start_year=2015, end_year=2023):
    """
    Combine word frequency data from multiple years into a single DataFrame
    with proper date formatting
    """
    dfs = []
    base_path = Path("/Users/kohanchen/Documents/Fall 2024/data315-au24/project/Final Project/Data")
    
    for year in range(start_year, end_year + 1):
        file_path = base_path / f'word_frequency_{year}.xlsx'
        
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Melt the dataframe to convert months from columns to rows
        melted_df = df.melt(
            id_vars=['Word'],
            value_vars=[str(i) if isinstance(i, str) else i for i in range(1, 13)],
            var_name='month',
            value_name='frequency'
        )

        # Add year column
        melted_df['year'] = year

        dfs.append(melted_df)
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by date
    combined_df = combined_df.sort_values(['year', 'month', 'Word'])
    
    # Save to CSV
    output_path = base_path / 'combined_frequency_data.csv'
    combined_df.to_csv(output_path, index=False)
    print(f"\nSaved combined data to: {output_path}")
    print("\nSample of combined data:")
    
    return combined_df

# Execute the function
combined_data = combine_frequency_data()

# Print the first few rows to verify the format
print(combined_data.head())

def create_time_series_visualization(df):
    """
    Create time series visualization for sector attention over time
    """
    # Create a datetime column
    df['date'] = pd.to_datetime(df.apply(lambda x: f"{x['year']}-{x['month']}-01", axis=1))
    
    # Group by date and Word (sector) to get monthly totals
    monthly_trends = df.groupby(['date', 'Word'])['frequency'].sum().reset_index()
    
    fig = px.line(monthly_trends, 
                  x='date', 
                  y='frequency', 
                  color='Word',
                  title='Sector Attention Trends Over Time')
    
    # Add vertical line for March 2019
    fig.add_vline(
        x=pd.Timestamp('2019-03-01').timestamp() * 1000,  # Convert to milliseconds timestamp
        line_dash="dash", 
        line_color="red",
        annotation=dict(
            text="MIC2025 Mention Decrease",
            textangle=-90,
            yref="paper",
            y=1
        )
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Mention Frequency",
        legend_title="Sectors",
        # Improve readability
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        ),
        # Add some margin on the right for the legend
        margin=dict(r=150)
    )
    
    return fig


def create_heatmap_periods(df):
    """
    Create heatmap showing intensity of coverage across sectors and time
    """
    # Create year-month column for better visualization
    df['year_month'] = df.apply(lambda x: f"{x['year']}-{x['month']:02d}", axis=1)
    
    # Pivot data for heatmap
    pivot_df = df.pivot_table(
        index='Word', 
        columns='year_month', 
        values='frequency',
        aggfunc='sum'
    ).fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title='Sector Coverage Intensity Over Time',
        xaxis_title='Year-Month',
        yaxis_title='Sector',
        xaxis={'tickangle': 45}
    )
    
    return fig

def compare_periods(df):
    """
    Compare coverage patterns before and after March 2019
    """
    # Create datetime column if not exists
    if 'date' not in df.columns:
        df['date'] = pd.to_datetime(df.apply(lambda x: f"{x['year']}-{x['month']}-01", axis=1))
    
    # Split into before and after periods
    cutoff_date = pd.to_datetime('2019-03-01')
    before_period = df[df['date'] < cutoff_date].groupby('Word')['frequency'].mean()
    after_period = df[df['date'] >= cutoff_date].groupby('Word')['frequency'].mean()
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame({
        'Before March 2019': before_period,
        'After March 2019': after_period
    }).reset_index()
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(name='Before March 2019', x=comparison_df['Word'], y=comparison_df['Before March 2019']),
        go.Bar(name='After March 2019', x=comparison_df['Word'], y=comparison_df['After March 2019'])
    ])
    
    fig.update_layout(
        title='Average Monthly Mentions Before and After March 2019',
        xaxis_title='Sector',
        yaxis_title='Average Frequency',
        barmode='group'
    )
    
    return fig

# Example usage
if __name__ == "__main__":
    # Assuming df is your combined DataFrame
    base_path = Path("/Users/kohanchen/Documents/Fall 2024/data315-au24/project/Final Project/Data")
    df = pd.read_csv(base_path / 'combined_frequency_data.csv')
    # Create visualizations
    time_series = create_time_series_visualization(df)
    heatmap = create_heatmap_periods(df)
    comparison = compare_periods(df)
    
    # Show plots
    time_series.show()
    heatmap.show()
    comparison.show()