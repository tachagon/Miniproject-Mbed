#!/usr/bin/env python
import serial, time, httplib, urllib
import datetime
from Sent2plotly import *
import webbrowser

ser = serial.Serial()       # create
ser.baudrate    = 9600      # baudrate
ser.port        = "/dev/ttyACM0"     # maybe change for your computer
ser.timeout     = 1         # tiemout 1 second
ser.open()                  # open serial port

plot_Vldr = Sent2plotly(0, "Plot-Vldr", "Voltage of LDR")
plot_Tem = Sent2plotly(1, "Plot-Tem", "Temperature")

webbrowser.open_new_tab("index.html")

duration = 16.0             # in seconds
def sent2Thingspeak(Vldr, Tem):
    Vldr = "%0.2f" % Vldr
    Tem = "%0.2f" % Tem
    conn = httplib.HTTPConnection("api.thingspeak.com:80") # connect to ThingSpeak
    time.sleep(1)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"} # header for HTTP request
    params = urllib.urlencode({'field1': Vldr, 'field2': Tem, 'key': 'PT288JPS3J2PXRB5'})
    conn.request("POST", "/update", params, headers)
    time.sleep(1)
    response = conn.getresponse()
    conn.close()
    return response.status, response.reason

while True:                 # endless loop
    time.sleep(1)           # wait for arduino to read data from sensor
    read = ser.readline()   # read one byte
    read = read.split(",")  # read = ['Vldr', 'Vtem', '\n']
    if len(read) >= 3:      # check read complete
        Vldr = int(read[0]) # converse Vldr from string to integer
        Vtem = int(read[1]) # converse Vtem from string to integer
        Vldr = Vldr * (5.0 / 1023.0)        # calculate voltage of LDR
        tem = Vtem * (5.0 / 1023.0) / 3.0 * 100  # calculate voltage of LM35DZ(with gain of Differential Amplifier)
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        status = sent2Thingspeak(Vldr, tem)
        print "status", status, "Vldr = " + str(Vldr) + " V, Vtem = " + str(tem) + " degree celsius"
        plot_Vldr.plot(x, Vldr)
        plot_Tem.plot(x, tem)
    time.sleep(duration - 3)# sleep
ser.close()
plot_Vldr.end()
plot_Tem.end()