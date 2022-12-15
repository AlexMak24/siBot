
def dfPriceGet(ticker):
    # making pair
    pair = ticker + "USDT"

    # getting candles
    candles = session.query_kline(symbol=pair, interval="1h")

    # cutting extra info
    candles = candles['result']

    # transforming into Data Frame + cutting extra info
    dataFrame = pd.DataFrame(candles)
    dataFrame = dataFrame.iloc[:, :6]

    # renaming columns' names + removing first column
    dataFrame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    # recalculating time
    dataFrame.Time = pd.to_datetime(dataFrame.Time, unit='ms')

    # floating columns with numbers
    dataFrame = dataFrame.astype({'Open': 'float',
                                  'High': 'float',
                                  'Low': 'float',
                                  'Close': 'float',
                                  'Volume': 'float'})

    # adding new column "Date"
    dataFrame = dataFrame.assign(Date=lambda x: x.Time.dt.date)

    # return
    return dataFrame

Tim Piskarev, [15.12.2022 12:36]
# Making CandleStick Chart
def chartMake(df, ticker):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # candles chart creating
    candlesticks = go.Candlestick(
        x=df.Time,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
    )

    # volumes chart creating
    volume_bars = go.Bar(
        x=df.Time,
        y=(df['Volume']),
        showlegend=False,
        marker={
            "color": "rgba(128,128,128,0.5)",
        }
    )

    # merging candles and volumes to one chart
    fig.add_trace(candlesticks, secondary_y=True)
    fig.add_trace(volume_bars, secondary_y=False)

    # naming chart + vectors
    fig.update_layout(title=(ticker + "/USDT Chart"), height=800)
    fig.update_yaxes(title="Price", secondary_y=True, showgrid=True)
    fig.update_yaxes(title="Volume", secondary_y=False, showgrid=False)

    # returning chart
    return fig
