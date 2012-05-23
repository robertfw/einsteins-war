from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE

from game.system import SystemWindow, System
from game import commands


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        fps_display = TextWidget(binding=lambda: self.clock.fps, font_size=20, color=(0, 255, 0))
        ups_display = TextWidget(binding=lambda: self.clock.ups, font_size=20, color=(50, 50, 255))
        
        self.widgets.add_widget(fps_display, (800, 600))
        self.widgets.add_widget(ups_display, (800, 585))

        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        self.scale_demo()

    def scale_demo(self):
        #create a new window, make it the full size of our current display
        self.system_window = SystemWindow(system=System(), rect=((0, 0), self.display.resolution))
        self.windows.add_window(self.system_window)
        scale_display = TextWidget(binding=lambda: self.system_window.scale, font_size=20, color=(50, 255, 255))
        self.widgets.add_widget(scale_display, (800, 570))

        def scale_demo_update(dt):
            self.system_window.scale = self.system_window.scale / 1.01

        self.register_update_callback(scale_demo_update)


Game(resolution=(800, 600)).run()
