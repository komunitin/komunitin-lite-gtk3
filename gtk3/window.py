import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, access, **kwargs):
        super().__init__(*args, **kwargs)
        self.access = access
        self.set_default_size(600, 400)

        # Combo to select account.
        self.accs_combo = Gtk.ComboBoxText()
        self.accs_combo.append_text("No account")
        self.accs_combo.set_active(0)
        self.accs_combo.connect("changed", self.on_account_combo_changed)

        # Network and balance labels.
        self.net_label = Gtk.Label(label="No network")
        self.balance_label = Gtk.Label(label="No balance")

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(True)
        hbox.pack_start(self.accs_combo, True, True, 0)
        hbox.pack_start(self.net_label, True, True, 0)
        hbox.pack_start(self.balance_label, True, True, 0)

        # Transactions list.
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("No transactions to show.")

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(False)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(self.textview)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(scrolledwindow, True, True, 0)

        self.add(vbox)

    def authenticate(self):
        print("No access yet")

    def fill_with_new_data(self):
        print("Get data")

    def on_account_combo_changed(self, combo):
        pass
