import threading
import os
import re
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
        builder.add_from_file(
            os.path.join(self.parent.glade_path, "dialog_transfer.glade"))
        self.main_box = builder.get_object("MainBox")

        self.error_label = builder.get_object("ErrorLabel")
        from_account_title = builder.get_object("FromAccountTitle")
        from_account_title.set_text(_("From account") + ":")
        to_account_title = builder.get_object("ToAccountTitle")
        to_account_title.set_text(_("To account") + ":")
        self.to_account_label = builder.get_object("ToAccountLabel")
        self.to_account_label.set_text(self.parent.account.account["code"])
        amount_title = builder.get_object("AmountTitle")
        amount_title.set_text(_("Amount") + ":")
        concept_title = builder.get_object("ConceptTitle")
        concept_title.set_text(_("Concept") + ":")

        self.from_account_input = builder.get_object("FromAccountInput")
        self.amount_input = builder.get_object("AmountInput")
        self.concept_text_view = builder.get_object("ConceptTextView")
        self.concept_buffer = self.concept_text_view.get_buffer()

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
            self.button_save_clicked(self.button_save)

    def button_cancel_clicked(self, button):
        self.destroy()

    def button_save_clicked(self, button):
        from_account = self.from_account_input.get_text().strip()
        amount = self.amount_input.get_text().strip().replace(',', '.')
        meta = self.concept_buffer.get_text(
            self.concept_buffer.get_start_iter(),
            self.concept_buffer.get_end_iter(), True).strip()
        error = ""
        if not re.search(r"^\w{4}\d{4}$", from_account):
            error = _("Wrong account code")
        elif not (re.search(r"^\d+(\.\d+)?$", amount) and float(amount) > 0):
            error = _("Wrong amount format")
        elif not meta:
            error = _("Empty concept")

        if error:
            self.error_label.set_text(error)
        else:
            self.error_label.set_text(_("Checking transfer data") + "...")
            self.button_cancel.set_sensitive(False)
            self.button_save.set_sensitive(False)
            new_transfer = self.parent.account.create_new_transfer(
                from_account, amount, meta)
            thread = threading.Thread(
                target=self.check_transfer, args=(new_transfer,))
            thread.daemon = True
            thread.start()

    def check_transfer(self, transfer):
        ok, error = transfer.check_data(self.parent.access,
                                        self.parent.account.group["code"])
        if not ok:
            GLib.idle_add(self.check_wrong, error)
        else:
            GLib.idle_add(self.check_ok, transfer)

    def check_wrong(self, error):
        # TODO: Show what's wrong
        self.error_label.set_text(_("Wrong data"))
        print(error)
        self.button_cancel.set_sensitive(True)
        self.button_save.set_sensitive(True)

    def check_ok(self, transfer):
        self.error_label.set_text(_("Data is ok. Sending transfer") + "...")
        thread = threading.Thread(
            target=self.send_transfer, args=(transfer,))
        thread.daemon = True
        thread.start()

    def send_transfer(self, transfer):
        ok, error = transfer.send_transfer(self.parent.access,
                                           self.parent.account.group["code"])
        if not ok:
            GLib.idle_add(self.send_wrong, error)
        else:
            GLib.idle_add(self.send_ok, transfer)

    def send_wrong(self, error):
        self.error_label.set_text(_("Something was wrong sending transfer"))
        print(error)
        self.button_cancel.set_sensitive(True)
        self.button_save.set_sensitive(True)

    def send_ok(self, transfer):
        self.error_label.set_text(_("Transfer done."))
        # self.destroy()
