# Run this animation in nodebox goofus!

size(1280, 720)
speed(60)
 
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
    
    c = FOLCircle(550, 270)
    circles = []
    outer_circles = [c]
    outer_circle_draw_pct = 0
 
def draw():
    global circles
    global outer_circles
    global outer_circle_draw_pct
    
    background(0.12, 0.12, 0.06)
    nofill()
    stroke(1, 1, 1)
    strokewidth(1)
    
    if len(circles) > 2000:
        # hack to make animation stop by causing python to puke on an unknown token
        # which I call stop, for obvious reasons
        stop

    # draw old circles
    for circle in circles:
        circle.draw()
    
    # draw new outer row
    for circle in outer_circles:
        circle.draw_portion(outer_circle_draw_pct)

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