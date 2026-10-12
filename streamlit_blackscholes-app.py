import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from black_scholes import blackscholes, delta, gamma, vega, theta, rho

# ---- Page settings (must be the first Streamlit command) ----
st.set_page_config(page_title="Black-Scholes Pricer", page_icon="📈", layout="wide")

st.title("Black-Scholes Option Pricer")
st.caption("Price European options and explore how their value, Greeks and P&L respond to each input.")

# ---- Sidebar: option inputs ----
st.sidebar.header("Option inputs")
S = st.sidebar.number_input("Stock price (S)", value=30.0, min_value=0.01)
K = st.sidebar.number_input("Strike price (K)", value=40.0, min_value=0.01)
days = st.sidebar.number_input("Days to expiry", value=240, min_value=1)
r_pct = st.sidebar.number_input("Risk-free rate (%)", value=1.0)
sigma_pct = st.sidebar.slider("Volatility (%)", 1.0, 100.0, 30.0)

# ---- Sidebar: your position ----
st.sidebar.header("Your position")
call_purchase = st.sidebar.number_input("Call purchase price", value=0.50, min_value=0.0, step=0.05)
put_purchase = st.sidebar.number_input("Put purchase price", value=10.00, min_value=0.0, step=0.05)
contracts = st.sidebar.number_input("Number of contracts", value=1, min_value=1)

# convert to the units the formula expects
T = days / 365
r = r_pct / 100
sigma = sigma_pct / 100

# ---- Prices and P&L ----
call_price = blackscholes(r, S, K, T, sigma, "C")
put_price = blackscholes(r, S, K, T, sigma, "P")

# one contract = 100 shares
call_pnl = (call_price - call_purchase) * 100 * contracts
put_pnl = (put_price - put_purchase) * 100 * contracts

c1, c2 = st.columns(2)
c1.metric("Call value", f"${call_price:.2f}", delta=f"{call_pnl:+,.2f} P&L")
c2.metric("Put value", f"${put_price:.2f}", delta=f"{put_pnl:+,.2f} P&L")

tab1, tab2, tab3 = st.tabs(["Greeks", "Price heatmap", "Greek charts"])

# ---- Tab 1: Greeks ----
with tab1:
    def show_greeks(option_type, label):
        st.subheader(f"Greeks ({label})")
        g1, g2, g3, g4, g5 = st.columns(5)
        g1.metric("Delta", f"{delta(r, S, K, T, sigma, option_type):.4f}")
        g2.metric("Gamma", f"{gamma(r, S, K, T, sigma):.4f}")
        g3.metric("Vega (1%)", f"{vega(r, S, K, T, sigma)/100:.4f}")
        g4.metric("Theta (day)", f"{theta(r, S, K, T, sigma, option_type)/365:.4f}")
        g5.metric("Rho (1%)", f"{rho(r, S, K, T, sigma, option_type)/100:.4f}")

    show_greeks("C", "call")
    show_greeks("P", "put")

# ---- Tab 2: Value / P&L heatmap ----
with tab2:
    option_choice = st.radio("Option type", ["Call", "Put"], horizontal=True)
    option_type = "C" if option_choice == "Call" else "P"

    spots = np.linspace(S * 0.7, S * 1.3, 10)
    vols = np.linspace(max(sigma * 0.5, 0.01), sigma * 1.5, 10)
    spot_grid, vol_grid = np.meshgrid(spots, vols)
    prices = blackscholes(r, spot_grid, K, T, vol_grid, option_type)

    show_pnl = st.toggle("Show P&L instead of option value")
    purchase = call_purchase if option_type == "C" else put_purchase

    if show_pnl:
        z = (prices - purchase) * 100 * contracts
        colorscale = "RdYlGn"
        zmid = 0
        title = f"{option_choice} P&L by stock price and volatility"
    else:
        z = prices
        colorscale = "Viridis"
        zmid = None
        title = f"{option_choice} value by stock price and volatility"

    fig = go.Figure(go.Heatmap(
        z=z,
        x=np.round(spots, 2),
        y=np.round(vols * 100, 1),
        colorscale=colorscale,
        zmid=zmid,
        text=np.round(z, 2),
        texttemplate="%{text}",
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Stock price",
        yaxis_title="Volatility (%)",
        height=550,
    )
    st.plotly_chart(fig)

# ---- Tab 3: Greek charts ----
with tab3:
    greek = st.selectbox("Choose a Greek", ["Delta", "Gamma", "Vega", "Theta", "Rho"])
    spot_range = np.linspace(S * 0.5, S * 1.5, 200)

    def greek_values(option_type):
        if greek == "Delta":
            return delta(r, spot_range, K, T, sigma, option_type)
        if greek == "Gamma":
            return gamma(r, spot_range, K, T, sigma)
        if greek == "Vega":
            return vega(r, spot_range, K, T, sigma) / 100
        if greek == "Theta":
            return theta(r, spot_range, K, T, sigma, option_type) / 365
        if greek == "Rho":
            return rho(r, spot_range, K, T, sigma, option_type) / 100

    chart = pd.DataFrame(
        {"Call": greek_values("C"), "Put": greek_values("P")},
        index=np.round(spot_range, 2),
    )
    chart.index.name = "Stock price"
    st.line_chart(chart)
    

