import streamlit as st
from black_scholes import blackscholes, delta, gamma, vega, theta, rho

st.title("Black-Scholes Option Pricer")
st.write("Enter the option inputs below to calculate its value.")

# ---- Inputs ----
col1, col2 = st.columns(2)
with col1:
    S = st.number_input("Stock price (S)", value=30.0, min_value=0.01)
    K = st.number_input("Strike price (K)", value=40.0, min_value=0.01)
    days = st.number_input("Days to expiry", value=240, min_value=1)
with col2:
    r_pct = st.number_input("Risk-free rate (%)", value=1.0)
    sigma_pct = st.number_input("Volatility (%)", value=30.0, min_value=0.01)

# convert to the units the formula expects
T = days / 365
r = r_pct / 100
sigma = sigma_pct / 100

# ---- Prices ----
call_price = blackscholes(r, S, K, T, sigma, type="C")
put_price = blackscholes(r, S, K, T, sigma, type="P")

st.subheader("Option Values")
c1, c2 = st.columns(2)
c1.metric("Call value", f"${call_price:.2f}")
c2.metric("Put value", f"${put_price:.2f}")

# ---- Greeks ----
st.subheader("Greeks (call)")
g1, g2, g3, g4, g5 = st.columns(5)
g1.metric("Delta", f"{delta(r, S, K, T, sigma, 'C'):.4f}")
g2.metric("Gamma", f"{gamma(r, S, K, T, sigma):.4f}")
g3.metric("Vega (1%)", f"{vega(r, S, K, T, sigma)/100:.4f}")
g4.metric("Theta (day)", f"{theta(r, S, K, T, sigma, 'C')/365:.4f}")
g5.metric("Rho (1%)", f"{rho(r, S, K, T, sigma, 'C')/100:.4f}")