from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE

from game.system import SystemWindow, System
from game import commands


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        fps_display = TextWidget(binding=lambda: round(self.clock.fps, 2), font_size=20, color=(0, 255, 0))
        ups_display = TextWidget(binding=lambda: round(self.clock.ups, 2), font_size=20, color=(50, 50, 255))
        
        self.widgets.add_widget(fps_display, (20, 20))
        self.widgets.add_widget(ups_display, (75, 20))

        self.keyboard_controller.bindings = {
            K_ESCAPE: commands.quit
        }
        
        self.system_window = SystemWindow(System())

    def _update(self, dt):
        pass

    def _draw(self, interpolation):
        self.system_window.render(self.display)

Game().run()
