from joypy import joyplot
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


countries_by_continent = {
        "Africa": [
            "Angola", "Burundi", "Benin", "Burkina Faso", "Botswana", "Cameroon", "Congo", "Cote d'Ivoire", "Comoros",
            "Cape Verde", "Djibouti", "Eritrea", "Ethiopia", "Gabon", "Ghana", "Guinea", "Gambia", "Guinea-Bissau",
            "Equatorial Guinea", "Kenya", "Liberia", "Libya", "Lesotho", "Madagascar", "Malawi", "Mali", "Mauritania",
            "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Senegal", "Sierra Leone",
            "Somalia", "South Sudan", "Sao Tome and Principe", "Togo", "Uganda", "Zambia", "Zimbabwe", "Sudan"
            "Central African Republic", "Chad", "Egypt ", "Eswatini", "Seychelles", "South Africa", "Tanzania",
            "Tunisia", "Algeria"
        ],
        "Asia": [
            "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China",
            "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan",
            "Kyrgyzstan", "Lebanon", "Lao", "Malaysia", "Maldives", "Myanmar", "Mongolia", "Nepal", "North Korea",
            "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Sri Lanka", "Syria", "Tajikistan",
            "Turkmenistan", "Thailand", "Timor-Leste", "Turkey", "United Arab Emirates", "Uzbekistan", "Vietnam",
            "Yemen", "Kuwait", "Laos", "Singapore", "South Korea", "Taiwan"
        ],
        "Europe": [
            "Albania", "Andorra", "Austria", "Belgium", "Bulgaria", "Belarus", "Bosnia and Herzegovina", "Croatia",
            "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Switzerland",
            "Iceland", "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Monaco",
            "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
            "Russia", "San Marino", "Serbia", "Slovak Republic", "Slovenia", "Spain", "Sweden", "Ukraine",
            "UK"
        ],
        "North America": [
            "Canada", "United States", "Mexico", "Cuba", "Guatemala", "Honduras", "Jamaica", "Panama", "Dominica",
            "Haiti", "Dominican Republic", "Barbados", "Belize", "Saint Kitts and Nevis", "Saint Lucia", "Grenada",
            "Trinidad and Tobago", "Antigua and Barbuda", "Bahamas ", "Costa Rica", "El Salvador",
            "Nicaragua", "USA"
        ],
        "South America": [
            "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname",
            "Uruguay", "Venezuela"
        ],
        "Oceania": [
            "Australia", "New Zealand", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Palau", "Samoa",
            "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu", "Nauru", "Papua New Guinea"
        ]
    }


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


def add_continent_column(df, column, countries_by_continent):
    """
    Adds a 'continent' column to the dataframe by mapping countries to their continents.

    :param df: DataFrame with a column (country names).
    :param column: The countries name column.
    :param countries_by_continent: Dictionary with continents as keys and a list of countries as values.
    :return: DataFrame with the added 'continent' column.
    """
    # Map countries by continents
    country_to_continent = {}
    for continent, countries in countries_by_continent.items():
        for country in countries:
            country_to_continent[country] = continent

    # Replace 'country' column with 'continent' column
    df['continent'] = df[column].map(country_to_continent)

    return df


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

    # Map countries by continents
    df_cleaned = add_continent_column(df_cleaned, 'Entity', countries_by_continent)

    # Group year and continent to calculate the average energy consumption by continent and year
    df_avg_consumption_by_continent_per_year =\
        df_cleaned.groupby(
            ['Year', 'continent'],
            as_index=False)['Primary energy consumption per capita (kWh/person)'].mean()

    # Create a scatter plot for average consumption per continent
    fig = px.scatter(
        df_avg_consumption_by_continent_per_year,
        x='Year',
        y='Primary energy consumption per capita (kWh/person)',
        color='continent',
        title='Average Primary Energy Consumption per Capita by Continent Over Time',
        labels={
            'Year': 'Year',
            'Primary energy consumption per capita (kWh/person)': 'Energy Consumption (kWh/person)',
            'continent': 'Continent'
        },
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Set1
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
    df_cleaned = load_and_clean_data('./datasets/cwurData.csv', ['country', 'institution'])

    # Map countries by continents
    df_cleaned = add_continent_column(df_cleaned, 'country', countries_by_continent)

    # Group by continent, country, and count institutions
    df_grouped = df_cleaned.groupby(['continent', 'country'], as_index=False)['institution'].count()
    df_grouped.rename(columns={'institution': 'num_universities'}, inplace=True)

    # Create the Sunburst plot
    fig = px.sunburst(
        df_grouped,
        path=['continent', 'country'],
        values='num_universities',
        title='Universities per Country and Continent Distribution',
        color='num_universities',
        color_continuous_scale='viridis',
        template='plotly_white'
    )

    # Save as HTML
    fig.write_html("./views/sunburst.html")


def plot_ridgeline():
    """
    Plots and saves as HTML a Ridgeline (no interactive)
    :return: None
    """

    # Load and clean dataset
    df_cleaned = load_and_clean_data('./datasets/lex.csv', ['country'])

    # Map countries by continents
    df_cleaned = add_continent_column(df_cleaned, 'country', countries_by_continent)

    # Melt df (changing 'country' to 'continent')
    df_melted = df_cleaned.melt(id_vars='continent', var_name='year', value_name='lifeExp')

    # Convert 'lifeExp' to numeric, coercing errors to NaN
    df_melted['lifeExp'] = pd.to_numeric(df_melted['lifeExp'], errors='coerce')

    # Calculate the average life expectancy per continent and year
    df_avg_life_exp = df_melted.groupby(['continent', 'year'], as_index=False)['lifeExp'].mean()

    # Create a Ridgeline plot using continents
    joyplot(
        data=df_avg_life_exp,
        by='continent',
        column='lifeExp',
        title="Life Expectancy Distribution by Continent",
        colormap=plt.cm.viridis,
        figsize=(17, 9),
        x_range=(df_avg_life_exp['lifeExp'].min(), df_avg_life_exp['lifeExp'].max()),
        fade=True,
        grid=True,
    )

    plt.xlabel("Life Expectancy")
    plt.ylabel("Continent")
    plt.savefig("ridgeline.png")
    plt.close()

    # Save as HTML
    with open("views/ridgeline.html", "w") as f:
        f.write('<html><body><img src="../ridgeline.png" alt="Ridgeline Plot"><br></body></html>')


if __name__ == '__main__':
    plot_scatter()
    plot_sunburst()
    plot_ridgeline()
