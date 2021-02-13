import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DialogLogin(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Login", transient_for=parent, flags=0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        hbox_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_top.set_homogeneous(False)
        hbox_med = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_med.set_homogeneous(False)
        hbox_bot = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_bot.set_homogeneous(False)

        vbox.pack_start(hbox_top, True, True, 0)
        vbox.pack_start(hbox_med, True, True, 0)
        vbox.pack_start(hbox_bot, True, True, 0)

        label_user = Gtk.Label(label="User:")
        hbox_top.pack_start(label_user, True, True, 0)

        self.entry_user = Gtk.Entry()
        hbox_top.pack_start(self.entry_user, True, True, 0)

        label_pswd = Gtk.Label(label="Password:")
        hbox_med.pack_start(label_pswd, True, True, 0)
        self.entry_pswd = Gtk.Entry()
        self.entry_pswd.set_visibility(False)
        hbox_med.pack_start(self.entry_pswd, True, True, 0)

        button_login = Gtk.Button.new_with_label("Log in")
        button_login.connect("clicked", self.button_login_clicked)
        hbox_bot.pack_start(button_login, True, True, 0)

        self.set_default_size(300, 100)

        box = self.get_content_area()
        box.add(vbox)
        self.show_all()

    def button_login_clicked(self, button):
        pass
