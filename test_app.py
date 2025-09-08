import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the processed data
df = pd.read_csv("data/processed_sales_data.csv")

# Convert sales back to numeric
df["sales_numeric"] = df["sales"].replace(r'[\$,]', '', regex=True).astype(float)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")

# Unique regions
regions = df["region"].unique()

# Calculate global ranges for consistency
y_min, y_max = df["sales_numeric"].min(), df["sales_numeric"].max()
x_min, x_max = df["date"].min(), df["date"].max()

# Create stacked subplots (1 row per region, shared x-axis)
fig = make_subplots(
    rows=len(regions),
    cols=1,
    shared_xaxes=True,
    subplot_titles=[f"Region: {r}" for r in regions]
)

# Add line + vertical marker for each region
for i, region in enumerate(regions, start=1):
    region_data = df[df["region"] == region]

    # Line chart (no markers, just clean line)
    fig.add_trace(
        go.Scatter(
            x=region_data["date"],
            y=region_data["sales_numeric"],
            mode="lines",
            name=region
        ),
        row=i, col=1
    )

    # Add vertical line at Jan 15, 2021
    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="red",
        row=i, col=1
    )

    # Add a red marker dot + label at Jan 15 (if exists in dataset)
    if "2021-01-15" in region_data["date"].astype(str).values:
        sale_value = region_data.loc[
            region_data["date"] == "2021-01-15", "sales_numeric"
        ].values[0]
        fig.add_trace(
            go.Scatter(
                x=["2021-01-15"],
                y=[sale_value],
                mode="markers+text",
                text=["Price Increase"],
                textposition="top right",
                marker=dict(color="red", size=10, symbol="circle"),
                showlegend=False
            ),
            row=i, col=1
        )

# Update layout with uniform ranges
fig.update_layout(
    height=350 * len(regions),  # more height for clarity
    title="Pink Morsel Sales Before and After Price Increase (by Region)",
    xaxis=dict(range=[x_min, x_max]),  # uniform date range
    yaxis=dict(range=[y_min, y_max]),  # uniform sales range
)

# Build Dash app
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(
        children="Soul Foods: Pink Morsel Sales Visualizer",
        style={"textAlign": "center", "marginBottom": "20px"}
    ),
    dcc.Graph(id="sales-line-chart", figure=fig),
])

if __name__ == "__main__":
    app.run(debug=True)
