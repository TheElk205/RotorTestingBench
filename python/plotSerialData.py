import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

from classes.SerialReader import SerialReader

threads = []

# Create new threads
thread1 = SerialReader(1, "Thread-1", 1)

# Start new Threads
thread1.start()

# Add threads to thread list
threads.append(thread1)

fig = plt.figure()
ax1 = fig.add_subplot(1, 3, 1)
ax2 = fig.add_subplot(1, 3, 2)
ax3 = fig.add_subplot(1, 3, 3)
xReadValues = []
yReadValues = []
yMeanValues = []

valuesRead = 0
valueSum = 0

ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.name)

def animate(i):
    values1 = np.array(thread1.values[1])
    values2 = np.array(thread1.values[2])
    values3 = np.array(thread1.values[3])
    ax1.clear()
    ax1.plot(values1[:, 0], values1[:, 1])
    ax2.clear()
    ax2.plot(values2[:, 0], values2[:, 1])
    ax3.clear()
    ax3.plot(values3[:, 0], values3[:, 1])

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()

for t in threads:
    t.exit()
    t.join()
    print("read " + str(len(t.values[0])) + " values for sensor 0")
    print("read " + str(len(t.values[1])) + " values for sensor 1")
    print("read " + str(len(t.values[2])) + " values for sensor 2")
    print("read " + str(len(t.values[3])) + " values for sensor 3")

print ("Exiting Main Thread")