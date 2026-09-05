import pymunk

class Wall:
    def __init__(self, space, p1, p2, thickness=15):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, thickness)
        self.shape.elasticity = 0.85
        self.shape.friction = 0.5
        space.add(self.body, self.shape)
        self.p1 = p1
        self.p2 = p2