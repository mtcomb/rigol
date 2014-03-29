from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

import gtk

import numpy as np
import h5py

from filechooser import filechooser
from ds1102e import ds1102e

class scope(object):
  def __init__(self):

    self.scope = ds1102e()
    self.data = {}
    self.info = []

    win = gtk.Window()
    win.connect("destroy", lambda x: gtk.main_quit())
    win.set_default_size(800,600)
    win.set_title("Rigol DS1102E")

    vbox = gtk.VBox()
    win.add(vbox)

    self.fig = Figure(figsize=(5,4))
    self.ax = self.fig.add_subplot(111)
    self.ax.set_ylabel("Voltage (V)")
    self.ax.set_xlabel("Time (S)")

    self.canvas = FigureCanvas(self.fig)  # a gtk.DrawingArea
    vbox.pack_start(self.canvas)

    hbox = gtk.HBox()
    button = gtk.Button('Capture')
    button.connect("pressed", self.capture)
    hbox.pack_start(button, True, True)
    button = gtk.Button('Save')
    button.connect("pressed", self.save)
    hbox.pack_start(button, True, True)
    vbox.pack_start(hbox, False, False)

    self.toolbar = NavigationToolbar(self.canvas, win)
    vbox.pack_start(self.toolbar, False, False)

    win.show_all()
    gtk.main()

  def capture(self,event):
    [time,data1,data2,info]=self.scope.read()
    self.data['time']  = time
    self.data['data1'] = data1
    self.data['data2'] = data2
    self.info  = info

    for item in self.info:
      print item[0]+":\t", item[1]

    # Plot the data
    self.ax.lines=[]
    self.ax.plot(time,data1,'b-')
    self.ax.plot(time,data2,'g-')
    self.ax.set_xlim(time[0], time[-1])
    self.canvas.draw()

  def save(self,event):
    filename = filechooser()
    if filename:
      f=h5py.File(filename,'w')
      for item in self.data.iteritems():
        f[item[0]]=item[1]
      for item in self.info:
        f[item[0]]=item[1]
      f.close()

if __name__ == '__main__':
  s=scope()
