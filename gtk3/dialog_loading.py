import threading
import gi

gi.require_version("Gtk", "3.0")  # noqa: E402
from gi.repository import Gtk, GLib

from utils.account import get_accounts


class DialogLoading(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title="Loading data", transient_for=parent)
        self.parent = parent
        self.access = access

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_loading.glade")
        self.main_box = builder.get_object("MainBox")
        self.label_error = builder.get_object("LabelError")
        self.label_error.set_text(_("Loading data") + "...")

        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

        thread = threading.Thread(target=self.get_new_data,
                                  args=(self.access,))
        thread.daemon = True
        thread.start()

    def get_new_data(self, access):
        try:
            accounts = get_accounts(access)
            accounts[0].get_balance(access)
            transfers = accounts[0].get_transfers(access)
        except Exception as e:
            GLib.idle_add(self.error_getting_data, e)

        GLib.idle_add(self.fill_with_new_data, accounts, transfers)

    def fill_with_new_data(self, accounts, transfers):
        self.parent.accounts = accounts
        self.parent.account = accounts[0]
        self.parent.transfers = transfers
        self.destroy()

    def error_getting_data(self, e):
        self.label_error.set_text("Error getting data")
        print("Error getting data")
        print(str(e))
