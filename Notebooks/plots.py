import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio


def group_to_df(df, year):
    df2 = df.groupby(["State", "Category"]).agg({"Value": "mean"})
    result_2020 = pd.DataFrame(
        {
            "State": df2.index.get_level_values("State"),
            "Category": df2.index.get_level_values("Category"),
            "Mean Value": df2["Value"],
        }
    )
    # resetting the index
    df3 = result_2020.reset_index(drop=True)
    df3["Year"] = year
    return df3


def box_plot(df, column, values_column):
    group = df.groupby(column)
    tot_cat = len(group)
    fig, axes = plt.subplots(nrows=tot_cat, ncols=1, figsize=(8, 6 * tot_cat))
    for ax, (cat, group_data) in zip(axes, group):
        group_data.boxplot(column=values_column, ax=ax)
        ax.set_title(f"{cat}")
        ax.set_xlabel(column)
        ax.set_ylabel(values_column)
    plt.tight_layout()
    plt.show()


def cat_state_plot(category_data, category_name):
    trace = go.Bar(
        x=category_data.index,
        y=category_data["Value"],
        marker=dict(color="skyblue"),
    )

    layout = go.Layout(
        title=f"Average Value by State for Category {category_name}",
        xaxis=dict(title="State"),
        yaxis=dict(title="Mean Value"),
        margin=dict(l=50, r=50, t=50, b=100),
        xaxis_tickangle=-45,
    )

    fig = go.Figure(data=[trace], layout=layout)

    pio.show(fig)


def group_plot(df, index, column, values, cat):
    pivot_cat = df.pivot(index=index, columns=column, values=values)
    traces = []
    for year in pivot_cat.columns:
        trace = go.Bar(x=pivot_cat.index, y=pivot_cat[year], name=str(year))
        traces.append(trace)

    layout = go.Layout(
        title=f"Mean Value of Category {cat} for all States",
        xaxis=dict(title="State"),
        yaxis=dict(title="Values"),
        barmode="group",
        legend=dict(title="Year", orientation="h"),
    )

    fig = go.Figure(data=traces, layout=layout)

    fig.show()


def plot_line_chart(data):
    # Create traces for each line
    traces = []
    for i, measure in enumerate(data["Measure"].unique()):
        visible = True if i == 0 else False
        trace = go.Scatter(
            x=data[data["Measure"] == measure]["City"],
            y=data[data["Measure"] == measure]["Value"],
            mode="lines+markers",
            name=measure,
            marker=dict(color="blue"),
            visible=visible,
        )
        traces.append(trace)

    fig = go.Figure()
    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(
        title="Measure Values by City",
        xaxis=dict(title="City"),
        yaxis=dict(title="Value"),
        legend=dict(title="Measure"),
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": measure,
                        "method": "update",
                        "args": [
                            {
                                "visible": [
                                    m == measure
                                    for m in data["Measure"].unique()
                                ]
                            }
                        ],
                    }
                    for measure in data["Measure"].unique()
                ],
                "direction": "down",
                "showactive": True,
                "x": 1.05,
                "y": 1.8,
            }
        ],
        height=600,
        width=1000,
    )

    # Show the plot
    fig.show()
