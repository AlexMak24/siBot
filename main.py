########################################################################################################################
# IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT #
########################################################################################################################

# importing libraries
import pandas as pd

# importing py files
from settings import *
from front import *
from structs import *
from orders import *

########################################################################################################################
# MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN ## MAIN #
########################################################################################################################

# defining using items
average_price = 0 if (coins == 0) else (invested_money / coins)
purchases = []
sales = []
leaf_purchases = []
wallet_empty_date = ""

# getting dataframe (historical prices)
data = pd.read_csv("/Users/timpiskarev/Documents/Projects/Trading/HistoricalPrices/"
                   + ticker + ":USDT/"
                   + time_frame + "/Binance_"
                   + ticker + "USDT_" + ("1" if time_frame == "hour" else "")
                   + time_frame[0] + ".csv"
                   )
data = data.head(candles)
dataFrame = data.astype({'Open': 'float', 'High': 'float', 'Low': 'float', 'Close': 'float', 'Volume USDT': 'float'})

# getting chart
chart = chartMake(dataFrame, ticker, time_frame)

########################################################################################################################
# ALGORITHM ## ALGORITHM ## ALGORITHM ### ALGORITHM ### ALGORITHM ### ALGORITHM ## ALGORITHM ## ALGORITHM ## ALGORITHM #
########################################################################################################################

# getting last price
last_price = dataFrame.iloc[0].Close

# going through all candles
for index, row in dataFrame[::-1].iterrows():

    # defining candle variables
    date_candle = row["Date"]
    open_candle = row["Open"]
    close_candle = row["Close"]
    percentage_candle = round(((close_candle - open_candle) / open_candle) * 100, 2)

    # defining candle color
    if open_candle > close_candle:
        color = "RED"
    else:
        color = "GREEN"

    # averageHard turn ON/OFF
    averageHard_button = ((close_candle < average_price) or (average_price == 0)) + abs(averageHard - 1)

    ##########################################
    # RED CANDLE ## RED CANDLE ## RED CANDLE #
    ##########################################
    if (color == "RED") and (wallet > (buy_sum * 2)) and averageHard_button:

        # call BUY function
        buy_check = BUY(date_candle, close_candle, buy_sum, ticker, (ticker + "/USDT"))

        # bought
        if buy_check == 1:

            # changing wallet info
            wallet -= buy_sum
            invested_money += buy_sum
            coins += (buy_sum / close_candle)
            average_price = invested_money / coins

            # creating new purchase
            new_purchase = Purchase(ticker,
                                    close_candle,
                                    (buy_sum / close_candle),
                                    buy_sum,
                                    fee,
                                    date_candle,
                                    (ticker + "/USDT"))

            # adding purchase to history
            purchases.append(new_purchase)

            # adding purchase to leaf-purchases
            leaf_purchases.append(new_purchase)

            # sorting leaf-purchases
            if leafsSort == 1:
                # new_list = sorted(inputList, key=lambda word: [alphabet.index(c) for c in word[0]])
                leaf_purchases = sorted(leaf_purchases)

            # adding arrow to the chart
            if chartArrowShow == 1:
                chart.add_annotation(x=date_candle, y=close_candle * 0.997, text="▲", showarrow=False,
                                     font=dict(size=15, color='darkgreen'))

            # text message
            print("BOUGHT")
            print()

            # printing wallet asset
            if walletChangeShow == 1:
                walletChangePrint(wallet,
                                  invested_money,
                                  coins, average_price,
                                  len(purchases),
                                  len(sales),
                                  len(leaf_purchases)
                                  )

        # not bought
        elif buy_check == 0:

            # text message
            print("I HAVE NOT BOUGHT")

    ################################################
    # GREEN CANDLE ## GREEN CANDLE ## GREEN CANDLE #
    ################################################
    elif color == "GREEN":

        # declaring selling purchases array
        selling_purchases = []

        # declaring sell check
        sell_check = 0

        # going through all leaf-purchases
        for purchase in leaf_purchases:

            # calculating difference between new price and bought price
            difference_percentage = ((close_candle - purchase.price) / purchase.price) * 100

            # leaf can be sold
            if difference_percentage > sell_percentage:

                # add leaf to selling purchases
                selling_purchases.append(purchase)

                # number of sales check
                if sellAll != 1 and sellNumber == len(selling_purchases):
                    # one purchase sell
                    break

        # declaring selling total + amount + average
        selling_total = 0
        selling_amount = 0
        selling_average = 0

        # counting selling total + amount + average
        for purchase in selling_purchases:
            selling_total += purchase.total
            selling_amount += purchase.amount
            selling_average = selling_total / selling_amount

        # call SELL function
        if len(selling_purchases) != 0:
            sell_check = SELL(date_candle, close_candle, selling_total, ticker, (ticker + "/USDT"))

        # SOLD
        if sell_check == 1:

            # changing wallet info
            wallet += selling_total
            invested_money -= selling_total
            coins -= (selling_total / close_candle)
            average_price = invested_money / coins

            # creating new sale
            new_sale = Sale(ticker,
                            close_candle,
                            (selling_total / close_candle),
                            selling_total,
                            fee,
                            date_candle,
                            (ticker + "/USDT"))

            # adding sale to history
            sales.append(new_sale)

            # deleting sold purchases
            for purchase in selling_purchases:
                leaf_purchases.remove(purchase)

            # adding arrow to the chart
            if chartArrowShow == 1:
                chart.add_annotation(x=date_candle,
                                     y=close_candle * 1.007,
                                     text="▼",
                                     showarrow=False,
                                     font=dict(size=15, color='darkred')
                                     )

            # adding number of sales to the chart
            if chartArrowShow == 1:
                chart.add_annotation(x=date_candle,
                                     y=close_candle * 1.013,
                                     text=str(len(selling_purchases)),
                                     showarrow=False,
                                     font=dict(size=10, color='black')
                                     )

            # text message
            print("SOLD")
            print("Income (coin): ", selling_amount - (selling_total / close_candle))
            print("Income (percentage): ",
                  round(((close_candle - selling_average) / selling_average) * 100, 2))
            print()

            # printing wallet asset
            if walletChangeShow == 1:
                walletChangePrint(wallet,
                                  invested_money,
                                  coins, average_price,
                                  len(purchases),
                                  len(sales),
                                  len(leaf_purchases)
                                  )

        # NOT SOLD
        elif sell_check == 0:

            # text message
            print("NOT SOLD")
            print()

    # print candle info
    if candlesInfoShow == 1:
        candleInfoPrint(date_candle, open_candle, close_candle, color, percentage_candle)

    # wallet empty check
    if wallet <= (buy_sum * 2):
        wallet_empty_date = date_candle
        print("!!! WALLET IS EMPTY !!")
        print()

