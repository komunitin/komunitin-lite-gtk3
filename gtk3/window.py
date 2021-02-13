import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gtk3.dialog_login import DialogLogin


class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = Gtk.Button(label="Open dialog")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.button.show()

    def on_button_clicked(self, widget):
        dialog = DialogLogin(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()
