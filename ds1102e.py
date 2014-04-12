#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Download data from a Rigol DS1102E oscilloscope and graph with matplotlib
         using  Alex Forencich's python-usbtmc pure python driver
 
https://github.com/alexforencich/python-usbtmc
 
mtcomb - 2014-04-12

based on
http://scruss.com/blog/2013/12/15/my-raspberry-pi-talks-to-my-oscilloscope/

scruss - 2013-12-20
  
based on
Download data from a Rigol DS1052E oscilloscope and graph with matplotlib.
By Ken Shirriff, http://righto.com/rigol
  
which in turn was
Based on http://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/
by Cibo Mahto.
"""
  
import usbtmc
import time
import numpy
  
class ds1102e(object):
  def __init__(self):
    # initialise device
    self.instr =  usbtmc.Instrument(0x1ab1, 0x0588) # Rigol DS1052E

  def read(self):
    # read data
    self.instr.write(":STOP")
    # Grab the data from channel 1
    self.instr.write(":WAV:POIN:MODE RAW")
    #instr.write(":WAV:POIN:MODE NOR")
  
    # first ten bytes are header, so skip
    rawdata1 = self.instr.ask_raw(":WAV:DATA? CHAN1")[10:]
    rawdata2 = self.instr.ask_raw(":WAV:DATA? CHAN2")[10:]
    data_size = len(rawdata1)
  
    # get metadata
    sample_rate = float(self.instr.ask_raw(':ACQ:SAMP?'))
    timescale   = float(self.instr.ask_raw(":TIM:SCAL?"))
    timeoffset  = float(self.instr.ask_raw(":TIM:OFFS?"))
    voltscale1  = float(self.instr.ask_raw(':CHAN1:SCAL?'))
    voltoffset1 = float(self.instr.ask_raw(":CHAN1:OFFS?"))
  
    voltscale2  = float(self.instr.ask_raw(':CHAN2:SCAL?'))
    voltoffset2 = float(self.instr.ask_raw(":CHAN2:OFFS?"))
  
    # show metadata
    info=[("Data size"          ,data_size),
          ("Sample rate"        ,sample_rate),
          ("Time scale"         ,timescale),
          ("Time offset"        ,timeoffset),
          ("Voltage offset ch1" ,voltoffset1),
          ("Voltage scale ch1"  ,voltscale1),
          ("Voltage offset ch2" ,voltoffset2),
          ("Voltage scale ch2"  ,voltscale2)]
  
    # convert data from (inverted) bytes to an array of scaled floats
    # this magic from Matthew Mets
    data1 = numpy.frombuffer(rawdata1, 'B')
    data1 = data1 * -1 + 255
    data1 = (data1 - 130.0 - voltoffset1/voltscale1*25) / 25 * voltscale1
  
    data2 = numpy.frombuffer(rawdata2, 'B')
    data2 = data2 * -1 + 255
    data2 = (data2 - 130.0 - voltoffset2/voltscale2*25) / 25 * voltscale2
  
    # creat array of matching timestamps
    time = numpy.linspace(timeoffset - 6 * timescale,
                          timeoffset + 6 * timescale,
                          num=len(data1))
  
    # scale time series and label accordingly
    '''
    if (time[-1] < 1e-3):
        time = time * 1e6
        tUnit = u"\u00B5\u0053"
    elif (time[-1] < 1):
        time = time * 1e3
        tUnit = "mS"
    else:
        tUnit = "S"
    '''
 
    self.instr.write(":RUN")
    self.instr.write(":KEY:FORC")
  
    return [time,data1,data2,info]

if __name__ == '__main__':

  import matplotlib.pyplot as plot

  scope=ds1102e()
  [time,tUnit,data1,data2]=scope.read()

  # Plot the data
  plot.figure(1)
  ax1 = plot.subplot(211)
  plot.plot(time, data1)
  plot.title("Channel 1")
  plot.ylabel("Voltage (V)")
  plot.xlabel("Time (" + tUnit + ")")
  plot.xlim(time[0], time[-1])
 
  plot.subplots_adjust(hspace = 0.5)
 
  plot.subplot(212, sharey=ax1)
  plot.plot(time, data2)
  plot.title("Channel 2")
  plot.ylabel("Voltage (V)")
  plot.xlabel("Time (" + tUnit + ")")
  plot.xlim(time[0], time[-1])
  #plot.ylim(ax1.get_ylim())
 
  plot.show()
