########################################################################################################################
# IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT #
########################################################################################################################

# importing libraries
import plotly.graph_objects as go


########################################################################################################################
# CHART MAKE ### CHART MAKE ### CHART MAKE ### CHART MAKE #### CHART MAKE ### CHART MAKE ### CHART MAKE ### CHART MAKE #
########################################################################################################################

# Making CandleStick Chart
def chartMake(df, ticker, timeframe):
    # candles chart creating
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.Date,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )])

    # naming chart + vectors
    fig.update_layout(title=(ticker + "/USDT Chart (" + timeframe + ")"), height=800)

    # returning chart
    return fig


########################################################################################################################
# PRINT CANDLE INFO ##### PRINT CANDLE INFO ###### PRINT CANDLE INFO ####### PRINT CANDLE INFO ##### PRINT CANDLE INFO #
########################################################################################################################

# print candle info
def candleInfoPrint(date, open, close, color, percentage):
    print("---HOUR CANDLE---")
    print("Date: ", date)
    print("Open price: ", open)
    print("Close price: ", close)
    print("Candle color: ", color)
    print("Percentage: ", percentage, "(%)")
    print("-----------------")
    print()


########################################################################################################################
# PRINT WALLET CHANGE ### PRINT WALLET CHANGE #### PRINT WALLET CHANGE ### PRINT WALLET CHANGE ### PRINT WALLET CHANGE #
########################################################################################################################

# print wallet change
def walletChangePrint(wallet, invested_money, coins, average_price, number_purch, number_sales, number_leafs):
    print("| WALLET CHANGE")
    print("| Wallet:", wallet)
    print("| Invested money:", invested_money)
    print("| Coins:", coins)
    print("| Average price:", average_price)
    print("| Number of purchases:", number_purch)
    print("| Number of sales:", number_sales)
    print("| Number of leaf-purchases:", number_leafs)
    print()

########################################################################################################################
# END ## END ## END ## END ## END ## END ## END ## END ### END ## END ## END ## END ## END ## END ## END ## END ## END #
########################################################################################################################
