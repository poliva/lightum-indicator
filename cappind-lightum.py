#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import sys
import subprocess
import argparse
import gobject

ICON_THEME = gtk.icon_theme_get_default()

# cappindicator, command line generic appindicator 
# by reda_ea <reda.ea@gmail.com>
# license is do whatever you want with this code i don't care

# accepts input in forms of multiple lines
# of the form menu:submenu:...:entry:command
# empty command means separator
# implied parent menus are automatically created
# entries in the same path appear in the same order as in the input
# undefined behaviour on wrong input

# modified by pof for lightum-indicator:
# if a submenu item begins with '*' it will be shown as disabled

class CmdAppIndicator:

	def __init__(self, persist, icon, label):
		# parameters
		self.persist = persist #True
		self.icon = icon #'terminal'
		self.status = appindicator.STATUS_ATTENTION # ACTIVE
		self.label = label
		# indicator
		self.ind = appindicator.Indicator ("c-indicator", self.icon, appindicator.CATEGORY_OTHER)
		self.ind.set_label(self.label)
		#self.ind.set_attention_icon (self.icon)
		self.ind.set_status(self.status)
		# menu
		self.menu = gtk.Menu()
		self.submenus = dict()
		for line in sys.stdin:
			line = line[0:len(line)-1] # removing last '\n'
			self.add_menu(self.menu, line, line) 
		if self.persist:
			self.add_quit()
		self.menu.show()
		self.ind.set_menu(self.menu)
	
	def add_entry(self, parent, name, path, state):
		ent = gtk.MenuItem(name)
		ent.connect("activate", self.say, path)
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
	
	def run(self, w, cmd):
		subprocess.Popen(cmd, shell=True)
		if not self.persist:
			gtk.main_quit()
	
	def say(self, w, name):
		print name
		sys.stdout.flush()
		if not self.persist:
			gtk.main_quit()
	
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
	# command line params
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description='Command line generic appindicator.\n\n'
	'Menu elements are given in standard input as lines in the form:\n\n'
	'\tmenu:submenu:subsubmenu:entry\n\n'
	'Menu structure is automatically built, selecting a leaf '
	'will print the associated input line (the whole path).')
	parser.add_argument('-i', '--icon', default='terminal', help='the indicator icon name')
	parser.add_argument('-l', '--label', default='', help='optional label (not recommended)')
	parser.add_argument('-p', '--persist', action='store_true', default=False,
		help='keep the indicator running after a selection (an additional "Quit" entry will be added)')
	parser.add_argument('-t', '--timeout', type=int, default=-1,
		help='a timeout in seconds after which the indicator will be closed')
	args =  parser.parse_args()
	if args.timeout >= 0:
		gobject.timeout_add(args.timeout*1000, gtk.main_quit)
	indicator = CmdAppIndicator(args.persist, args.icon, args.label)
	gtk.main()

