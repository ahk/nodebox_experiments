size(1280, 720)
speed(30)

from math import pi, sin, cos, radians, sqrt

# our circle class
class FOLCircle:
    def __init__(self, x, y, radius=90):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self):
        oval(self.x, self.y, self.radius * 2, self.radius * 2)    
    
    # draw a portion of the circle, starting with the point nearest given x,y coords
    def draw_portion(self, x, y, percent=100):
        path = oval(self.x, self.y, self.radius * 2, self.radius * 2, draw=False)
        # point precision is 100 here, makes working with percents easy
        path_points = list(path.points(amount=100))
        
        # trickery to loop through the list from the beginning
        # if we reach the end before we've gotten enough points
        # smash both of these together at the end
        start_point = point_nearest(x, y, path_points)
        start_index = path_points.index(start_point)
        # smaller of percent or remaining items
        end_index = sorted([(start_index + percent), len(path_points)])[0]
        print "slice1: " + str(start_index) + ":" + str(end_index)
        
        chunk = path_points[start_index:end_index]
        remaining = percent - len(chunk)
        if remaining > 0:
            chunk2 = path_points[0:remaining]
            print "slice2: 0:" + str(remaining)
            chunk.extend(chunk2)
        
        print "points: " + str(len(chunk))
        if len(chunk) > 0:
            subpath = findpath(chunk)
            drawpath(subpath)
        
def point_nearest(x,y, points):
    deltas2points = {}
    for point in points:
        dx = abs(x - point.x)
        dy = abs(y - point.y)
        delta = sqrt(dx**2 + dy**2)
        deltas2points[point] = delta
    # reverse index, make into list of lists, sort list by value (delta)
    # grab last (lowest delta), get the second value (the original point object)
    point = sorted([(value,key) for (key,value) in deltas2points.items()])[0][1]
    oval(x - 10, y - 10, 20, 20)
    oval(point.x - 10, point.y - 10, 20, 20)
    return point
        
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
    circle.draw_portion(0,0,percent_to_draw)
    
    if percent_to_draw >= 100:
        percent_to_draw = 0
    else:
        percent_to_draw += 1