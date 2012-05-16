from engine.core import GameCore
from engine.widgets import TextWidget
from engine.utils import quit
from pygame.locals import K_ESCAPE


class Game(GameCore):

    def __init__(self):
        super(Game, self).__init__()

        fps_display = TextWidget(font_size=20, color=(0, 255, 0))
        ups_display = TextWidget(font_size=20, color=(50, 50, 255))
        self.widgets.add_widget('fps_display', fps_display, (20, 20))
        self.widgets.add_widget('ups_display', ups_display, (20, 100))

        self.keyboard_controller.bindings = {
            K_ESCAPE: quit
        }

    def _update(self, dt):
        pass

    def _draw(self, interpolation):
        pass

    def _update_widgets(self, interpolation):
        self.widgets.get_widget('fps_display').set_text('fps: {fps}'.format(fps=round(self.clock.fps, 2)))
        self.widgets.get_widget('ups_display').set_text('ups: {ups}'.format(ups=round(self.clock.ups, 2)))


Game().run()
