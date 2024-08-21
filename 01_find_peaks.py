import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import extremas as ex


# get data, e.g. Apple, last 2 years
df = ex.load_data("AAPL", "2y")

# calculate extrema
prominence = 5
dfe = ex.get_find_peaks_extremas(df, prominence)

# draw chart
fig = make_subplots()   
fig.update_xaxes(rangebreaks=[dict(values=ex.get_break_days(df))]) # exclude break days (weekends, holidays) 
fig.add_trace(go.Scatter(x=df['Date'].values, y=df['Close'].values, name='Price', mode='lines', line_color='blue'))
fig.add_trace(go.Scatter(x=dfe['Date'], y=dfe['Extrema'], name='Extrema', mode='lines+markers', line_color='red'))
fig.update_layout(title={'text': "find_peaks, prominence:"+str(prominence),'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
fig.show() 