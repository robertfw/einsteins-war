from render import Sprite
from pygame.font import Font


class WidgetHandler(object):
    widgets = {}
    widget_map = {}

    def get_widget_map(self):
        return self.widgets

    def add_widget(self, name, widget, pos=(0, 0)):
        self.widgets[pos] = widget
        self.widget_map[name] = pos

    def update(self, interpolation):
        for pos in self.widgets:
            self.widgets[pos].update_value(interpolation)

    #TODO: see if there is a nicer way to handle this
    def get_widget(self, name):
        return self.widgets[self.widget_map[name]]


class BaseWidget(Sprite):
    value = None
    binding = None

    def __init__(self, binding):
        self.binding = binding

    def update_value(self, interpolation):
        self.value = self.binding()
        self.update_image()


class TextWidget(BaseWidget):
    font_size = None
    font = None
    color = None

    def __init__(self, binding=None, font_size=12, font=None, color=(0, 255, 0)):
        super(TextWidget, self).__init__(binding)

        self.font_size = font_size
        self.font = font
        self.color = color

    def update_image(self):
        obj = Font(self.font, self.font_size)
        self.image = obj.render(str(self.value), True, self.color)

    def set_rect_pos(self, pos):
        self.rect.topleft = pos
