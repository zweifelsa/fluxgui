#!/usr/bin/python
import os, subprocess
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'xflux'

FILE = '/opt/xflux/xflux'
ICON = '/opt/xflux/flux-icon-sm.png'
LONGITUDE = '37.8727'
GRATITUDE = '-122.2724'

DEVNULL = open(os.devnull, 'w')



def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    
    item_flux = gtk.CheckMenuItem('Enable Flux')
    item_flux.connect('activate', toggle_flux)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)

    menu.append(item_flux)
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


def start_flux():
    is_not_running = subprocess.call(['pgrep', 'xflux'], stdout=DEVNULL)
    if is_not_running:
        subprocess.call([FILE, '-l', LONGITUDE, '-g', GRATITUDE], stdout=DEVNULL)

 
def quit(source):
    stop_flux()
    gtk.main_quit()


if __name__ == "__main__":
    main()