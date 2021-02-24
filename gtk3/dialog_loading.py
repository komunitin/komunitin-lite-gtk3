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
        self.headers = access.headers

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.label_error = Gtk.Label(label="Loading data...")
        vbox.pack_start(self.label_error, True, True, 0)

        spinner = Gtk.Spinner()
        spinner.start()
        vbox.pack_start(spinner, True, True, 0)

        self.set_default_size(200, 200)
        box = self.get_content_area()
        box.add(vbox)
        self.show_all()

        thread = threading.Thread(target=self.get_new_data, args=(self.headers,))
        thread.daemon = True
        thread.start()

    def get_new_data(self, headers):
        try:
            members, accounts, groups = get_user_accounts(headers)
            balance, currency = get_account_balance(
                headers, groups[0]["code"], members[0]["code"])
            transfers = get_account_statement(
                headers, groups[0]["code"], accounts[0]["id"])
        except Exception as e:
            GLib.idle_add(self.error_getting_data, e)

        GLib.idle_add(self.fill_with_new_data, members, accounts, groups,
                                                balance, transfers)

    def fill_with_new_data(self, members, accounts, groups,
                           balance, transfers):
        print("Succesful getting data")
        self.destroy()

    def error_getting_data(self, e):
        self.label.set_text("Error getting data")
        print("Error getting data")
        print(str(e))
