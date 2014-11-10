require 'thingspeak'

client = ThingSpeak::Client.new("PT288JPS3J2PXRB5", "WNHCTH8CTTAJ16F8")

# post an update to your channel, returns the identifier of the new post if successful
while true
  data = [rand(20), rand(100)]
  client.update_channel({field1: data[0].to_s, field2: data[1].to_s}) # update data in channel
  puts "Data of Field1: " + data[0].to_s
  puts "Data of Field2: " + data[1].to_s
  sleep 15 # wait for 15 seconds.
end
