import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class DialogLogin(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title="demo.integralces.net",
                            transient_for=parent)
        self.parent = parent
        self.access = access
        self.user = access.user

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_login.glade")
        self.main_box = builder.get_object("MainBox")
        self.entry_user = builder.get_object("EntryUser")
        self.entry_user.set_text(self.user)
        self.entry_pswd = builder.get_object("EntryPassword")
        button_login = builder.get_object("ButtonLogin")
        button_login.connect("clicked", self.button_login_clicked)

        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

    def button_login_clicked(self, button):
        user = self.entry_user.get_text()
        password = self.entry_pswd.get_text()
        thread = threading.Thread(target=self.authenticate,
                                  args=(user, password))
        thread.daemon = True
        thread.start()

    def authenticate(self, user, password):
        ok, error = self.access.new_access(user, password)
        if not ok:
            if error == "Wrong credentials":
                print(error)
            if error[0:7] == "Network":
                print(error)
            GLib.idle_add(self.auth_wrong)

        else:
            GLib.idle_add(self.auth_done)

    def auth_wrong(self):
        print("Error on authentication")

    def auth_done(self):
        print("Succesful authentication")
        self.destroy()
