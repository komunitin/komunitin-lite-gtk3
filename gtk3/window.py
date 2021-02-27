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
        self.accs_combo.append_text("----")
        self.accs_combo.set_active(0)
        self.accs_combo.connect("changed", self.on_account_combo_changed)

        # Network and balance labels.
        self.net_label = Gtk.Label(label="----")
        self.balance_label = Gtk.Label(label="----")

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(True)
        hbox.pack_start(self.accs_combo, True, True, 0)
        hbox.pack_start(self.net_label, True, True, 0)
        hbox.pack_start(self.balance_label, True, True, 0)

        # Transactions list.
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        # self.add(self.grid)

        self.transfers_liststore = Gtk.ListStore(str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.transfers_liststore)
        for i, column_title in enumerate(
            ["Created", "Concept", "State", "Amount"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

        self.scrollable_treelist.add(self.treeview)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(self.grid, True, True, 0)

        self.add(vbox)

    def show_dialog_login(self):
        self.dialog_login = DialogLogin(self, self.access)
        self.dialog_login.set_modal(True)
        self.dialog_login.connect("destroy",
                                  lambda x: self.show_dialog_loading())

    def show_dialog_loading(self):
        if self.access.has_access:
            self.dialog_loading = DialogLoading(self, self.access)
            self.dialog_loading.set_modal(True)
            self.dialog_loading.set_decorated(False)
            self.dialog_loading.connect("destroy",
                                        lambda x: self.fill_with_data())
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="You are not authenticated. Try with new user option.",
            )
            dialog.run()
            dialog.destroy()

    def fill_with_data(self):
        if self.members:
            self.accs_combo.remove_all()
            for memb in self.members:
                self.accs_combo.append_text(memb["code"])
            self.accs_combo.set_active(0)
            self.net_label.set_text(self.groups[0]["code"])
            self.balance_label.set_text(
                "{} {}".format(self.balance, self.currency["symbol"]))
            self.transfers_liststore.clear()
            for trans in self.transfers:
                created = datetime.datetime.fromisoformat(
                    trans["attributes"]["created"])
                amount = str(trans["attributes"]["amount"]) + " " + \
                    self.currency["symbol"]
                self.transfers_liststore.append([
                    created.strftime("%d/%m/%Y"),
                    trans["attributes"]["meta"],
                    trans["attributes"]["state"],
                    str(amount)
                ])

    def on_account_combo_changed(self, combo):
        pass
