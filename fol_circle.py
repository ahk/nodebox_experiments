size(1280, 720)
speed(1)
 
from math import pi, sin, cos, radians
 
# our circle class
class FOLCircle:
    def __init__(self, x, y, radius=90):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self):
        oval(self.x, self.y, self.radius * 2, self.radius * 2)    
      
# list of coordinates for the next generation of FOLCircles built
# off a given circle
def new_coords_for(circle):
    coords_list = []
    angles = [-90, -30, 30, 90, 150, 210]
    for angle in angles:
        coords_list.append(coords_relative_to(circle, angle))
    return coords_list
    
# single x,y coordinate pair whose center occurs on the circumference 
# of the given circle at the given angle
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
    c = FOLCircle(550, 270)
    circles = [c]
    outer_circles = [c]
 
def draw():
    global circles
    global outer_circles
    if len(circles) > 10000:
        stop
        
    background(0.12, 0.12, 0.06)
    nofill()
    stroke(1, 1, 1)
    strokewidth(6)

    for circle in circles:
        circle.draw()

    potential_coords = []
    for circle in outer_circles:
        coords = new_coords_for(circle)
        potential_coords.extend(coords)

    new_circles = generate_circles_from_coords(potential_coords)
    # drop any that might overlap circles we've already made
    new_circles = drop_redundant_circles(new_circles, circles)    
    circles.extend(new_circles)
    outer_circles = new_circles