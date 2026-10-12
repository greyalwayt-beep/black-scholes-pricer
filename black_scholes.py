# Implementing the Black-Scholes formula in Python

import numpy as np
from scipy.stats import norm

# define variables
r = 0.01
S = 30
K = 40
T = 240/365
sigma = 0.30


def d1_d2(r, S, K, T, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return d1, d2


def blackscholes(r, S, K, T, sigma, type="C"):
    "Calculate Black-Scholes option price for call/put"
    d1, d2 = d1_d2(r, S, K, T, sigma)
    if type == "C":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    elif type == "P":
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)


def delta(r, S, K, T, sigma, type="C"):
    d1, d2 = d1_d2(r, S, K, T, sigma)
    if type == "C":
        return norm.cdf(d1)
    elif type == "P":
        return norm.cdf(d1) - 1


def gamma(r, S, K, T, sigma):
    d1, d2 = d1_d2(r, S, K, T, sigma)
    return norm.pdf(d1)/(S*sigma*np.sqrt(T))


def vega(r, S, K, T, sigma):
    d1, d2 = d1_d2(r, S, K, T, sigma)
    return S*norm.pdf(d1)*np.sqrt(T)


def theta(r, S, K, T, sigma, type="C"):
    d1, d2 = d1_d2(r, S, K, T, sigma)
    first_term = -S*norm.pdf(d1)*sigma/(2*np.sqrt(T))
    if type == "C":
        return first_term - r*K*np.exp(-r*T)*norm.cdf(d2)
    elif type == "P":
        return first_term + r*K*np.exp(-r*T)*norm.cdf(-d2)


def rho(r, S, K, T, sigma, type="C"):
    d1, d2 = d1_d2(r, S, K, T, sigma)
    if type == "C":
        return K*T*np.exp(-r*T)*norm.cdf(d2)
    elif type == "P":
        return -K*T*np.exp(-r*T)*norm.cdf(-d2)


if __name__ == "__main__":
    print("Call price:", round(blackscholes(r, S, K, T, sigma, "C"), 2))
    print("Put price:", round(blackscholes(r, S, K, T, sigma, "P"), 2))