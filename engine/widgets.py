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

    #TODO: see if there is a nicer way to handle this
    def get_widget(self, name):
        return self.widgets[self.widget_map[name]]


class BaseWidget(Sprite):
    pass


class TextWidget(BaseWidget):
    text = ''
    font_size = None
    font = None
    color = None

    def __init__(self, font_size=12, font=None, color=(0, 255, 0)):
        self.font_size = font_size
        self.font = font
        self.color = color

    def set_text(self, text):
        self.text = str(text)

    def update_image(self):
        #TODO: should only re-render if text has changed
        obj = Font(self.font, self.font_size)
        self.image = obj.render(self.text, True, self.color)

    def set_rect_pos(self, pos):
        self.rect.topleft = pos
