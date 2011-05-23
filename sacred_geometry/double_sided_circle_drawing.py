size(1280, 720)
speed(30)

from math import pi, sin, cos, radians, sqrt

# our circle class
class FOLCircle:
    def __init__(self, x, y, radius=90):
        self.x = x
        self.y = y
        self.radius = radius
        path = oval(self.x, self.y, self.radius * 2, self.radius * 2, draw=False)
        self.path = path
        # point precision is 100 to make percent based logic easy
        self.path_points = path.points(100)
        
    def draw(self):
        drawpath(self.path)
    
    # draw a portion of the circle, starting with the point nearest given x,y coords
    def draw_portion(self, x, y, percent=100):
        oval(x - 10, y - 10, 20, 20)
        print len(list(self.path_points))
        
        mid_index = 50
        top_index = mid_index + (percent/2)
        bot_index = mid_index - (percent/2)
        
        # point precision is 100 here, makes working with percents easy
        path_points = list(self.path.points(amount=100))
        mid_point = point_nearest(x,y,path_points)
        
        target = path_points.index(mid_point)
        rotation_amount = mid_index - target + 1
        path_points = rotate_list(rotation_amount, path_points)
    
        if percent > 0:
            curve1 = path_points[mid_index:top_index]
            curve2 = path_points[bot_index:mid_index + 1]
            if len(curve1) > 0:
                subpath = findpath(curve1)
                subpath.extend(findpath(curve2))
                drawpath(subpath)
        
        
def rotate_list(amount,lst):
    if amount == 0:
        return lst
    if amount > 0:
        above = lst[-amount:-1]
        rest = lst[0:-amount + 1]
        below = []
    else:
        above = []
        rest = lst[abs(amount):]
        below = lst[0:abs(amount)]
        
    above.extend(rest)
    above.extend(below)
    return above
            
def sort_distance_from_point(x,y,points):
    deltas2points = {}
    for point in points:
        dx = abs(x - point.x)
        dy = abs(y - point.y)
        delta = sqrt(dx**2 + dy**2)
        deltas2points[point] = delta
    # reverse index, make into list of lists, sort list by value (delta)
    # grab last (lowest delta), get the second value (the original point object)
    sorted_deltas2points = sorted([(value,key) for (key,value) in deltas2points.items()])
    points = [delta_point[1] for delta_point in sorted_deltas2points]
    return points
        
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
    circle.draw_portion(700,600,percent_to_draw)
    
    if percent_to_draw >= 100:
        percent_to_draw = 0
    else:
        percent_to_draw += 1