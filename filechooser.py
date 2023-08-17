#!/usr/bin/env python

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
import os


def filechooser():
  dialog = Gtk.FileDialog.new()
  dialog.set_title("Save...")
  dialog.set_initial_folder(Gio.File.new_for_path(os.getcwd()))

  filt = Gtk.FileFilter()
  filters = Gio.ListStore.new(Gtk.FileFilter)
  filt.set_name("All HDF5 Files")
  filt.add_pattern("*.h5")
  filt.add_pattern("*.hdf5")
  filters.append(filt)

  filt = Gtk.FileFilter()
  filt.set_name("All Files")
  filt.add_pattern("*")
  filters.append(filt)
  dialog.set_filters(filters)

  return dialog

if __name__ == '__main__':
  filechooser()
