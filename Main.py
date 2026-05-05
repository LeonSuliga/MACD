import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def calculate_ema(prices, period):
    prices = np.asarray(prices, dtype=np.float64)
    ema = np.zeros_like(prices)
    alpha = 2 / (period + 1)
    ema[0] = prices[0]
    for i in range(1, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
    return ema

def calculate_macd(prices):
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)
    return ema_12 - ema_26

def calculate_signal(macd_values):
    return calculate_ema(macd_values, 9)

def find_trade_signals(macd, signal):
    buy_signals = []
    sell_signals = []

    for i in range(1, len(macd)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
            buy_signals.append(i)
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
            sell_signals.append(i)

    return buy_signals, sell_signals

def simulate_investor(close_prices, buy_signals, sell_signals):
    capital = 1000
    shares = 0
    portfolio_value = []

    for i in range(len(close_prices)):
        price = close_prices[i]

        if i in buy_signals and capital > 0:
            shares = capital / price
            capital = 0
        elif i in sell_signals and shares > 0:
            capital = shares * price
            shares = 0

        portfolio_value.append(capital + shares * price)

    return portfolio_value

def find_trade_signals(macd, signal):
    buy_signals = []
    sell_signals = []
    for i in range(1, len(macd)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
            buy_signals.append(i)
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
            sell_signals.append(i)
    return buy_signals, sell_signals
matplotlib.use("TkAgg")

# Pobranie danych PZU z ostatnich 3 lat
pzu_recent = yf.download("PZU.WA", period="3y")
close_prices_recent = pzu_recent["Close"].dropna()

# Pobranie danych PZU z wcześniejszych 3 lat (od 6 do 3 lat temu)
end_date = datetime.today() - timedelta(days=3*365)
start_date = end_date - timedelta(days=3*365)
pzu_past = yf.download("PZU.WA", start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
close_prices_past = pzu_past["Close"].dropna()

# Obliczenie MACD i SIGNAL dla obu okresów
macd_recent = calculate_macd(close_prices_recent)
signal_recent = calculate_signal(macd_recent)
macd_past = calculate_macd(close_prices_past)
signal_past = calculate_signal(macd_past)

# Znalezienie sygnałów kupna i sprzedaży
buy_recent, sell_recent = find_trade_signals(macd_recent, signal_recent)
buy_past, sell_past = find_trade_signals(macd_past, signal_past)


fig, axs = plt.subplots(2, 2, figsize=(14, 10))

#WYKRES 1: MACD i SIGNAL dla ostatnich 3 lat
axs[0, 0].plot(pzu_recent.index, macd_recent, label="MACD", color="red", linestyle="--")
axs[0, 0].plot(pzu_recent.index, signal_recent, label="SIGNAL", color="green", linestyle="--")

# Oznaczenie sygnałów kupna i sprzedaży
axs[0, 0].scatter(pzu_recent.index[buy_recent], macd_recent[buy_recent], marker='x', color='blue', s=100, label="Kupno")
axs[0, 0].scatter(pzu_recent.index[sell_recent], macd_recent[sell_recent], marker='x', color='black', s=100, label="Sprzedaż")

axs[0, 0].set_title("PZU - MACD i SIGNAL 2022-2025")
axs[0, 0].set_xlabel("Data")
axs[0, 0].legend()
axs[0, 0].grid()

#WYKRES 2: Cena akcji PZU z sygnałami kupna/sprzedaży dla ostatnich 3 lat
axs[0, 1].plot(pzu_recent.index, close_prices_recent, label="Cena zamknięcia", color="blue", alpha=0.5)

axs[0, 1].scatter(pzu_recent.index[buy_recent], close_prices_recent.iloc[buy_recent], marker='o', color='green', s=100, label="Kupno")
axs[0, 1].scatter(pzu_recent.index[sell_recent], close_prices_recent.iloc[sell_recent], marker='o', color='red', s=100, label="Sprzedaż")

axs[0, 1].set_title("PZU - Cena akcji 2022-2025")
axs[0, 1].set_xlabel("Data")
axs[0, 1].set_ylabel("Cena")
axs[0, 1].legend()
axs[0, 1].grid()

#WYKRES 3: MACD i SIGNAL dla poprzednich 3 lat
axs[1, 0].plot(pzu_past.index, macd_past, label="MACD", color="red", linestyle="--")
axs[1, 0].plot(pzu_past.index, signal_past, label="SIGNAL", color="green", linestyle="--")

axs[1, 0].scatter(pzu_past.index[buy_past], macd_past[buy_past], marker='x', color='blue', s=100, label="Kupno")
axs[1, 0].scatter(pzu_past.index[sell_past], macd_past[sell_past], marker='x', color='black', s=100, label="Sprzedaż")

axs[1, 0].set_title("PZU - MACD i SIGNAL 2019-2022")
axs[1, 0].set_xlabel("Data")
axs[1, 0].legend()
axs[1, 0].grid()

#WYKRES 4: Cena akcji PZU z sygnałami kupna/sprzedaży dla poprzednich 3 lat
axs[1, 1].plot(pzu_past.index, close_prices_past, label="Cena zamknięcia", color="blue", alpha=0.5)

axs[1, 1].scatter(pzu_past.index[buy_past], close_prices_past.iloc[buy_past], marker='o', color='green', s=100, label="Kupno")
axs[1, 1].scatter(pzu_past.index[sell_past], close_prices_past.iloc[sell_past], marker='o', color='red', s=100, label="Sprzedaż")

axs[1, 1].set_title("PZU - Cena akcji 2019-2022")
axs[1, 1].set_xlabel("Data")
axs[1, 1].set_ylabel("Cena")
axs[1, 1].legend()
axs[1, 1].grid()

plt.tight_layout()
plt.show()

buy_recent, sell_recent = find_trade_signals(macd_recent, signal_recent)
buy_past, sell_past = find_trade_signals(macd_past, signal_past)


# symulacja portfolio
portfolio_recent = simulate_investor(close_prices_recent.values, buy_recent, sell_recent)
portfolio_past = simulate_investor(close_prices_past.values, buy_past, sell_past)
fig, axs = plt.subplots(2, 1, figsize=(12, 10))

#WYKRES 5: Portfolio (Ostatnie 3 lata)
axs[0].plot(close_prices_recent.index, portfolio_recent, label="Wartość portfela", color='blue')
axs[0].set_title("Symulacja inwestora - ostatnie 3 lata")
axs[0].set_xlabel("Data")
axs[0].set_ylabel("Wartość portfela (PLN)")
axs[0].legend()
axs[0].grid()
#WYKRES 6: Portfolio (Poprzednie 3 lata)
axs[1].plot(close_prices_past.index, portfolio_past, label="Wartość portfela", color='red')
axs[1].set_title("Symulacja inwestora - poprzednie 3 lata")
axs[1].set_xlabel("Data")
axs[1].set_ylabel("Wartość portfela (PLN)")
axs[1].legend()
axs[1].grid()

plt.tight_layout()
plt.show()
print(portfolio_recent[len(portfolio_recent)-1],"\n")
print(portfolio_past[len(portfolio_past)-1],"\n")
print("W ostatnich 3 latach",(len(buy_recent)+len(sell_recent))/2,"  ",len(buy_recent),"  ",len(sell_recent),"\n")
print("W poprzednich 3 latach",(len(buy_past)+len(sell_past))/2,"  ",len(buy_past), "   ",len(sell_past),"\n")
print(np.max(portfolio_recent),"\n")
print(np.max(portfolio_past),"\n")
