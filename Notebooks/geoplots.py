import os
import zipfile

import geopandas as gpd
import geoviews as gv
import mapclassify
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import plots as p
from IPython.display import display
from shapely import wkt


def group_df(df):
    mea_data = pd.DataFrame(
        columns=["City", "Year", "Measure", "Value", "geometry"]
    )
    for measure in df["Measure"].unique():
        # Filter data for the current measure and aggregate by city and year, calculating the mean value for 'Value' and taking the first occurrence of 'geometry' and 'Measure' within each group
        df_mes = (
            df[df["Measure"] == measure]
            .groupby(["City", "Year"])
            .agg({"Value": "mean", "geometry": "first", "Measure": "first"})
            .reset_index()
        )

        # Append the aggregated data to mea_data
        mea_data = pd.concat([mea_data, df_mes], ignore_index=True)
    mea_data = gpd.GeoDataFrame(mea_data, geometry="geometry")
    return mea_data


def map_distribution(mea_data, measure):
    years = mea_data[mea_data["Measure"] == measure]["Year"].unique()
    # If there are multiple years, plot multiple maps for each year in one axes
    if len(years) > 1:
        fig, axes = plt.subplots(1, len(years), figsize=(12, 6))
        for i, year in enumerate(years):
            ax = axes[i]
            data_year = mea_data[
                (mea_data["Measure"] == measure) & (mea_data["Year"] == year)
            ]
            data_year.plot(
                ax=ax,
                column="Value",
                legend=True,
                cmap="YlOrRd",
                scheme="natural_breaks",
                k=3,
                edgecolor="grey",
                linewidth=0.5,
                legend_kwds={
                    "fmt": "{:,.4f}",
                    "loc": "lower right",
                    "title_fontsize": "medium",
                    "fontsize": "small",
                    "markerscale": 0.5,
                },
            )
            ax.set_title(f"Measure: {measure}, Year: {year}")
            ax.set_xticks([])  # Remove xticks
            ax.set_yticks([])  # Remove yticks
        plt.show()
    # If there's only one year, plot a single map
    year = years[0]
    data_year = mea_data[
        (mea_data["Measure"] == measure) & (mea_data["Year"] == year)
    ]
    fig, ax = plt.subplots(figsize=(6, 6))
    data_year.plot(
        ax=ax,
        column="Value",
        legend=True,
        cmap="YlOrRd",
        scheme="natural_breaks",
        k=3,
        edgecolor="grey",
        linewidth=0.5,
        legend_kwds={
            "fmt": "{:,.4f}",
            "loc": "lower right",
            "title_fontsize": "medium",
            "fontsize": "small",
            "markerscale": 0.5,
        },
    )
    ax.set_title(f"Measure: {measure}, Year: {year}")
    ax.set_xticks([])  # Remove xticks
    ax.set_yticks([])  # Remove yticks
    plt.show()


def esri_map(data, measure):
    esri_world = gv.tile_sources.EsriImagery()
    ky_plot = data.hvplot(
        color="Value", alpha=1.0, clabel="Population %", hover_cols=["City"]
    ).opts(
        title=f"Population Into the Measure {measure}",
        xlabel="Longitude (deg)",
        ylabel="Latitude (deg)",
        data_aspect=1,
        show_grid=True,
        height=480,
        width=720,
    )

    display(esri_world * ky_plot)


def max_measure(mea_data, max_values, year):
    fig, ax = plt.subplots(figsize=(10, 6))
    mea_data.plot(ax=ax, color="lightgrey", edgecolor="black", alpha=0.5)

    # Plot the max values with red color
    max_values.plot(ax=ax, color="red", markersize=50)
    # Annotate each marker with the corresponding measure name
    for idx, row in max_values.iterrows():
        ax.annotate(
            row["Measure"],
            xy=(row.geometry.centroid.x, row.geometry.centroid.y),
            xytext=(3, 3),  # Offset for the text
            textcoords="offset points",
            fontsize=8,
            color="black",
            ha="left",
        )

    plt.title(f"Max Values by Measure for the year {year}")

    plt.show()
