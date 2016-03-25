#!/usr/bin/python
import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


def main():
    Fluxgui('37.8727','-122.2724')


class Fluxgui(object):

    def __init__(self, longitude, latitude):
        self.id = 'xflux'
        self.xflux = '/opt/xflux/xflux'
        self.icon_active = '/opt/xflux/fluxgui-active.png'
        self.icon_inactive = '/opt/xflux/fluxgui-inactive.png'
        self.longitude = longitude
        self.latitude = latitude

        self.devnull = open(os.devnull, 'w')

        self.item_flux = Gtk.CheckMenuItem('Enable Flux')
        self.item_flux.connect('activate', self.toggle_flux)

        self.item_quit = Gtk.MenuItem('Quit')
        self.item_quit.connect('activate', quit)

        self.menu = Gtk.Menu()
        self.menu.append(self.item_flux)
        self.menu.append(self.item_quit)
        self.menu.show_all()

        self.item_flux.set_active(True)

        self.indicator = appindicator.Indicator.new(self.id, self.icon_active, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

        Gtk.main()

    def toggle_flux(self, widget):
        if self.item_flux.get_active():
            self.start_flux()
        else:
            self.stop_flux()

    def stop_flux(self):
        subprocess.call(['pkill', 'xflux'], stdout=self.devnull)
        self.indicator.set_icon(self.icon_inactive)

    def start_flux(self):
        is_not_running = subprocess.call(['pgrep', 'xflux'], stdout=self.devnull)
        if is_not_running:
            subprocess.call([self.xflux, '-l', self.longitude, '-g', self.latitude], stdout=self.devnull)
            self.indicator.set_icon(self.icon_active)


    def quit(self):
        self.stop_flux()
        Gtk.main_quit()


if __name__ == "__main__":
    main()
