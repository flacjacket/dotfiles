from libqtile.widget import base

import cairocffi


class IconTextBox(base._TextBox):
    defaults = [
        ('update_interval', 5, 'The update interval'),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, text='Not Connected', **config)
        self.add_defaults(IconTextBox.defaults)

        self._icon_size = 0, 0
        self.icon_current = []
        self.icon_widths = []
        self.icon_gen = []

    @property
    def icon_size(self):
        return self._icon_size

    @icon_size.setter
    def icon_size(self, value):
        self._icon_size = value

    def timer_setup(self):
        self.update()
        self.timeout_add(self.update_interval, self.timer_setup)

    def update(self):
        old_width = self.width
        old_icon_gen = self.icon_gen
        old_text = self.text

        self.icon_gen, self.text = self.poll()

        if old_icon_gen != self.icon_gen:
            self.update_icons()

        if old_icon_gen != self.icon_gen or old_text != self.text:
            if self.width == old_width:
                self.draw()
            else:
                self.bar.draw()

    def update_icons(self):
        w, h = self.icon_size
        sp = h / float(self.bar.height - 1)

        icons = []
        widths = []
        for gen in self.icon_gen:
            img = cairocffi.ImageSurface(cairocffi.FORMAT_ARGB32, w, h)
            ctx = cairocffi.Context(img)

            self.gen_icon(gen, ctx)

            scaler = cairocffi.Matrix()
            scaler.scale(sp, sp)

            imgpat = cairocffi.SurfacePattern(img)
            imgpat.set_matrix(scaler)
            imgpat.set_filter(cairocffi.FILTER_BEST)

            icons.append(imgpat)
            widths.append(w / sp)

        self.icon_current = icons
        self.icon_widths = widths

    def poll(self):
        return [], 'N/A'

    def gen_icon(self, value, ctx):
        pass

    def calculate_length(self):
        width = sum(self.icon_widths) + len(self.icon_widths) * self.actual_padding

        if self.text:
            width += self.layout.width + self.actual_padding

        if width:
            width += self.actual_padding

        return width

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        icon_width = self.actual_padding
        for icon, width in zip(self.icon_current, self.icon_widths):
            scaler = icon.get_matrix()
            xx, yx, xy, yy, x0, y0 = scaler.as_tuple()
            scaler.translate(-(x0 / xx + icon_width), 0)
            icon.set_matrix(scaler)

            icon_width += width + self.actual_padding

            self.drawer.ctx.set_source(icon)
            self.drawer.ctx.paint()

        if self.text:
            self.layout.draw(
                icon_width,
                int(self.bar.height / 2 - self.layout.height / 2) + 1
            )

        self.drawer.draw(offsetx=self.offset, width=self.width)
