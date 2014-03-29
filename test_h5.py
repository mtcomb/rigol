import matplotlib.pyplot as plot
import h5py

f = h5py.File('test.h5','r')
time = f['time']
data1 = f['data1']
data2 = f['data2']

plot.plot(time,data1)
plot.plot(time,data2)
plot.ylabel("Voltage (V)")
plot.xlabel("Time (S)")
plot.xlim(time[0], time[-1])
plot.show()
