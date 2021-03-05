import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class DialogLogin(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title=_("Server") + ": " +
                            access.server["server_name"], transient_for=parent)
        self.parent = parent
        self.access = access
        self.user = access.user

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_login.glade")
        self.main_box = builder.get_object("MainBox")
        self.error_label = builder.get_object("ErrorLabel")

        label_email = builder.get_object("LabelEmail")
        label_email.set_text(_("Email") + ":")
        self.entry_email = builder.get_object("EntryEmail")
        self.entry_email.set_text(self.user)

        self.entry_pswd = builder.get_object("EntryPassword")
        label_pswd = builder.get_object("LabelPassword")
        label_pswd.set_text(_("Password") + ":")

        self.button_login = builder.get_object("ButtonLogin")
        self.button_login.connect("clicked", self.button_login_clicked)

        self.connect("key-release-event", self.on_key_release)
        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return:
            self.button_login_clicked(self.button_login)

    def button_login_clicked(self, button):
        user = self.entry_email.get_text()
        password = self.entry_pswd.get_text()
        if user and password:
            self.button_login.set_sensitive(False)
            self.error_label.set_text(_("Connecting") + "...")
            thread = threading.Thread(target=self.authenticate,
                                      args=(user, password))
            thread.daemon = True
            thread.start()

    def authenticate(self, user, password):
        ok, error = self.access.new_access(user, password)
        if not ok:
            GLib.idle_add(self.auth_wrong, error)

        else:
            GLib.idle_add(self.auth_done)

    def auth_wrong(self, error):
        if error[0:17] == "Wrong credentials":
            self.error_label.set_text(
                _("Authentication error. Please, try again."))
            self.entry_pswd.set_text("")
        if error[0:7] == "Network":
            self.error_label.set_text(
                _("Network error. Cannot connect."))
        print(error)
        self.button_login.set_sensitive(True)

    def auth_done(self):
        self.destroy()