########################################################################################################################
# PRINT DATA FRAME ## PRINT DATA FRAME ## PRINT DATA FRAME ## PRINT DATA FRAME ## PRINT DATA FRAME ## PRINT DATA FRAME #
########################################################################################################################

# print data frame
if dataFrameShow == 1:
    print(dataFrame)

########################################################################################################################
# PRINT WALLET ### PRINT WALLET ### PRINT WALLET #### PRINT WALLET #### PRINT WALLET ### PRINT WALLET ### PRINT WALLET #
########################################################################################################################

# declaring earned coins + money
income_coins = coins
income_money = 0

# calculating earned coins
for purchase in leaf_purchases:
    income_coins -= purchase.amount

# calculating earned money
income_money = income_coins * last_price

# wallet empty info
if wallet_empty_date == "":
    print("Wallet wasn't empty ever.")
    print()
else:
    print("Wallet was empty on: " + wallet_empty_date)
    print()

# print wallet asset
print("| WALLET INFO")
print("| ")
print("| Wallet:", wallet)
print("| Invested (money):", invested_money)
print("| Invested (percentage):", round((invested_money / (invested_money + wallet)) * 100, 2), "%")
print("| ")
print("| Coins:", coins)
print("| Current money:", coins * last_price)
print("| ")
print("| Income (coins):", income_coins)
print("| Income (money):", income_money)
print("| ")
print("| Average price:", average_price)
print("| ")
print("| Number of purchases:", len(purchases))
print("| Number of sales:", len(sales))
print("| Number of leaf-purchases:", len(leaf_purchases))
print("| ")
print("| Difference (percentage):", round((((coins * last_price - invested_money) / invested_money) * 100), 2), "%")
print("| Difference (dollar):", round(coins * last_price - invested_money, 2), "$")
print()

########################################################################################################################
# PRINT CHART ## PRINT CHART ## PRINT CHART ## PRINT CHART ## PRINT CHART ## PRINT CHART ## PRINT CHART ## PRINT CHART #
########################################################################################################################

# add level (average price) on chart
chart.add_trace(
    go.Scatter(
        x=dataFrame['Date'],
        y=[average_price] * candles,
        name="average price",
        mode="lines",
        line=dict(color='darkred', width=2)
    )
)

# draw left leafs (blue arrows)
if chartArrowShow == 1:
    for purchase in leaf_purchases:
        chart.add_annotation(x=purchase.date, y=purchase.price * 0.997, text="▲", showarrow=False,
                             font=dict(size=15, color='darkblue'))

# enable zoom
chart_config = dict({'scrollZoom': True})

# show chart (html)
chart.show(config=chart_config)

########################################################################################################################
# END ## END ## END ## END ## END ## END ## END ## END ### END ## END ## END ## END ## END ## END ## END ## END ## END #
########################################################################################################################
