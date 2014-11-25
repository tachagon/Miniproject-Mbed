#!/usr/bin/env ruby

# using the SerialPort gem
# (http://rubygems.org/gems/serialport)
require "serialport"
require "rubygems"
require 'thingspeak'

client = ThingSpeak::Client.new("PT288JPS3J2PXRB5", "WNHCTH8CTTAJ16F8")

# params for serial port
port_str = "/dev/ttyACM0"   # maybe change for your computer
baud_rate = 9600            # baudrate
data_bits = 8
stop_bits = 1
parity = SerialPort::NONE

sp = SerialPort.new(port_str, baud_rate, data_bits, stop_bits, parity)

duration = 16.0                 # in seconds
# just read forever
sleep 1
while true do
  sleep duration - 1            # wait for arduino to read data from sensor
  read = sp.read                # read data from serial port
  sleep 1
  read = read.split("\n")       # because ruby store a lot of data (during sleep)
  read = read[read.length-1]    # use the last of data
  read = read.split(",")        # divide data are Vldr and Vtem
  if (read.length == 2)         # because the first packet has wrong data
    input = Array.new
    read.each {|e| input.push(e.to_f)}  # convert each data from string to float
    client.update_channel({field1: (input[0] * (5.0 / 1023.0)).to_s, field2: (input[1] * (5.0 / 1023.0) / 3 * 100).to_s}) # update data in channel
    printf("(From Ruby)Vldr = %f V, Tem = %f degree celsius\n", (input[0] * (5.0 / 1023.0)), (input[1] * (5.0 / 1023.0) / 3 * 100))
  end
end

begin
  while true do
    sp.print STDIN.gets.chomp
  end
rescue Interrupt
  sp.close
  puts                          # insert a newline character after ^C
end
