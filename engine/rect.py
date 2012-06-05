class Rect(object):
    def __init__(self, args):
        self.top = args[0][0]
        self.left = args[0][1]
        self.width = args[1][0]
        self.height = args[1][1]

        self.dirty = True

    def __repr__(self):
        return '(({top:,.2f}, {left:,.2f}), ({width:,.2f}, {height:,.2f}))'.format(top=self.top, left=self.left, height=self.height, width=self.width)

    def _update(self):
        self._bottom = self.top + self.height
        self._right = self.left + self.width
        self.center = (self.top + (self.height / 2), self.left + (self.height / 2))

        self.dirty = False

    @property
    def bottom(self):
        if self.dirty:
            self._update()

        return self._bottom

    @bottom.setter
    def bottom(self, value):
        self.top = value - self.height
        self.dirty = True

    @property
    def right(self):
        if self.dirty:
            self._update()

        return self._right

    @right.setter
    def right(self, value):
        self.left = value - self.width
        self.dirty = True
