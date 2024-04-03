import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Load the data
clean_data = pd.read_csv('data/clean_data.csv')  # Update this path
nyc_boroughs = gpd.read_file('data/nyc_boroughs.geojson')
uhf42_geo_path = 'data/UHF42.geo.json'
uhf42_gdf = gpd.read_file(uhf42_geo_path)


def plot_average_levels(pollutant_name, legend_label):
    data = clean_data
    column_name = 'Data Value'
    pollutant_data = data[data['Name'] == pollutant_name]
    avg_pollutant_by_name = pollutant_data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
    merged_data = nyc_boroughs.merge(avg_pollutant_by_name, how='left', left_on='name', right_on='Geo Place Name')
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    merged_data.plot(column=column_name, ax=ax, legend=True, legend_kwds={'label': legend_label})
    title  = 'Average ' + pollutant_name + ' Levels by Borough in NYC'
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


def plot_average_levels_by_uhf42(pollutant_name, legend_label):
    data = clean_data[clean_data['Name'] == pollutant_name]
    avg_pollutant_by_uhf42 = data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
    merged_data = uhf42_gdf.merge(avg_pollutant_by_uhf42, how='left', left_on='GEONAME', right_on='Geo Place Name')
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    merged_data.plot(column='Data Value', ax=ax, legend=True, legend_kwds={'label': legend_label})
    title = 'Average ' + pollutant_name + ' Levels by UHF42 Area in NYC'
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


def plot_average_levels_by_season(pollutant_name, ylabel):
    data = clean_data[clean_data['Name'] == pollutant_name]
    data = data[data['Geo Type Name'] == 'Borough']
    avg_pollutant_by_season_borough = data.groupby(['Season', 'Geo Place Name'])['Data Value'].mean().reset_index()
    borough_order = avg_pollutant_by_season_borough.groupby('Geo Place Name')['Data Value'].mean().sort_values(ascending=False).index
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    sns.barplot(x='Geo Place Name', y='Data Value', hue='Season', data=avg_pollutant_by_season_borough, ax=ax, order=borough_order)
    title = 'Average ' + pollutant_name + ' Levels by Season and Borough in NYC'
    plt.title(title)
    plt.xlabel('Borough')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.show()

def plot_average_levels_by_year(pollutant_name, ylabel):
    data = clean_data[clean_data['Name'] == pollutant_name]
    avg_pollutant_by_year = data.groupby('Year')['Data Value'].mean().reset_index()
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    sns.lineplot(x='Year', y='Data Value', data=avg_pollutant_by_year, ax=ax, marker='o')
    title = 'Average ' + pollutant_name + ' Levels by Year in NYC'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.show()

def plot_average_levels_by_year(data_name, ylabel):
    data = clean_data[clean_data['Name'] == data_name]
    avg_data_by_year = data.groupby('Year')['Data Value'].mean().reset_index()
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    sns.barplot(x='Year', y='Data Value', data=avg_data_by_year, ax=ax)
    title = 'Average ' + data_name + ' by Year in NYC'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()

plot_average_levels_by_year('Asthma emergency department visits due to PM2.5', 'Average Asthma Emergency Department Visits')
plot_average_levels_by_year('Deaths due to PM2.5', 'Average Deaths')
plot_average_levels_by_year('Cardiovascular hospitalizations due to PM2.5 (age 40+)', 'Average Cardiovascular Hospitalizations')
plot_average_levels_by_year('Respiratory hospitalizations due to PM2.5 (age 20+)', 'Average Respiratory Hospitalizations')
plot_average_levels_by_year('Boiler Emissions- Total PM2.5 Emissions', 'Average Boiler Emissions')


# plot_average_levels_by_year('Fine particles (PM 2.5)', 'Average PM 2.5 Level (µg/m³)')
# plot_average_levels_by_year('Nitrogen dioxide (NO2)', 'Average NO2 Level (ppb)')
# plot_average_levels_by_year('Ozone (O3)', 'Average O3 Level (ppb')

# plot_average_levels_by_season('Nitrogen dioxide (NO2)', 'Average NO2 Level (ppb)')
# plot_average_levels_by_season('Fine particles (PM 2.5)', 'Average PM 2.5 Level (µg/m³)')

# plot_average_levels_by_uhf42('Nitrogen dioxide (NO2)', 'Average NO2 Level (ppb)')
# plot_average_levels_by_uhf42('Fine particles (PM 2.5)', 'Average PM 2.5 Level (µg/m³)')
# plot_average_levels_by_uhf42('Ozone (O3)', 'Average O3 Level (ppb)')


# plot_average_levels('Nitrogen dioxide (NO2)', 'Average NO2 Level (ppb)')
# plot_average_levels('Fine particles (PM 2.5)',  'Average PM 2.5 Level (µg/m³)')
# plot_average_levels('Ozone (O3)', 'Average O3 Level (ppb)')