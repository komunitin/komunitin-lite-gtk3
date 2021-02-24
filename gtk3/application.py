
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk

from gtk3.window import AppWindow
from gtk3.menu import MENU_XML
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

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))
        self.access = ApiAccess()

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Komunitin Lite",
                                    access=self.access)
            self.add_window(self.window)
        self.window.show_all()
        if not self.access.has_access:
            self.window.show_dialog_login()
        else:
            self.window.show_dialog_loading()

    def on_about(self, action, param):
        pass
        # about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        # about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
