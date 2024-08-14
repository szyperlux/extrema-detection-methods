import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import extremas as ex

                    
# get data, e.g. Apple, last 2 years
df = ex.load_data("AAPL", "2y")

# calculate extremas
order = 7
dfe = ex.get_argrelmax_extremas(df, order)

# draw chart
fig = make_subplots()    
fig.add_trace(go.Scatter(x=df['Date'].values, y=df['Close'].values, name='Price', mode='lines', line_color='blue'))
fig.add_trace(go.Scatter(x=dfe['Date'], y=dfe['Extrema'], name='Extrema', mode='lines+markers', line_color='red'))
fig.update_layout(title={'text': "argrelmax, order:"+str(order),'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
fig.show() 
