#!/usr/bin/python3

import threading
import time

from classes.SerialReader import SerialReader

threads = []

# Create new threads
thread1 = SerialReader(1, "Thread-1", 1)

# Start new Threads
thread1.start()

# Add threads to thread list
threads.append(thread1)

time.sleep(1)

# Wait for all threads to complete
for t in threads:
    t.exit()
    t.join()
    print("read " + str(len(t.values[0])) + " values for sensor 0")
    print("read " + str(len(t.values[1])) + " values for sensor 1")
    print("read " + str(len(t.values[2])) + " values for sensor 2")
    print("read " + str(len(t.values[3])) + " values for sensor 3")

print ("Exiting Main Thread")