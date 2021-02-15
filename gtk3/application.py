import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk

from gtk3.signal_handlers import SignalHandlers
from utils.oauth2 import ApiAccess


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.komunitin.komunitinLite",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )
        self.window = None
        self.access = None

#    def do_startup(self):
#        self.access = ApiAccess()

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file("./gtk3/glade/application_window.glade")
            self.window = builder.get_object("main_window")
            builder.connect_signals(SignalHandlers())
            self.add_window(self.window)
        self.window.show_all()
