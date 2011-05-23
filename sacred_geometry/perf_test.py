size(1280, 720)
speed(100)
 
def setup():
    global i
    i = 1
    
def draw():
    global i
    print i
    nofill()
    stroke(0,0,0)
    

    # big path, optimum?
    big_path = oval(0,0,5,5, draw=False)
    for x in range(i):
        for y in range(i):
            p = oval(x*5,y*5,5,5, draw=False)
            big_path.extend(p)
            
    drawpath(big_path)
    
    """
    # many paths, not optimum?
    oval(0,0,5,5)
    for x in range(i):
        for y in range(i):
            oval(x*5,y*5,5,5)
    """
            
    i += 1