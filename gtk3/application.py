import threading

import gi
gi.require_version('Gtk', '3.0')  # noqa: E402
from gi.repository import Gio, GLib, Gtk

from gtk3.window import AppWindow
from core.oauth2 import ApiAccess


class Application(Gtk.Application):
    def __init__(self, *args, config, **kwargs):
        super().__init__(
            *args,
            application_id="org.komunitin.komunitinLite",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )
        self.config = config
        self.window = None
        self.access = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("new_user", None)
        action.connect("activate", self.new_user)
        self.add_action(action)
        action = Gio.SimpleAction.new("make_transfer", None)
        action.connect("activate", self.make_transfer)
        self.add_action(action)
        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.preferences)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        self.access = ApiAccess(self.config)
        if not self.window:
            self.window = AppWindow(
                application=self,
                title=_("Komunitin Lite"),
                access=self.access
            )
            self.add_window(self.window)
        self.window.show_all()

        # Try to read local data & refresh token in a new thread.
        thread = threading.Thread(target=self.get_local_data)
        thread.daemon = True
        thread.start()

    def get_local_data(self):
        self.access.get_local_auth()
        GLib.idle_add(self.start_login_or_loading_dialog)

    def start_login_or_loading_dialog(self):
        if not self.access.has_access:
            self.window.show_dialog_login()
        else:
            self.window.show_dialog_loading()

    def new_user(self, action, param):
        self.window.show_dialog_login()

    def make_transfer(self, action, param):
        self.window.show_dialog_transfer()

    def preferences(self, action, param):
        self.window.show_dialog_preferences()

    def on_quit(self, action, param):
        self.quit()
