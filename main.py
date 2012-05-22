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
        
        self.widgets.add_widget(fps_display, (750, 600))
        self.widgets.add_widget(ups_display, (800, 600))

        self.keyboard_controller.bindings = {
            K_ESCAPE: commands.quit
        }

        self.windows.add_window(SystemWindow(system=System(), rect=((0, 0), self.display.resolution)))

    def _update(self, dt):
        pass

    def _draw(self, interpolation):
        pass

Game(resolution=(800, 600)).run()
