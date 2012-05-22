from render import Sprite
from pygame.font import Font


class WidgetHandler(object):
    widgets = {}
    widget_map = {}

    def get_widget_map(self):
        return self.widgets

    #TODO: should return a handler for future reference
    def add_widget(self, widget, pos=(0, 0)):
        self.widgets[pos] = widget

    def update(self, interpolation):
        for pos in self.widgets:
            self.widgets[pos].update_value(interpolation)


class BaseWidget(Sprite):
    value = None
    binding = None

    def __init__(self, binding):
        self.binding = binding

    def update_value(self, interpolation):
        new_value = self.binding()
        if new_value != self.value:
            self.value = new_value
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
        self.rect.bottomright = pos
