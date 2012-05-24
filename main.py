from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_KP_PLUS, K_KP_MINUS, K_UP, K_DOWN, K_LEFT, K_RIGHT

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

        def zoom_in():
            self.system_window.scale = self.system_window.scale * 1.1

        def zoom_out():
            self.system_window.scale = self.system_window.scale / 1.1

        def pan_up():
            self.system_window.center = (self.system_window.center[0], self.system_window.center[1] + 10)

        def pan_down():
            self.system_window.center = (self.system_window.center[0], self.system_window.center[1] - 10)

        def pan_left():
            self.system_window.center = (self.system_window.center[0] + 10, self.system_window.center[1])

        def pan_right():
            self.system_window.center = (self.system_window.center[0] - 10, self.system_window.center[1])

        self.keyboard.set_repeat(100, 100)
        self.keyboard.bindings[K_KP_PLUS] = zoom_in
        self.keyboard.bindings[K_KP_MINUS] = zoom_out
        self.keyboard.bindings[K_UP] = pan_up
        self.keyboard.bindings[K_DOWN] = pan_down
        self.keyboard.bindings[K_LEFT] = pan_left
        self.keyboard.bindings[K_RIGHT] = pan_right


Game(resolution=(800, 600)).run()
