import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import extremas as ex
import numpy as np

# get data, e.g. Apple, last 2 years
df = ex.load_data ("AAPL", "2y")

# calculate extrema
vector_start = 3
vector_end = 6
widths = np.arange (vector_start, vector_end)
dfe = ex.get_find_peaks_cwt_extremas (df, widths = widths)

# draw chart
fig = make_subplots()    
fig.update_xaxes(rangebreaks=[dict(values=ex.get_break_days(df))]) # exclude break days (weekends, holidays)
fig.add_trace(go.Scatter(x=df['Date'].values, y=df['Close'].values, name='Price', mode='lines', line_color='blue'))
fig.add_trace(go.Scatter(x=dfe['Date'], y=dfe['Extrema'], name='Extrema', mode='lines+markers', line_color='red'))
fig.update_layout(title={'text': "find_peaks_cwt "+str(widths),'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
fig.show() 