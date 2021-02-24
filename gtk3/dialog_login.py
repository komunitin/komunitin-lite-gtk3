import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class DialogLogin(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title="Login", transient_for=parent)
        self.parent = parent
        self.access = access
        self.user = access.user

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        hbox_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_top.set_homogeneous(True)
        hbox_med = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_med.set_homogeneous(True)
        hbox_bot = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_bot.set_homogeneous(False)

        vbox.pack_start(hbox_top, True, True, 0)
        vbox.pack_start(hbox_med, True, True, 0)
        vbox.pack_start(hbox_bot, True, True, 0)

        label_user = Gtk.Label(label="Email:")
        hbox_top.pack_start(label_user, True, True, 0)

        self.entry_user = Gtk.Entry()
        self.entry_user.set_text(self.user)
        hbox_top.pack_start(self.entry_user, True, True, 20)

        label_pswd = Gtk.Label(label="Password:")
        hbox_med.pack_start(label_pswd, False, True, 0)
        self.entry_pswd = Gtk.Entry()
        self.entry_pswd.set_visibility(False)
        hbox_med.pack_start(self.entry_pswd, False, True, 20)

        button_login = Gtk.Button.new_with_label("Log in")
        button_login.connect("clicked", self.button_login_clicked)
        hbox_bot.pack_end(button_login, False, False, 20)

        box = self.get_content_area()
        box.add(vbox)
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
