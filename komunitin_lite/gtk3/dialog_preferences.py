import os
import gi

gi.require_version("Gtk", "3.0")  # noqa: E402
from gi.repository import Gtk, Gdk

from komunitin_lite.core.local_storage import get_local_data, put_local_data


class DialogPreferences(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title=_("Preferences"), transient_for=parent)
        self.parent = parent
        self.set_default_size(300, 200)

        builder = Gtk.Builder()
        builder.add_from_file(
            os.path.join(self.parent.glade_path, "dialog_preferences.glade"))
        self.main_box = builder.get_object("MainBox")
        self.label_langs = builder.get_object("LabelLangs")
        self.label_langs.set_text(_("Select language") + ":")
        self.combo_langs = builder.get_object("ComboLangs")
        self.label_restart = builder.get_object("LabelRestart")
        # self.label_restart.set_line_wrap(True)
        self.button_save = builder.get_object("ButtonSave")
        self.button_save.connect("clicked", self.button_save_clicked)

        langs_available = (self.parent.config["app_data"]["languages"]
                           .split(","))
        local_config = {}
        try:
            local_config = get_local_data(config=True)
        except Exception as e:
            print("Error reading configuration file.")
            print(str(e))

        self.current_lang = local_config["language"] if local_config else "en"
        self.combo_langs.append_text(self.current_lang)
        for lang in langs_available:
            if lang != self.current_lang:
                self.combo_langs.append_text(lang)
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
        lang = self.combo_langs.get_active_text()
        if lang != self.current_lang:
            komunitin_config = {
                "language": lang
            }
            put_local_data(komunitin_config, config=True)
        self.destroy()

    def on_lengs_combo_changed(self, combo):
        self.label_restart.set_text(
            _("(To see the changes,\nsave and restart.)"))
