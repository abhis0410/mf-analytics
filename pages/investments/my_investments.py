import streamlit as st
import pandas as pd

from utils.data_loader import MyInvestmentsManager
from streamlit_components.dataframe import show_dataframe
from streamlit_components.line_chart_plotter import LineChartPlotter
from src.investment_metrics import merge_investment_with_nav, get_investment_metrics
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from streamlit_components.metrics import show_investment_metrics
from streamlit_components.groww_link_manager import GrowwLinkManager



def custom_plot(main_df):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
        subplot_titles=("Amount Invested", "NAV")
    )
    fig.add_trace(
        go.Scatter(
            x=main_df['date'],
            y=main_df['amount_invested'],
            name="Amount Invested",
            mode="lines",
            line=dict(width=2, color="#1f77b4"),
            marker=dict(size=6, color="#1f77b4", line=dict(width=1, color="white")),
            hovertemplate="Date: %{x|%Y-%m-%d}<br>Invested: %{y:,.0f}<extra></extra>"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=main_df['date'],
            y=main_df['nav'],
            name="NAV",
            mode="lines",
            line=dict(width=2, color="#ff7f0e"),
            marker=dict(size=6, color="#ff7f0e", line=dict(width=1, color="white")),
            hovertemplate="Date: %{x|%Y-%m-%d}<br>NAV: %{y:.2f}<extra></extra>"
        ),
        row=2, col=1
    )
    fig.update_layout(
        hovermode="x unified",   # 👈 crosshair vertical ruler + shared tooltip
        spikedistance=-1,        # ensures spike follows mouse
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_color="white"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.05,
            xanchor="left", x=0
        ),
        margin=dict(l=60, r=40, t=60, b=40),
    )
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",   # 👈 makes spike span all rows
        spikesnap="cursor",
        spikethickness=1.5,
        spikecolor="gray"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_plots(main_df, scheme_code):
    plot_type = st.radio("Choose Plot Type", ("Main", "Custom"), key=f"plot_type_{scheme_code}")
    if plot_type == "Main":
        plot_obj = LineChartPlotter(main_df)
        plot_obj.plot(
            value_cols=["amount_invested"]
        )
        plot_obj.plot(
            value_cols=["nav"]
        )
    elif plot_type == "Custom":
        custom_plot(main_df)

def show_scheme_wise_investments(scheme_code, invest_manager_obj : MyInvestmentsManager):
    all_investments = pd.DataFrame(invest_manager_obj.load_data())
    scheme_investments = all_investments[all_investments['scheme_code'] == scheme_code]

    if scheme_investments.empty:
        st.write("No investments found for this scheme.")
        return
    
    main_df = merge_investment_with_nav(scheme_investments, scheme_code)
    show_plots(main_df, scheme_code)

    st.divider()
    metrics = get_investment_metrics(scheme_code, scheme_investments)
    show_investment_metrics(metrics)


def show_all_investments(invest_manager_obj : MyInvestmentsManager):
    st.subheader("My Investments")
    all_investments = pd.DataFrame(invest_manager_obj.load_data())
    if all_investments.empty:
        st.info("No investments found.")
        return

    show_dataframe(all_investments)

    tabs = st.tabs([f"{code}" for code in all_investments['scheme_code'].unique()])
    for i, scheme_code in enumerate(all_investments['scheme_code'].unique()):
        scheme_name = all_investments[all_investments['scheme_code'] == scheme_code]['scheme_name'].iloc[0]
        with tabs[i]:
            st.subheader(f"{scheme_name} | {scheme_code}")
            GrowwLinkManager().add_groww_link(scheme_name=scheme_name)

            show_scheme_wise_investments(scheme_code, invest_manager_obj)


def main():
    invest_manager_obj = MyInvestmentsManager()
    
    st.divider()
    show_all_investments(invest_manager_obj)

    pass



if __name__ == "__main__":
    main()