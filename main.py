from joypy import joyplot
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def load_and_clean_data(file_path, dropna_columns):
    """
    Loads a CSV file and cleans NaN values based on specified columns.

    :param file_path: Path to the CSV file.
    :param dropna_columns: List of column names to drop NaN values from.
    :return: Cleaned DataFrame.
    """
    df = pd.read_csv(file_path)
    return df.dropna(subset=dropna_columns)


def filter_top_countries(df, country_column, top_n=10):
    """
    Filters the DataFrame to include only the top N unique countries.

    :param df: DataFrame to filter.
    :param country_column: Column name containing country data.
    :param top_n: Number of unique countries to include.
    :return: Filtered DataFrame.
    """
    top_countries = df[country_column].unique()[:top_n]
    return df[df[country_column].isin(top_countries)]


def plot_scatter():
    """
    Plots and saves as HTML a scatter (interactive)
    :return: None
    """

    # Load and clean dataset
    df_cleaned = load_and_clean_data(
        './datasets/energy-use-per-person.csv',
        ['Year', 'Primary energy consumption per capita (kWh/person)']
    )

    # Select a few countries for a better visualization
    df_filtered = filter_top_countries(df_cleaned, 'Entity')

    # Create a scatter plot
    fig = px.scatter(
        df_filtered,
        x='Year',
        y='Primary energy consumption per capita (kWh/person)',
        color='Entity',
        title='Primary Energy Consumption per Capita Over Time',
        labels={
            'Year': 'Year',
            'Primary energy consumption per capita (kWh/person)': 'Energy Consumption (kWh/person)',
            'Entity': 'Country'
        },
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    # Update traces
    fig.update_traces(marker=dict(size=10, opacity=0.7), selector=dict(mode='markers'))

    # Save as HTML
    fig.write_html("./views/scatter.html")


def plot_sunburst():
    """
    Plots and saves as HTML a Sunburst (interactive)
    :return: None
    """

    # Load and clean dataset
    df_cleaned = load_and_clean_data(
        './datasets/energy-use-per-person.csv',
        ['Year', 'Primary energy consumption per capita (kWh/person)']
    )

    # Add a new column for grouping by decade
    df_cleaned['decade'] = (df_cleaned['Year'] // 10) * 10

    # Select a few countries for a better visualization
    df_filtered = filter_top_countries(df_cleaned, 'Entity')

    # Group the dataframe by 'decade', 'Entity' and 'Primary energy consumption per capita (kWh/person)'
    df_grouped = df_filtered.groupby(
        ['decade', 'Entity']
    )['Primary energy consumption per capita (kWh/person)'].mean().reset_index()

    # Create the Sunburst plot
    fig = px.sunburst(df_grouped,
                      path=['decade', 'Entity'],
                      values='Primary energy consumption per capita (kWh/person)',
                      title="Primary Energy Consumption per Capita by Decade and Country",
                      color='Primary energy consumption per capita (kWh/person)',
                      template='plotly_white')

    # Save as HTML
    fig.write_html("./views/sunburst.html")


def plot_ridgeline():
    """
    Plots and saves as HTML a Ridgeline (no interactive)
    :return: None
    """

    # Load and clean dataset
    df_cleaned = load_and_clean_data('./datasets/lex.csv', ['country'])

    # Select 50 countries for a better visualization
    df_filtered = filter_top_countries(df_cleaned, 'country', top_n=50)

    # Melt df
    df_melted = df_filtered.melt(id_vars='country', var_name='year', value_name='lifeExp')

    # Create a Ridgeline plot
    joyplot(
        data=df_melted,
        by='country',
        column='lifeExp',
        title="Life Expectancy Distribution by Country",
        colormap=plt.cm.viridis,
        figsize=(17, 9),
        x_range=(df_melted['lifeExp'].min(), df_melted['lifeExp'].max()),
        fade=True,
        grid=True,
    )

    plt.xlabel("Life Expectancy")
    plt.ylabel("Country")
    plt.savefig("ridgeline.png")
    plt.close()

    # Save as HTML (rigid didn't find a proper way)
    with open("views/ridgeline.html", "w") as f:
        f.write('<html><body><img src="../ridgeline.png" alt="Ridgeline Plot"></body></html>')


if __name__ == '__main__':
    plot_scatter()
    plot_sunburst()
    plot_ridgeline()
