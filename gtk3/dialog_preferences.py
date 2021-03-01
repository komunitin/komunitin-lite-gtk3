import gettext
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from utils.local_storage import get_local_data


class DialogPreferences(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title=_("Preferences"), transient_for=parent)
        self.parent = parent
        self.set_default_size(400, 300)

        builder = Gtk.Builder()
        builder.add_from_file("gtk3/glade/dialog_preferences.glade")
        self.main_box = builder.get_object("MainBox")
        self.label_langs = builder.get_object("LabelLangs")
        self.label_langs.set_text(_("Select language") + ":")
        self.combo_langs = builder.get_object("ComboLangs")
        self.label_restart = builder.get_object("LabelRestart")
        self.label_restart.set_text(
            _("(You need to restart Komunitin Lite to see changes)"))
        self.button_save = builder.get_object("ButtonSave")
        self.button_save.connect("clicked", self.button_save_clicked)

        langs_available = gettext.find("base", localedir="po", all=True)
        print(langs_available)

        try:
            local_config = get_local_data(config=True)
        except Exception as e:
            print("Error reading configuration file.")
            print(str(e))
        print(local_config)

        for lang in langs_available:
            self.combo_langs.append_text(lang[3:5])
        self.combo_langs.set_active(0)
        self.combo_langs.connect("changed", self.on_lengs_combo_changed)

        self.connect("key-release-event", self.on_key_release)
        box = self.get_content_area()
        box.add(self.main_box)
        self.show_all()

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return:
            self.button_save_clicked(self.button_login)

    def button_save_clicked(self, button):
        pass

    def on_lengs_combo_changed(self, combo):
        pass
