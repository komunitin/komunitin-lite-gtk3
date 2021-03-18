import gi
gi.require_version('Gtk', '3.0')  # noqa: E402
from gi.repository import Gio


def build_menu():
    # root of the menu
    menu_model = Gio.Menu.new()

    # menu items
    menu_item_1 = Gio.MenuItem.new(_('New user'), 'app.new_user')
    menu_item_2 = Gio.MenuItem.new(_('New transfer'), 'app.make_transfer')
    menu_item_3 = Gio.MenuItem.new(_('Preferences'), 'app.preferences')
    menu_item_4 = Gio.MenuItem.new(_('Quit'), 'app.quit')

    # sub-menu "Menu" with menu items
    menu_actions = Gio.Menu.new()
    menu_actions.append_item(menu_item_1)
    menu_actions.append_item(menu_item_2)
    menu_actions.append_item(menu_item_3)
    menu_actions.append_item(menu_item_4)
    menu_model.append_submenu(_('Menu'), menu_actions)

    return menu_model
