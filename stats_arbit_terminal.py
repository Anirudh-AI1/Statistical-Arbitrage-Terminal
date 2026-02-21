import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as statmodel


class stocks():
    def names(self):
        print()
        self.stock_A = input("ENTER THE TICKER FOR STOCK A : " )
        self.stock_B = input("ENTER THE TICKER FOR STOCK B : ")
        print()

    def fetching_Data(self):
        raw_df_A =yf.download(self.stock_A, period= '10y', progress= False )
        raw_df_B = yf.download(self.stock_B, period= '10y', progress= False)

        self.aligned_data = pd.concat([raw_df_A['Close'], raw_df_B['Close']], axis=1).dropna()

        self.aligned_data.columns = [self.stock_A, self.stock_B]

    def returns(self):
        
        self.vector_A = ((self.aligned_data[self.stock_A] - self.aligned_data[self.stock_A].shift(1)) / self.aligned_data[self.stock_A].shift(1)).dropna()

        self.vector_B = ((self.aligned_data[self.stock_B] - self.aligned_data[self.stock_B].shift(1)) / self.aligned_data[self.stock_B].shift(1)).dropna()
        
        return self.vector_A, self.vector_B
    
    def averages(self):

        self.mean_A = self.vector_A.mean()
        self.mean_B = self.vector_B.mean()

        return self.mean_A, self.mean_B
    
    def mean_centre(self):

        self.u = self.vector_A - self.mean_A
        self.v = self.vector_B - self.mean_B

        return self.u, self.v
    
    def dot_prod(self):
        self.dot_product = np.dot(self.u,self.v)
        return self.dot_product
    
    def L2_norms(self):

        self.norm_u = np.sqrt((self.u ** 2).sum())
        self.norm_v = np.sqrt((self.v ** 2).sum())

        return self.norm_u, self.norm_v
    
    def correlation(self):
        self.formula = self.dot_product/ (self.norm_u * self.norm_v)

        print(f"Correlation b/w : {self.stock_A} and {self.stock_B} implies to {self.formula.round(decimals = 5)}")
        print()
        return self.formula

    def plot_data(self):
        normalized_data = (self.aligned_data / self.aligned_data.iloc[0]) * 100

        normalized_data.plot(figsize=(10,6), title= f'Visualizing correlation of {self.formula.round(decimals = 5)} b/w {self.stock_A} and {self.stock_B}')
        plt.xlabel("Date")
        plt.ylabel("Normalized Growth (Starts at 100)")
        plt.grid(True)
        


class co_integration():
    def receive_names(self, ticker_1, ticker_2):
        self.stock_A = ticker_1
        self.stock_B = ticker_2
        print(f"Cointegration Engine loaded : {self.stock_A} and {self.stock_B}")
        print()

    def fetching_data(self):
        raw_df_A = yf.download(self.stock_A, period= '10y',progress=False)
        raw_df_B = yf.download(self.stock_B, period='10y', progress=False)

        self.aligned_Data= pd.concat([raw_df_A['Close'], raw_df_B['Close']], axis=1).dropna()

        self.aligned_Data.columns = [self.stock_A, self.stock_B]

        self.n = len(self.aligned_Data)

        print(f"Total synchronised Trading days (n): {self.n}")
        print("")

    def means(self):
        self.mean_A = self.aligned_Data[self.stock_A].mean()
        self.mean_B = self.aligned_Data[self.stock_B].mean()

        return self.mean_A, self.mean_B
    
    def mean_centre(self):
        self.u = self.aligned_Data[self.stock_A] - self.mean_A
        self.v = self.aligned_Data[self.stock_B] - self.mean_B

        return self.u, self.v
    
    def covariance(self):
        self.overlap = ((self.u * self.v) / self.n).sum()
        return self.overlap
    
    def variance_of_Stock_B(self):
        self.variance = ((self.v)**2 / self.n).sum()
        return self.variance
    
    def hedge_ratio(self):
        self.beta = self.overlap / self.variance
        print(f"You need {self.beta.round(decimals = 2)} shares of {self.stock_B} to hedge 1 share of {self.stock_A}")
        print("")
        return self.beta
    
    def intercept(self):
        self.alpha = self.mean_A - (self.beta * self.mean_B)
        return self.alpha
    
    def spread_vector(self):
        self.spread = (self.aligned_Data[self.stock_A] - ((self.aligned_Data[self.stock_B] * self.beta) + self.alpha))
        print(f"Spread for the last 10 days b/w {self.stock_A} and {self.stock_B} is :\n{self.spread.tail(10)}")
        print("")
        return self.spread
    
    def plot_spread(self, a, p, c):
        plt.figure()
        self.spread.plot(figsize =(12,6), label = "Spread")
        plt.title(f"Spread b/w {self.stock_A} and {self.stock_B}") 
        plt.xlabel('Date')
        plt.ylabel('Spread Value')
        plt.axhline(y = 0, color = 'red', linestyle = '--')
        text_str = f"ADF Stat: {a:.2f}\nP-Value: {p:.4f}\nCritical 5%: {c['5%']:.2f}"
        plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes, fontsize=10, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        plt.legend()
        plt.grid(True)
        
        
