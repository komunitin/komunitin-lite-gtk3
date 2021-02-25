
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.new_user</attribute>
        <attribute name="label" translatable="yes">_New user</attribute>
      </item>
      <item>
        <attribute name="action">app.make_transfer</attribute>
        <attribute name="label" translatable="yes">_Make transfer</attribute>
      </item>
      <item>
        <attribute name="action">app.preferences</attribute>
        <attribute name="label" translatable="yes">_Preferences</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""
