#!/usr/bin/env python
import plotly
import plotly.plotly as py

print plotly.__version__

import random
import plotly.tools as tls
import datetime
import time
import numpy as np
from plotly.graph_objs import *

py.sign_in('tachagon', 'e3xdl3rnqe')
stream_ids=["5oedue6mq7", "thg9gb1wwd", "p8x1frf0qx"]
tls.set_credentials_file(stream_ids)

# Get stream id from stream id list
stream_id = stream_ids[0]
# Make instance of stream id object
stream = Stream(
    token=stream_id,    # link stream id to 'token' key
    maxpoints=80        # keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream       # embed stream id, 1 per trace
)

data = Data([trace1])

# Add title to layout object
layout = Layout(title='Time Series')

# Make a figure object
fig = Figure(data=data, layout=layout)

#(@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='s7_first-stream')

# (@)   Make instance of the Stream link object,
#       with same stream id as Stream id object
s = py.Stream(stream_id)

#(@) Open the stream
s.open()

i = 0   # a counter
k = 5   # some shape parameter
N = 200 # number of points to be plotted

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

while i<N:
    i += 1  # add to counter
    
    # Current time on x-axis, random numbers on y-axis
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    y = (np.cos(k*i/50)*np.cos(i/50.)+np.random.randn(1))[0]
    
    # Both x and y are numbers (i.e. not lists nor arrays)
    
    # write to Plotly stream!
    s.write(dict(x=x, y=y))
    
    # write number to stream to append current data on plot,
    # write lists to overwrite existing data on plot (more in 7.2)
    
    time.sleep(0.08)    # plot a point every 80 ms, for smoother plotting
    
# Close the stream when done plotting
s.close()

























