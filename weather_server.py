#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from random import randrange
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

i = 0
# while i<10:
while True:
    i = i + 1
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)
    order = i

    sent_string = "{} {} {} {}".format(zipcode, order, temperature, relhumidity)
    # this is not good practice to set a sleep here, but this is just to illustrate the behavior depicted in the zmq manual book.
    # if no wait is set, even if we start the client before, we'll loose thousands of published messages
    if ( i == 1 ):
        time.sleep(0.3)
    socket.send_string(sent_string)
    print(sent_string)
