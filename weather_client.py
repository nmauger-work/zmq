#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server…")
socket.connect("tcp://localhost:5556")

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else False
 
# Python 2 - ascii bytes to unicode str
if zip_filter != False:
    if isinstance(zip_filter, bytes):
        zip_filter = zip_filter.decode('ascii')
    socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
else:
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

# Process 50 updates
total_temp = 0
for update_nbr in range(50):
    string = socket.recv_string()
    order, zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)
    print("{} Current temp for zipcode {} is {}".format(order, zip_filter, temperature))
    sys.stdout.flush()

print("Average temperature for zipcode '%s' was %dF" % (
      zip_filter, total_temp / (update_nbr+1))
)
