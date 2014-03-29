#!/usr/bin/env python

# example filechooser.py

import pygtk
pygtk.require('2.0')

import gtk

def filechooser():
  dialog = gtk.FileChooserDialog("Save..",
                                 None,
                                 gtk.FILE_CHOOSER_ACTION_SAVE,
                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                  gtk.STOCK_SAVE, gtk.RESPONSE_OK))
  dialog.set_default_response(gtk.RESPONSE_OK)
  dialog.set_do_overwrite_confirmation(True)

  filter = gtk.FileFilter()
  filter.set_name("All HDF5 Files")
  filter.add_pattern("*.h5")
  filter.add_pattern("*.hdf5")
  dialog.add_filter(filter)

  filter = gtk.FileFilter()
  filter.set_name("All Files")
  filter.add_pattern("*")
  dialog.add_filter(filter)

  response = dialog.run()
  if response == gtk.RESPONSE_OK:
      filename = dialog.get_filename()
  elif response == gtk.RESPONSE_CANCEL:
      filename = None

  dialog.destroy()

  return filename

if __name__ == '__main__':
  filechooser()
