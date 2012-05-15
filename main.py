from engine.core import GameCore


class Game(GameCore):

    def _update(self, interpolation):
        self._handle_events()

    def _draw(self, dt):
        self.widgets.get_widget('fps_display').set_text('fps: {fps}'.format(fps=round(self.clock.fps, 2)))
        self.widgets.get_widget('ups_display').set_text('ups: {ups}'.format(ups=round(self.clock.ups, 2)))

        self.renderer.reset_view()
        self.renderer.draw_sprite_map(self.widgets.get_widget_map())
        self.renderer.update()
    

Game().run()
