import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk

from gtk3.window import Window


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.komunitin.komunitinLite",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )

    def do_activate(self):
        self.window = Window(application=self, title="Main Window")
        self.window.present()
