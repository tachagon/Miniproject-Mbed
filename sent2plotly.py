#!/usr/bin/env python
import plotly
import plotly.plotly as py
import plotly.tools as tls
import datetime
import time
from plotly.graph_objs import *

class Sent2plotly(object):
    def __init__(self,choose_stream_id, filename, title):
        self.filename = filename
        self.title = title
        self.dataX = 0.0
        self.dataY = 0.0
        
        py.sign_in('tachagon', 'e3xdl3rnqe')
        stream_ids=["5oedue6mq7", "thg9gb1wwd", "p8x1frf0qx"]
        tls.set_credentials_file(stream_ids)
        
        # Get stream id from stream id list
        stream_id = stream_ids[choose_stream_id]
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
        layout = Layout(title=self.title)
        
        # Make a figure object
        fig = Figure(data=data, layout=layout)
        
        #(@) Send fig to Plotly, initialize streaming plot, open new tab
        unique_url = py.plot(fig, filename=self.filename)
        
        # (@)   Make instance of the Stream link object,
        #       with same stream id as Stream id object
        self.s = py.Stream(stream_id)
        
        #(@) Open the stream
        self.s.open()
    
    def plot(self, dataX, dataY):
        self.dataX = dataX
        self.dataY = dataY
        self.s.write(dict(x=self.dataX, y=self.dataY))
    
    def end(self):
        self.s.close()
    
if __name__ == '__main__':
    test = Sent2plotly(0,"filename", "title")
    test2 = Sent2plotly(1,"filename2", "title")
    time.sleep(5)
    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = 1
        test.plot(x, y)
        time.sleep(1)
        y = 2
        test2.plot(x, y)
        time.sleep(1)
    test.end()
    test2.end()
