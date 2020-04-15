# =====================================================
#                  Author Brad Heffernan
# =====================================================

import cairo
import gi
import shutil
import GUI
import Modal
import Functions as fn
import threading

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, Wnck, GLib, GdkX11  # noqa


class TransparentWindow(Gtk.Window):
    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_hibernate = "systemctl hibernate"
    cmd_lock = "betterlockscreen -l dimblur"
    wallpaper = "/usr/share/arcologout/wallpaper.jpg"
    d_buttons = ['cancel',
                 'shutdown',
                 'restart',
                 'suspend',
                 'hibernate',
                 'lock',
                 'logout']
    theme = "white"
    hover = "#ffffff"
    buttons = None
    active = False

    def __init__(self):
        super(TransparentWindow, self).__init__(type=Gtk.WindowType.POPUP, title="Arcolinux Logout")
        # Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(300, 220)
        self.connect('delete-event', self.on_close)
        self.connect('destroy', self.on_close)
        self.connect('draw', self.draw)
        # self.connect("key-press-event", self.on_keypress)
        self.connect("window-state-event", self.on_window_state_event)
        self.set_decorated(False)

        self.monitor = 0

        if not fn.os.path.isdir(fn.home + "/.config/arcologout"):
            fn.os.mkdir(fn.home + "/.config/arcologout")

        if not fn.os.path.isfile(fn.home + "/.config/arcologout/arcologout.conf"):
            shutil.copy(fn.config, fn.home + "/.config/arcologout/arcologout.conf")

        # s = Gdk.Screen.get_default()
        # self.width = s.width()
        # height = s.height()

        screens = Gdk.Display.get_default()
        s = screens.get_n_monitors()

        self.width = 0
        for x in range(s):
            sc = screens.get_monitor(x)
            rec = sc.get_geometry()
            self.width += rec.width

        screen = self.get_screen()

        monitor = screens.get_monitor(0)
        rect = monitor.get_geometry()

        self.single_width = rect.width
        height = rect.height

        self.resize(self.width, height)
        self.move(0, 0)

        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        fn.get_config(self, Gdk, Gtk, fn.config)

        if self.buttons is None or self.buttons == ['']:
            self.buttons = self.d_buttons

        self.fullscreen()
        self.set_app_paintable(True)
        self.present()
        
        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk, fn)
        if not fn.os.path.isfile("/tmp/arcologout.lock"):
            with open("/tmp/arcologout.lock", "w") as f:
                f.write("")
        self.show_all()
        Gtk.main()

    def on_save_clicked(self, widget):
        with open(fn.home + "/.config/arcologout/arcologout.conf", "r") as f:
            lines = f.readlines()
            f.close()

        pos_opacity = fn._get_position(lines, "opacity")
        pos_size = fn._get_position(lines, "icon_size")
        pos_theme = fn._get_position(lines, "theme=")
        pos_color = fn._get_position(lines, "hover_color")

        lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_text())) + "\n"
        lines[pos_size] = "icon_size=" + str(int(self.icons.get_text())) + "\n"
        lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
        lines[pos_color] = "hover_color=" + self.hovers.get_text() + "\n"

        with open(fn.home + "/.config/arcologout/arcologout.conf", "w") as f:
            f.writelines(lines)
            f.close()
        self.popover.popdown()

    def on_mouse_in(self, widget, event, data):
        if data == "S":
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/shutdown_blur.svg'), self.icon, self.icon)
            self.imagesh.set_from_pixbuf(psh)
            self.lbl1.set_markup("<span foreground=\"" + self.hover + "\">Shutdown</span>")
        elif data == "R":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/restart_blur.svg'), self.icon, self.icon)
            self.imager.set_from_pixbuf(pr)
            self.lbl2.set_markup("<span foreground=\"" + self.hover + "\">Reboot</span>")
        elif data == "U":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/suspend_blur.svg'), self.icon, self.icon)
            self.images.set_from_pixbuf(ps)
            self.lbl3.set_markup("<span foreground=\"" + self.hover + "\">Suspend</span>")
        elif data == "K":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/lock_blur.svg'), self.icon, self.icon)
            self.imagelk.set_from_pixbuf(plk)
            self.lbl4.set_markup("<span foreground=\"" + self.hover + "\">Lock</span>")
        elif data == "L":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/logout_blur.svg'), self.icon, self.icon)
            self.imagelo.set_from_pixbuf(plo)
            self.lbl5.set_markup("<span foreground=\"" + self.hover + "\">Logout</span>")
        elif data == "Escape":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/cancel_blur.svg'), self.icon, self.icon)
            self.imagec.set_from_pixbuf(plo)
            self.lbl6.set_markup("<span foreground=\"" + self.hover + "\">Cancel</span>")
        elif data == "H":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/hibernate_blur.svg'), self.icon, self.icon)
            self.imageh.set_from_pixbuf(plo)
            self.lbl7.set_markup("<span foreground=\"" + self.hover + "\">Hibernate</span>")
        elif data == "P":
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'configure_blur.svg'), 48, 48)
            self.imageset.set_from_pixbuf(pset)
        elif data == 'light':
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'light_blur.svg'), 48, 48)
            self.imagelig.set_from_pixbuf(pset)
        event.window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))

    def on_mouse_out(self, widget, event, data):
        if not self.active:
            if data == "S":
                psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/shutdown.svg'), self.icon, self.icon)
                self.imagesh.set_from_pixbuf(psh)
                self.lbl1.set_markup("Shutdown")
            elif data == "R":
                pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/restart.svg'), self.icon, self.icon)
                self.imager.set_from_pixbuf(pr)
                self.lbl2.set_markup("Reboot")
            elif data == "U":
                ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/suspend.svg'), self.icon, self.icon)
                self.images.set_from_pixbuf(ps)
                self.lbl3.set_markup("Suspend")
            elif data == "K":
                plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/lock.svg'), self.icon, self.icon)
                self.imagelk.set_from_pixbuf(plk)
                self.lbl4.set_markup("Lock")
            elif data == "L":
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/logout.svg'), self.icon, self.icon)
                self.imagelo.set_from_pixbuf(plo)
                self.lbl5.set_markup("Logout")
            elif data == "Escape":
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/cancel.svg'), self.icon, self.icon)
                self.imagec.set_from_pixbuf(plo)
                self.lbl6.set_markup("Cancel")
            elif data == "H":
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/hibernate.svg'), self.icon, self.icon)
                self.imageh.set_from_pixbuf(plo)
                self.lbl7.set_markup("Hibernate")
            elif data == "P":
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'configure.svg'), 48, 48)
                self.imageset.set_from_pixbuf(pset)
            elif data == 'light':
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'light.svg'), 48, 48)
                self.imagelig.set_from_pixbuf(pset)

    def on_click(self, widget, event, data):
        self.click_button(widget, data)

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)  # noqa

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, self.opacity)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    # def on_keypress(self, widget=None, event=None, data=None):
    #     self.shortcut_keys = ["Escape", "S", "R", "U", "L", "K", "H", "P"]

    #     for key in self.shortcut_keys:
    #         if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
    #             self.click_button(widget, key)

    def click_button(self, widget, data=None):

        if not data == "P" and not data == "light":
            self.active = True
            fn.button_toggled(self, data)
            fn.button_active(self, data, GdkPixbuf)

        if (data == "L"):
            command = fn._get_logout()
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(command)
            Gtk.main_quit()

        elif (data == "R"):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_restart)
            Gtk.main_quit()

        elif (data == "S"):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_shutdown)
            Gtk.main_quit()

        elif (data == "U"):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_suspend)
            Gtk.main_quit()

        elif (data == "H"):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_hibernate)
            Gtk.main_quit()

        elif (data == "K"):
            if not fn.os.path.isdir(fn.home + "/.cache/i3lock"):
                if fn.os.path.isfile(self.wallpaper):
                    self.lbl_stat.set_markup("<span size=\"x-large\"><b>Caching lockscreen images for a faster locking next time</b></span>")  # noqa
                    t = threading.Thread(target=fn.cache_bl,
                                         args=(self, GLib, Gtk,))
                    t.daemon = True
                    t.start()
                else:
                    self.lbl_stat.set_markup("<span size=\"x-large\"><b>You need to set the wallpaper path in arcologout.conf</b></span>")  # noqa
                    self.Ec.set_sensitive(True)
                    self.active = False
            else:
                fn.os.unlink("/tmp/arcologout.lock")
                self.__exec_cmd(self.cmd_lock)
                Gtk.main_quit()
        elif (data == "P"):
            self.themes.grab_focus()
            self.popover.set_relative_to(self.Eset)
            self.popover.show_all()
            self.popover.popup()
        elif (data == 'light'):
            self.popover2.set_relative_to(self.Elig)
            self.popover2.show_all()
            self.popover2.popup()
        else:
            fn.os.unlink("/tmp/arcologout.lock")
            Gtk.main_quit()

    def modal_close(self, widget, signal):
        print(self.state)

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)

    def on_close(self, widget, data):
        fn.os.unlink("/tmp/arcologout.lock")
        Gtk.main_quit()

    def message_box(self, message, title):
        md = Gtk.MessageDialog(parent=self,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.YES_NO,
                               text=title)
        md.format_secondary_markup(message)  # noqa

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            return True
        else:
            return False


if __name__ == "__main__":
    if not fn.os.path.isfile("/tmp/arcologout.lock"):
        with open("/tmp/arcologout.pid", "w") as f:
            f.write(str(fn.os.getpid()))
            f.close()
        TransparentWindow()
        # w.show_all()
        # Gtk.main()
    else:
        print("something")
