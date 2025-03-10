
# =====================================================
#                  Author Brad Heffernan
# =====================================================

import os
import shutil
from pathlib import Path
import configparser

home = os.path.expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = ''.join([str(Path(__file__).parents[2]), "/share/arcologout/"])

if os.path.isfile(home + "/.config/arcologout/arcologout.conf"):
    config = home + "/.config/arcologout/arcologout.conf"
else:
    config = ''.join([str(Path(__file__).parents[3]), "/etc/arcologout.conf"])
root_config = ''.join([str(Path(__file__).parents[3]), "/etc/arcologout.conf"])


def _get_position(lists, value):
    data = [string for string in lists if value in string]
    position = lists.index(data[0])
    return position


def _get_themes():
    y = [x for x in os.listdir(working_dir + "themes")]
    y.sort()
    return y


def get_config(self, Gdk, Gtk, config):
    try:
        self.parser = configparser.RawConfigParser()
        self.parser.read(config)

        # Set some safe defaults
        self.opacity = 60

        # Check if we're using HAL, and init it as required.
        if self.parser.has_section("settings"):
            if self.parser.has_option("settings", "opacity"):
                self.opacity = int(self.parser.get("settings", "opacity"))/100
            if self.parser.has_option("settings", "buttons"):
                self.buttons = self.parser.get("settings", "buttons").split(",")
            if self.parser.has_option("settings", "icon_size"):
                self.icon = int(self.parser.get("settings", "icon_size"))
            if self.parser.has_option("settings", "font_size"):
                self.font = int(self.parser.get("settings", "font_size"))

        # if self.parser.has_section("commands"):
        #    if self.parser.has_option("commands", "lock"):
        #        self.cmd_lock = str(self.parser.get("commands", "lock"))

        if self.parser.has_section("binds"):
            if self.parser.has_option("binds", "lock"):
                self.binds['lock'] = self.parser.get("binds", "lock").capitalize()
            if self.parser.has_option("binds", "restart"):
                self.binds['restart'] = self.parser.get("binds", "restart").capitalize()
            if self.parser.has_option("binds", "shutdown"):
                self.binds['shutdown'] = self.parser.get("binds", "shutdown").capitalize()
            if self.parser.has_option("binds", "suspend"):
                self.binds['suspend'] = self.parser.get("binds", "suspend").capitalize()
            if self.parser.has_option("binds", "hibernate"):
                self.binds['hibernate'] = self.parser.get("binds", "hibernate").capitalize()
            if self.parser.has_option("binds", "logout"):
                self.binds['logout'] = self.parser.get("binds", "logout").capitalize()
            if self.parser.has_option("binds", "cancel"):
                self.binds['cancel'] = self.parser.get("binds", "cancel").capitalize()
            if self.parser.has_option("binds", "settings"):
                self.binds['settings'] = self.parser.get("binds", "settings").capitalize()

        if self.parser.has_section("themes"):
            if self.parser.has_option("themes", "theme"):
                self.theme = self.parser.get("themes", "theme")

        if len(self.theme) > 1:
            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(working_dir + 'themes/' + self.theme + '/theme.css')

            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
    except Exception as e:
        print(e)
        os.unlink(home + "/.config/arcologout/arcologout.conf")
        if not os.path.isfile(home + "/.config/arcologout/arcologout.conf"):
            shutil.copy(root_config, home + "/.config/arcologout/arcologout.conf")


def button_active(self, data, GdkPixbuf):
    try:
        if data == self.binds['shutdown']:
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/shutdown_blur.svg'), self.icon, self.icon)
            self.imagesh.set_from_pixbuf(psh)
            self.lbl1.set_markup("<span foreground=\"white\">Shutdown</span>")
        elif data == self.binds['restart']:
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/restart_blur.svg'), self.icon, self.icon)
            self.imager.set_from_pixbuf(pr)
            self.lbl2.set_markup("<span foreground=\"white\">Restart</span>")
        elif data == self.binds['suspend']:
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/suspend_blur.svg'), self.icon, self.icon)
            self.images.set_from_pixbuf(ps)
            self.lbl3.set_markup("<span foreground=\"white\">Suspend</span>")
        elif data == self.binds['lock']:
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/lock_blur.svg'), self.icon, self.icon)
            self.imagelk.set_from_pixbuf(plk)
            self.lbl4.set_markup("<span foreground=\"white\">Lock</span>")
        elif data == self.binds['logout']:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/logout_blur.svg'), self.icon, self.icon)
            self.imagelo.set_from_pixbuf(plo)
            self.lbl5.set_markup("<span foreground=\"white\">Logout</span>")
        elif data == self.binds['cancel']:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/cancel_blur.svg'), self.icon, self.icon)
            self.imagec.set_from_pixbuf(plo)
            self.lbl6.set_markup("<span foreground=\"white\">Cancel</span>")
        elif data == self.binds['hibernate']:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/hibernate_blur.svg'), self.icon, self.icon)
            self.imageh.set_from_pixbuf(plo)
            self.lbl7.set_markup("<span foreground=\"white\">Hibernate</span>")
    except:
        pass

def button_toggled(self, data):
    self.Esh.set_sensitive(False)
    self.Er.set_sensitive(False)
    self.Es.set_sensitive(False)
    self.Elk.set_sensitive(False)
    self.El.set_sensitive(False)
    self.Ec.set_sensitive(False)
    self.Eh.set_sensitive(False)

    if data == self.binds['shutdown']:
        self.Esh.set_sensitive(True)
    elif data == self.binds['restart']:
        self.Er.set_sensitive(True)
    elif data == self.binds['suspend']:
        self.Es.set_sensitive(True)
    elif data == self.binds['lock']:
        self.Elk.set_sensitive(True)
    elif data == self.binds['logout']:
        self.El.set_sensitive(True)
    elif data == self.binds['cancel']:
        self.Ec.set_sensitive(True)
    elif data == self.binds['hibernate']:
        self.Eh.set_sensitive(True)


def file_check(file):
    if os.path.isfile(file):
        return True
