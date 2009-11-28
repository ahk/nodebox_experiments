# Run this animation in nodebox goofus!

size(1280, 720)
speed(60)
 
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
        print len(list(self.path_points))
        # point precision is 100 here, makes working with percents easy
        path_points = list(self.path.points(amount=100))
        
        # trickery to loop through the list from the beginning
        # if we reach the end before we've gotten enough points
        # smash both of these together at the end
        start_point = point_nearest(x, y, path_points)
        start_index = path_points.index(start_point)
        # smaller of percent or remaining items
        end_index = sorted([(start_index + percent), len(path_points)])[0]
        
        chunk = path_points[start_index:end_index]
        remaining = percent - len(chunk)
        if remaining > 0:
            chunk2 = path_points[0:remaining]
            chunk.extend(chunk2)
        
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
    return point

      
# list of coordinates for the next generation of FOLCircles built
# off a given circle
def new_coords_for(circle, num_circles):
    coords_list = []
    # do some math here to gen an appropriate list of angles
    angles = [(i*(360/num_circles)) for i in range(num_circles)]
    for angle in angles:
        coords_list.append(coords_relative_to(circle, angle))
    return coords_list
    
# single x,y coordinate pair whose center occurs on the circumference 
# of the given circle at the given angle (in degrees)
def coords_relative_to(circle, angle):
    """ (x_?,y_?) = (x + radius * cos(angle), radius * sin(angle)) """
    rads = radians(angle)
    x = circle.x + (circle.radius * cos(rads))
    y = circle.y + (circle.radius * sin(rads))
    return [x,y]
    
# instantiate FOLCircles based on a set of coordinates
def generate_circles_from_coords(coords):
    # make unique: like [[1,2],[1,2],[1,3]]
    unique_coords = []
    for xy in coords:
        matches = False
        for other_xy in unique_coords:
            if xy == other_xy:
                matches = True
        if matches == False:
            unique_coords.append(xy)
    # instantiate circles by x,y
    # circles = [FOLCircle(c[0], c[1]) for c in unique_coords]
    return [FOLCircle(c[0], c[1]) for c in unique_coords]

# strip out any coordinates (for circles) that would be layed over 
# top those already found in the master list
def drop_redundant_circles(new_list, master_list):
    master_coords = [[c.x, c.y] for c in master_list]
    
    # find all the redundant circles by whether or not we already have a circle
    # at those coordinates
    redundant = []
    for circle in new_list:
        for coords in master_coords:
            if [circle.x, circle.y] == coords:
                redundant.append(circle)
            
    # difference the potential new circles with the known redundant
    good_list = list( set(new_list).difference(set(redundant)) )
    return good_list

def setup():
    global circles
    global outer_circles
    global outer_circle_draw_pct
    global frame
    
    c = FOLCircle(550, 270)
    circles = []
    outer_circles = [c]
    outer_circle_draw_pct = 0
    frame = 0
 
def draw():
    global circles
    global outer_circles
    global outer_circle_draw_pct
    global frame
    
    frame += 1
    
    background(0.12, 0.12, 0.06)
    nofill()
    stroke(1, 1, 1)
    strokewidth(3)
    
    if len(circles) > 2500:
        # hack to make animation stop by causing python to puke on an unknown token
        # which I call stop, for obvious reasons
        stop

    # draw old circles
    for circle in circles:
        circle.draw()
    
    # draw new outer row
    for circle in outer_circles:
        stroke(1,1,1)
        circle.draw_portion(640,360,outer_circle_draw_pct)

    if outer_circle_draw_pct >= 100:
        # reset drawing progress
        outer_circle_draw_pct = 0
        
        # add outer row to old
        circles.extend(outer_circles)
        potential_coords = []
        for circle in outer_circles:
            coords = new_coords_for(circle, 6)
            potential_coords.extend(coords)

        new_circles = generate_circles_from_coords(potential_coords)
        # drop any that might overlap circles we've already made
        new_circles = drop_redundant_circles(new_circles, circles)
        outer_circles = new_circles
    else:
        outer_circle_draw_pct += 1
    
    canvas.save("partial" + str(frame) + ".png")
    canvas.clear()