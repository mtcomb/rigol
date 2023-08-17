# based on
# http://stackoverflow.com/questions/4652439/is-there-a-matplotlib-equivalent-of-matlabs-datacursormode
# Left click: add an annotation
# Right click: remove the nearest annotation

class DataCursor(object):
  xoffset, yoffset = -20, 20
  text_template = 'x: %0.4f\ny: %0.4f'
  text_template = 'x: %0.4f %s\ny: %0.4f %s'

  def __init__(self, artist, tolerance=5):
    self.artist = artist
    self.ax = self.artist.axes
    self.fc=self.artist.get_markerfacecolor()
    self.annotations = []
    self.artist.set_picker(tolerance) # Tolerance in points
    self.pick  = self.ax.figure.canvas.mpl_connect('pick_event',self.on_pick)

  def on_pick(self, event):
    self.event = event

    self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
    button = event.mouseevent.button

    if self.x is not None and event.artist == self.artist:
      if button == 1:
        self.annotations.append(self.annotate(self.ax))
        event.canvas.draw()
      elif button == 3 and len(self.annotations):
        dist = [(self.x-a.xy[0])**2 for a in self.annotations]
        ind, _ = min(enumerate(dist),key=lambda x:x[1])
        self.annotations.pop(ind).remove()
        event.canvas.draw()

  def annotate(self,ax):
    annotation = self.ax.annotate(self.text_template, 
      xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset), 
      textcoords='offset points', ha='right', va='bottom',
      bbox=dict(boxstyle='round,pad=0.5', fc=self.fc, alpha=0.5),
      arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
    )

    time = self.x
    if (abs(time) < 1e-3):
        time = time * 1e6
        tUnit = "\u00B5\u0053"
    elif (abs(time) < 1):
        time = time * 1e3
        tUnit = "mS"
    else:
        tUnit = "S"

    annotation.set_text(self.text_template % (time, tUnit, self.y, 'V'))
    return annotation

  def remove(self):
    for annotation in self.annotations:
      annotation.remove()

if __name__ == '__main__':
  import matplotlib.pyplot as plt
  import numpy as np
  fig = plt.figure()
  X = np.linspace(-1,1,1000)
  Y1 = np.sin(2*np.pi*X)+0.1*np.random.rand(1000)
  Y2 = np.cos(2*np.pi*X)+0.1*np.random.rand(1000)
  line1, = plt.plot(X,Y1, 'r-')
  line2, = plt.plot(X,Y2, 'g-')
  cursor1=DataCursor(line1)
  cursor2=DataCursor(line2)
  plt.show()
