import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from utils.api_services import get_account_balance, get_account_statement
from utils.api_services import get_user_accounts


class DialogLoading(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title="Loading data", transient_for=parent)
        self.parent = parent
        self.access = access
        self.headers = access.headers

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_loading.glade")
        self.main_box = builder.get_object("MainBox")
        self.label_error = builder.get_object("LabelError")
        self.label_error.set_text(_("Loading data") + "...")

        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

        thread = threading.Thread(target=self.get_new_data,
                                  args=(self.headers,))
        thread.daemon = True
        thread.start()

    def get_new_data(self, headers):
        try:
            members, accounts, groups = get_user_accounts(self.access)
            balance, currency = get_account_balance(
                self.access, groups[0]["code"], members[0]["code"])
            transfers = get_account_statement(
                self.access, groups[0]["code"], accounts[0]["id"])
        except Exception as e:
            GLib.idle_add(self.error_getting_data, e)

        GLib.idle_add(self.fill_with_new_data, members, accounts, groups,
                      balance, currency, transfers)

    def fill_with_new_data(self, members, accounts, groups,
                           balance, currency, transfers):
        self.parent.members = members
        self.parent.accounts = accounts
        self.parent.groups = groups
        self.parent.balance = balance
        self.parent.currency = currency
        self.parent.transfers = transfers
        self.destroy()

    def error_getting_data(self, e):
        self.label_error.set_text("Error getting data")
        print("Error getting data")
        print(str(e))
