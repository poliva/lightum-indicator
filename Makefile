DESTDIR?=/
SHELL = /bin/sh
INSTALL = /usr/bin/install -c
INSTALLDATA = /usr/bin/install -c -m 644

srcdir = .
prefix = $(DESTDIR)
bindir = $(prefix)/usr/bin
docdir = $(prefix)/usr/share/doc
shadir = $(prefix)/usr/share/lightum-indicator
appdir = $(prefix)/usr/share/applications

install:
	mkdir -p $(bindir)
	$(INSTALL) $(srcdir)/lightum-indicator $(bindir)/lightum-indicator
	mkdir -p $(shadir)
	$(INSTALL) $(srcdir)/cappind-lightum.py $(shadir)/cappind-lightum.py
	mkdir -p $(appdir)
	$(INSTALLDATA) $(srcdir)/lightum-indicator.desktop $(appdir)/lightum-indicator.desktop
	mkdir -p $(shadir)/icons/
	$(INSTALLDATA) $(srcdir)/icons/AB.png $(shadir)/icons/AB.png
	$(INSTALLDATA) $(srcdir)/icons/AK.png $(shadir)/icons/AK.png
	$(INSTALLDATA) $(srcdir)/icons/AS.png $(shadir)/icons/AS.png
	$(INSTALLDATA) $(srcdir)/icons/MB.png $(shadir)/icons/MB.png
	$(INSTALLDATA) $(srcdir)/icons/MK.png $(shadir)/icons/MK.png
	$(INSTALLDATA) $(srcdir)/icons/MS.png $(shadir)/icons/MS.png
	$(INSTALLDATA) $(srcdir)/icons/lightum.png $(shadir)/icons/lightum.png
	mkdir -p $(docdir)/lightum-indicator/
	$(INSTALLDATA) $(srcdir)/README.md $(docdir)/lightum-indicator/README
	$(INSTALLDATA) $(srcdir)/LICENSE $(docdir)/lightum-indicator/

uninstall:
	rm -rf $(bindir)/lightum-indicator
	rm -rf $(appdir)/lightum-indicator.desktop
	rm -rf $(docdir)/lightum-indicator/
