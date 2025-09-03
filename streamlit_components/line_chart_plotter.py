import pandas as pd
import altair as alt
import streamlit as st


class LineChartPlotter:
    """
    Generic multi-line chart plotter for time series data.
    
    Attributes:
        df (pd.DataFrame): DataFrame containing 'Date' column and numeric columns to plot.
    """

    def __init__(self, df: pd.DataFrame):
        if "Date" not in df.columns and 'date' not in df.columns:
            raise ValueError("DataFrame must contain a 'Date' column.")
        self.df = df.copy()
        self.df.columns = self.df.columns.str.replace('_', ' ').str.title()
        self.df["Date"] = pd.to_datetime(self.df["Date"])

    def _preprocess(self, value_cols=None, start_date=None, end_date=None) -> pd.DataFrame:
        df = self.df.copy()
        df["Weekday"] = df["Date"].dt.strftime("%A")
        if start_date:
            df = df[df["Date"] >= start_date]
        if end_date:
            df = df[df["Date"] <= end_date]

        # default: all numeric cols except Date
        value_cols = value_cols or [
            c for c in df.select_dtypes(include="number").columns if c != "Date"
        ]

        return df.melt(
            id_vars=["Date", "Weekday"],
            value_vars=value_cols,
            var_name="Metric",
            value_name="Value"
        )

    def plot(self, value_cols=None, start_date=None, end_date=None):
        """Plot interactive line chart with crosshairs and hover tooltips."""
        if self.df.empty:
            st.warning("No data available for the selected date range.")
            return
        value_cols = [col.replace('_', ' ').title() for col in value_cols]
        df_melt = self._preprocess(value_cols, start_date, end_date)
        if df_melt.empty:
            st.warning("No data available for given filters.")
            return

        hover = alt.selection_point(
            fields=["Date"], 
            nearest=True, 
            on="mouseover",
            # select="click",
            empty="none"
        )

        ymin, ymax = df_melt["Value"].min(), df_melt["Value"].max()
        y_pad = (ymax - ymin or 1) * 0.2
        y_domain = [ymin - y_pad, ymax + y_pad]

        # define padded x-axis domain
        x_min, x_max = df_melt["Date"].min(), df_melt["Date"].max()
        x_pad = (x_max - x_min) * 0.01
        x_domain = [x_min - x_pad, x_max + x_pad]

        line = alt.Chart(df_melt).mark_line().encode(
            x=alt.X("Date:T", scale=alt.Scale(domain=x_domain)),
            y=alt.Y("Value:Q", scale=alt.Scale(domain=y_domain)),
            color=alt.Color(
                "Metric:N",
                legend=alt.Legend(
                    orient="top-left", 
                    direction="horizontal",  # makes it horizontal
                    title=None           # optional: removes legend title
                )
            ),
            tooltip=["Date:T", "Weekday:N", "Metric:N", alt.Tooltip("Value:Q", format=".2f")]
        ).properties(
            width=1500,
            height=400,
        )

        points = line.mark_point(size=60).encode(
            opacity=alt.condition(hover, alt.value(1), alt.value(0))
        ).add_params(hover)

        text = line.mark_text(align="left", dx=5, dy=-5).encode(
            text=alt.condition(
                hover,
                alt.Text("Value:Q", format=".2f"),
                alt.value("")
            )
        )

        vline = alt.Chart(df_melt).mark_rule(color="gray").encode(
            x="Date:T"
        ).transform_filter(hover)

        hline = alt.Chart(df_melt).mark_rule(color="gray").encode(
            y="Value:Q"
        ).transform_filter(hover)

        chart = (line + points + text + vline + hline).interactive()
        chart = (
            chart
            .configure_view(stroke=None)
            .configure_axis(
                labelFontSize=12,
                titleFontSize=14,
                labelLimit=80
            )
            .configure(
                padding={"left": 60, "right": 20, "top": 20, "bottom": 30}  # force equal margins
            )
        )
                
        st.altair_chart(chart, use_container_width=True)



