#!/usr/bin/python
import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'xflux'

FILE = '/opt/xflux/xflux'
ICON = '/opt/xflux/flux-icon-sm.png'
LONGITUDE = '37.8727'
LATITUDE = '-122.2724'

DEVNULL = open(os.devnull, 'w')


class SettingsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="F.lux Settings")

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(30)

        self.grid.attach(Gtk.Label('longitude'), 1, 1, 1, 1)
        self.entry_l = Gtk.Entry()
        self.entry_l.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.grid.attach(self.entry_l, 2, 1, 1, 1)

        self.grid.attach(Gtk.Label('latitude'), 1, 2, 1, 1)
        self.entry_g = Gtk.Entry()
        self.entry_g.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.grid.attach(self.entry_g, 2, 2, 1, 1)

        buttonbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        buttonbox.set_spacing(2)
        self.button_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        self.button_cancel.connect('clicked', self.cancel)
        buttonbox.add(self.button_cancel)

        self.button_ok = Gtk.Button(stock=Gtk.STOCK_OK)
        self.button_ok.connect('clicked', self.apply_values)
        buttonbox.add(self.button_ok)
        self.grid.attach(buttonbox, 1, 3, 2, 1)

        self.add(self.grid)

    def apply_values(self, widget):
        try:
            longitude = float(self.entry_l.get_text())
            latitude = float(self.entry_g.get_text())
            if -180 <= longitude <= 180 and -90 <= latitude <= 90:
                stop_flux()
                start_flux(str(longitude), str(latitude))
                self.destroy()
            else:
                raise ValueError('wrong range of values')
        except ValueError:
            print 'wrong values'

    def cancel(self, widget):
        self.destroy()
        

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()


def build_menu():
    item_flux = Gtk.CheckMenuItem('Enable Flux')
    item_flux.connect('activate', toggle_flux)

    item_settings = Gtk.MenuItem('Settings')
    item_settings.connect('activate', open_settings)

    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)

    menu = Gtk.Menu()
    menu.append(item_flux)
    menu.append(item_settings)
    menu.append(item_quit)
    menu.show_all()

    item_flux.set_active(True)
    return menu


def toggle_flux(item_flux):
    if item_flux.get_active():
        start_flux()
    else:
        stop_flux()


def stop_flux():
    subprocess.call(['pkill', 'xflux'], stdout=DEVNULL)


def start_flux(longitude=LONGITUDE, latitude=LATITUDE):
    print longitude + ' ' + latitude
    is_not_running = subprocess.call(['pgrep', 'xflux'], stdout=DEVNULL)
    if is_not_running:
        subprocess.call([FILE, '-l', longitude, '-g', latitude], stdout=DEVNULL)


def open_settings(widget):
    window = SettingsWindow()
    window.show_all()


def quit(widget):
    stop_flux()
    Gtk.main_quit()


if __name__ == "__main__":
    main()