class mean_reversion_ADF():
    def adf_test(self, coint_Spread):
        self.spread = coint_Spread
        adf_stat, p_val, lags, obs, crit_val, icbest = statmodel.adfuller(self.spread)

        if p_val < 0.05:
            print(f"The p value for the trade is {p_val.round(decimals= 3)}, i.e. 95% certainty that the spread b/w {quant_engine.stock_A} and {quant_engine.stock_B} is stationary. ")
            print("")

        elif p_val >= 0.05:
            print(f"The p value : {p_val.round(decimals= 3)} is greater than 0.05, so the certainty of the spread being stationary is less. ")
            print("")
            
        if adf_stat< crit_val['5%']:
            print(f"{adf_stat.round(decimals= 3)} < {crit_val['5%']} proves that the further the spread wanders away from zero, the harder the math pulls it back.")
            print("")

        elif adf_stat >= crit_val['5%']:
            print(f"{adf_stat.round(decimals= 3)} >= {crit_val['5%']} proves that the mathematical bungee cord is not strong enough to pull the spread back.")   
            print("")

        return adf_stat, p_val, crit_val


class trade_signals():
    def rolling_window(self,spread_For_z, p_val):
        self.spread= spread_For_z
        self.rolling_window_spread = self.spread.rolling(window = 21)
        self.rolling_window_mean = self.rolling_window_spread.mean()
        self.rolling_window_std = self.rolling_window_spread.std()

        self.z_score = (self.spread - self.rolling_window_mean) / self.rolling_window_std
        self.z_score = self.z_score.dropna()

        current_z = self.z_score.iloc[-1]
        if p_val < 0.05:
            if current_z >=0.5:
                print(f"The z-score for {quant_engine.stock_A} and {quant_engine.stock_B} is = {current_z:.2f}. Which signifies that the relationship b/w them curently is in OVERBOUGHT condition")

            elif current_z<=-0.5:
                print(f"The z-score for {quant_engine.stock_A} and {quant_engine.stock_B} is = {current_z:.2f}. Which signifies that the relationship b/w them curently is in OVERSOLD condition") 

            else:
                print(f"The z-score for {quant_engine.stock_A} and {quant_engine.stock_B} is = {current_z:.2f}. The spread is in NEUTRAL range.")
        
        else:
            print(f"WARNING: The P-Value is {p_val:.3f} (> 0.05). The spread is NOT stationary. Z-Score is invalid. DO NOT TRADE.")

    def plot_z_score(self):
        plt.figure()
        self.z_score.plot(figsize = (12,6), label = "z-score", color ="blue")
        plt.title(f"Z-Score Trading Signals for {quant_engine.stock_A} and {quant_engine.stock_B}")
        plt.axhline(y = 2, color = 'red', linestyle = '--')
        plt.axhline( y = -2, color = 'green', linestyle = '--')
        plt.axhline( y = 0, color = 'black')
        plt.legend()
        

quant_engine = stocks()
integration_engine = co_integration()
test_engine = mean_reversion_ADF()
signal_engine = trade_signals()

# 2. Basic Data Prep
quant_engine.names()
quant_engine.fetching_Data()
quant_engine.returns()
quant_engine.averages()
quant_engine.mean_centre()
quant_engine.dot_prod()
quant_engine.L2_norms()
quant_engine.correlation()

# 3. Cointegration Math
integration_engine.receive_names(quant_engine.stock_A, quant_engine.stock_B)
integration_engine.fetching_data()
integration_engine.means()
integration_engine.mean_centre()
integration_engine.covariance()
integration_engine.variance_of_Stock_B()
integration_engine.hedge_ratio()
integration_engine.intercept()
integration_engine.spread_vector()

# 4. THE CRITICAL ORDER: Run the math test BEFORE plotting
# We capture the exported numbers in three new variables: a, p, c
a, p, c = test_engine.adf_test(integration_engine.spread)

# 5. NOW we plot, passing those numbers into the spread chart
quant_engine.plot_data()
integration_engine.plot_spread(a, p, c)
signal_engine.rolling_window(integration_engine.spread, p)
signal_engine.plot_z_score()

# 6. Master Switch
plt.show()