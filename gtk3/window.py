import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gtk3.dialog_login import DialogLogin
from gtk3.dialog_loading import DialogLoading


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, access, **kwargs):
        super().__init__(*args, **kwargs)
        self.access = access
        self.set_default_size(600, 400)
        self.members = []
        self.accounts = []
        self.groups = []
        self.balance = 0
        self.currency = {}
        self.transfers = []

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

    def show_dialog_login(self):
        self.dialog_login = DialogLogin(self, self.access)
        self.dialog_login.set_modal(True)
        self.dialog_login.connect("destroy",
                                  lambda x: self.show_dialog_loading())

    def show_dialog_loading(self):
        self.dialog_loading = DialogLoading(self, self.access)
        self.dialog_loading.set_modal(True)
        self.dialog_loading.set_decorated(False)
        self.dialog_loading.connect("destroy",
                                    lambda x: self.fill_with_data())

    def fill_with_data(self):
        if self.members:
            self.accs_combo.remove_all()
            for memb in self.members:
                self.accs_combo.append_text(memb["code"])
            self.accs_combo.set_active(0)
            self.net_label.set_text(self.groups[0]["code"])
            self.balance_label.set_text(
                "{} {}".format(self.balance, self.currency["symbol"]))
            self.textbuffer.set_text("Last transactions\n")
            for trans in self.transfers:
                end_buffer = self.textbuffer.get_end_iter()
                created = datetime.datetime.fromisoformat(
                    trans["attributes"]["created"])
                amount = str(trans["attributes"]["amount"]) + " " + \
                    self.currency["symbol"]
                self.textbuffer.insert(end_buffer, "{}| {}| {}\n".format(
                    created.strftime("%d/%m/%Y").ljust(12),
                    trans["attributes"]["meta"].ljust(50),
                    amount.ljust(20)
                ))

    def on_account_combo_changed(self, combo):
        pass
