#!/usr/bin/env python
import serial, time
import datetime
from Sent2plotly import *

ser = serial.Serial()       # create
ser.baudrate    = 9600      # baudrate
ser.port        = "/dev/ttyACM0"     # maybe change for your computer
ser.timeout     = 1         # tiemout 1 second
ser.open()                  # open serial port

plot_Vldr = Sent2plotly(0, "Plot-Vldr", "Vldr")
plot_Tem = Sent2plotly(1, "Plot-Tem", "Tem")

duration = 16.0             # in seconds
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
        print "(From Python)Vldr = " + str(Vldr) + " V, Vtem = " + str(tem) + " degree celsius"
        plot_Vldr.plot(x, Vldr)
        plot_Tem.plot(x, tem)
    time.sleep(duration - 6)# sleep
ser.close()
plot_Vldr.end()
plot_Tem.end()