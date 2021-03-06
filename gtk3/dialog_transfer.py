import threading
import gi

gi.require_version("Gtk", "3.0")  # noqa: E402
from gi.repository import Gtk, Gdk, GLib


class DialogTransfer(Gtk.Dialog):
    def __init__(self, parent, access):
        Gtk.Dialog.__init__(self, title="{}: {}".format(_("Server"),
                            access.server["server_name"]),
                            transient_for=parent)
        self.parent = parent
        self.access = access
        self.user = access.user

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_transfer.glade")
        self.main_box = builder.get_object("MainBox")

        self.error_label = builder.get_object("ErrorLabel")
        from_account_title = builder.get_object("FromAccountTitle")
        from_account_title.set_text(_("From account") + ":")
        self.from_account_label = builder.get_object("FromAccountLabel")
        self.from_account_label.set_text(self.parent.account.acc_code)
        to_account_title = builder.get_object("ToAccountTitle")
        to_account_title.set_text(_("To account") + ":")
        amount_title = builder.get_object("AmountTitle")
        amount_title.set_text(_("Amount") + ":")

        self.to_account_input = builder.get_object("ToAccountInput")
        self.amount_input = builder.get_object("AmountInput")

        self.button_cancel = builder.get_object("CancelButton")
        self.button_cancel.connect("clicked", self.button_cancel_clicked)
        self.button_save = builder.get_object("SaveButton")
        self.button_save.connect("clicked", self.button_save_clicked)

        self.connect("key-release-event", self.on_key_release)
        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return:
            self.button_save_clicked(self.button_login)

    def button_cancel_clicked(self, button):
        self.destroy()

    def button_save_clicked(self, button):
        self.error_label.set_text("Under developing")
#        from_account = self.from_account_label
#        to_account = self.to_account_input
#        amount = self.amount_input
#        if not to_account or not amount:
#            self.error_label.set_text("Fill in account and amount")
#        else:
#            self.button_cancel.set_sensitive(False)
#            self.button_save.set_sensitive(False)
#
#            # TODO: check valid account and amount
#            thread = threading.Thread(target=self.check_transaction,
#                                      args=(from_account, to_account, amount))
#            thread.daemon = True
#            thread.start()

    def check_transaction(self, from_account, to_account, amount):
        # TODO: send check to server
        ok, error = (True, None)
        if not ok:
            GLib.idle_add(self.check_wrong, error)

        else:
            GLib.idle_add(self.check_ok)

    def check_wrong(self, error):
        # TODO: Show what's wrong
        self.error_label.set_text("Wrong data")
        print(error)
        self.button_cancel.set_sensitive(True)
        self.button_save.set_sensitive(True)

    def check_ok(self):
        # TODO: Send real transaction
        self.destroy()
