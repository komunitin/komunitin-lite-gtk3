import gi
gi.require_version('Gtk', '3.0')  # noqa: E402 # noqa: E402
from gi.repository import Gtk

from gtk3.dialog_login import DialogLogin
from gtk3.dialog_loading import DialogLoading
from gtk3.dialog_preferences import DialogPreferences
from gtk3.dialog_transfer import DialogTransfer


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, access, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)
        self.access = access
        self.accounts = []
        self.account = None
        self.transfers = []

        # Combo to select account.
        self.accs_combo = Gtk.ComboBoxText()
        self.accs_combo.append_text("----")
        self.accs_combo.set_active(0)
        self.accs_combo.connect("changed", self.on_account_combo_changed)

        # Network and balance labels.
        self.user_label = Gtk.Label(label="----")
        self.net_label = Gtk.Label(label="----")
        self.balance_label = Gtk.Label(label="----")

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(True)
        hbox.pack_start(self.user_label, True, True, 0)
        hbox.pack_start(self.accs_combo, True, True, 0)
        hbox.pack_start(self.net_label, True, True, 0)
        hbox.pack_start(self.balance_label, True, True, 0)

        # Transactions list.
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        # self.add(self.grid)

        self.transfers_liststore = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.transfers_liststore)
        for i, column_title in enumerate(
            [_("Created"), _("Concept"), _("From account"), _("To account"),
             _("State"), _("Amount")]
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

    def show_dialog_loading(self, account=None):
        if self.access.has_access:
            self.dialog_loading = DialogLoading(self, self.access, account)
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
                text=_("You are not authenticated. Try with new user option.")
            )
            dialog.run()
            dialog.destroy()

    def fill_with_data(self):
        if self.account:
            name = self.account.member["name"]
            name = (name[:10] + '..') if len(name) > 10 else name
            self.user_label.set_text(_("Name") + ": {}".format(name))
            self.accs_combo.remove_all()
            active_index = 0
            for index, acc in enumerate(self.accounts):
                self.accs_combo.append_text(acc.account["code"])
                if acc == self.account:
                    active_index = index
            self.accs_combo.set_active(active_index)
            self.net_label.set_text(
                _("Group") + ": {}".format(self.account.group["code"]))
            show_balance = int(self.account.balance) * 10 ** (
                -int(self.account.currency["decimals"]))
            self.balance_label.set_text(
                _("Balance") + ": {} {}".format(
                    show_balance, self.account.currency["symbol"]))
            self.transfers_liststore.clear()
            for trans in self.transfers:
                sign_amount = "" if (trans.payee_account["code"] ==
                                     self.account.account["code"]) else "-"
                self.transfers_liststore.append([
                    trans.created.strftime("%d/%m/%Y"),
                    trans.meta,
                    trans.payer_account["code"],
                    trans.payee_account["code"],
                    trans.state,
                    "{}{} {}".format(
                        sign_amount,
                        trans.amount * 10 ** -(
                            int(trans.currency["decimals"])),
                        trans.currency["symbol"]
                    )
                ])

    def show_dialog_preferences(self):
        dialog = DialogPreferences(parent=self)
        dialog.run()
        dialog.destroy()

    def show_dialog_transfer(self):
        self.dialog_login = DialogTransfer(self, self.access)
        self.dialog_login.set_modal(True)

    def on_account_combo_changed(self, combo):
        account = None
        account_code = combo.get_active_text()
        for acc in self.accounts:
            if acc.account["code"] == account_code:
                account = acc
        if account and account != self.account:
            self.account = account
            self.show_dialog_loading(account)
