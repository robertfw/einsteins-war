class Map(object):
    objects = {}

    def add_object(self, obj, pos):
        self.objects[pos] = obj
