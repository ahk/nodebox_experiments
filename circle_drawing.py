size(1280, 720)
speed(30)

from math import pi, sin, cos, radians

# our circle class
class FOLCircle:
    def __init__(self, x, y, radius=90):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self):
        oval(self.x, self.y, self.radius * 2, self.radius * 2)    
        
    def draw_portion(self, percent=100):
        path = oval(self.x, self.y, self.radius * 2, self.radius * 2, draw=False)
        points = list(path.points(amount=100))
        subpath_points = points[0:percent + 1]
        subpath = findpath(subpath_points, 1)
        drawpath(subpath)

def setup():
    global circle
    circle = FOLCircle(550, 270)
    
    global percent_to_draw
    percent_to_draw = 0

def draw():
    global circle
    global percent_to_draw
    
    background(0.12, 0.12, 0.06)
    nofill()
    stroke(1, 1, 1)
    strokewidth(1)
    circle.draw_portion(percent_to_draw)
    
    if percent_to_draw >= 100:
        percent_to_draw = 0
    else:
        percent_to_draw += 1