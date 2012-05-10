#!/usr/bin/python
#
# lightum-indicator applet
# (c) 2012 Pau Oliva Fora
#
# based on: 
#         cappindicator, command line generic appindicator 
#         by reda_ea <reda.ea@gmail.com>
#         license is do whatever you want with this code i don't care
#
# changes introduced in lightum-indicator licensed under GPLv2+
#

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import sys
import subprocess
import argparse
import gobject
import os

ICON_THEME = gtk.icon_theme_get_default()

class LightumIndicator:

	def __init__(self):
		# icon
		icon = "/usr/share/lightum-indicator/icons/lightum.png"
		self.icon = icon #'terminal'
		# status
		self.status = appindicator.STATUS_ATTENTION # ACTIVE
		# indicator
		self.ind = appindicator.Indicator ("lightum-indicator", self.icon, appindicator.CATEGORY_OTHER)
		#self.ind.set_attention_icon (self.icon)
		self.ind.set_status(self.status)
		# menu
		self.menu = gtk.Menu()
		self.read_config()
		

	def read_config(self):
		for i in self.menu.get_children():
			self.menu.remove(i) # check here if you want to remove this child
		self.submenus = dict()
		filename = os.getenv("HOME") + '/.config/lightum/indicator.menu'
		in_file = open(filename,"r")
		while (1):
			line = in_file.readline()
			if line == "":
				break
			line = line[0:len(line)-1] # removing last '\n'
			self.add_menu(self.menu, line, line) 
		in_file.close()
		self.add_quit()
		self.menu.show()
		self.ind.set_menu(self.menu)
	
	def add_entry(self, parent, name, path, state):
		ent = gtk.MenuItem(name)
		ent.connect("activate", self.run, path)
		ent.show()
		if state == 0:
			ent.set_sensitive(False)
		parent.append(ent)
	
	def add_sep(self, parent):
		sepr = gtk.SeparatorMenuItem()
		sepr.show()
		parent.append(sepr)
	
	def add_quit(self):
		self.add_sep(self.menu)
		ent = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		ent.connect("activate", gtk.main_quit)
		ent.show()
		self.menu.append(ent)
	
	def run(self, w, name):
		cmd = "/usr/share/lightum-indicator/lightum-indicator-helper " + name
		p = subprocess.Popen(cmd, shell=True)
		p.wait()
		self.read_config()
	
	def get_child(self, parent, name):
		if parent not in self.submenus:
			self.submenus[parent] = dict()
		children = self.submenus[parent]
		if name not in children :
			child = gtk.Menu()
			child.show()
			item = gtk.MenuItem(name)
			item.set_submenu(child)
			item.show()
			parent.append(item)
			children[name] = child
		return children[name]
	
	def add_menu(self, parent, line, path):
		s = line.split(':', 1)
		if len(s) > 1:
			child = self.get_child(parent, s[0])
			self.add_menu(child, s[1], path)
		else:
			if len(s[0]) == 0:
				self.add_sep(parent)
			else:
				if line[0] == '*':
					state=0
					line = line[1:len(line)]
				else:
					state=1
				self.add_entry(parent, line, path, state)



if __name__ == "__main__":
	indicator = LightumIndicator()
	gtk.main()
