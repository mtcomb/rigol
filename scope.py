import matplotlib
matplotlib.use('GTK4Agg')
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas

from matplotlib.figure import Figure

import numpy as np
import h5py

from filechooser import filechooser
from ds1102e import ds1102e
from cursor import DataCursor

class scope(object):
  def __init__(self):
    self.scope = ds1102e()
    self.data = {}
    self.info = []
    self.cursors = []

  def on_activate(self, app):
    self.win = Gtk.ApplicationWindow(application=app)
    self.win.connect("destroy", lambda x: Gtk.main_quit())
    self.win.set_default_size(800,600)
    self.win.set_title("Rigol DS1102E")

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.win.set_child(vbox)

    self.fig = Figure(figsize=(5,4))
    self.ax = self.fig.add_subplot(111)
    self.ax.set_ylabel("Voltage (V)")
    self.ax.set_xlabel("Time (S)")

    self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
    vbox.prepend(self.canvas)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    button = Gtk.Button(label="Capture")
    button.connect("clicked", self.capture)
    hbox.prepend(button) #, True, True)
    button = Gtk.Button(label="Save")
    button.connect("clicked", self.save)
    hbox.prepend(button)
    vbox.prepend(hbox)

    self.toolbar = NavigationToolbar(self.canvas, self.win)
    vbox.prepend(self.toolbar)

    self.dialog = filechooser()

    self.win.present()

  def capture(self,event):
    [time,data1,data2,info]=self.scope.read()
    self.data['time']  = time
    self.data['data1'] = data1
    self.data['data2'] = data2
    self.info  = info

    for item in self.info:
      print(item[0]+":\t", item[1])

    # Plot the data
    lines = []
    lines.extend(self.ax.plot(time,data1,'b-'))
    lines.extend(self.ax.plot(time,data2,'g-'))
    self.ax.set_xlim(time[0], time[-1])
    for cursor in self.cursors:
      cursor.remove()
    self.cursors = []
    for line in lines:
      self.cursors.append(DataCursor(line))
    self.ax.grid(True)
    self.canvas.draw()

  def save(self, event):
    def save_cb(dlg, result):
      sfile = dlg.save_finish(result)
      f=h5py.File(sfile.get_path(),'w')
      for item in self.data.items():
        f[item[0]]=item[1]
      for item in self.info:
        f[item[0]]=item[1]
      f.close()

    self.dialog.save(self.win, None, save_cb)


if __name__ == '__main__':
  app = Gtk.Application()
  s=scope()
  app.connect("activate", s.on_activate)
  app.run()
