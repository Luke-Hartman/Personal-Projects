import Config
import Graphics
import Sound
import LoadModel
from R3Region import R3Region
from Hull import Hull

#Problems:

# Also for some reason the R3Regions seem to be reacting/merging some times
# Sometimes the center fix doesn't seem to work as the planes can get strange

# Collision seems to create empty collisions sometimes but not always? phase1 must be returning true when it ought not.
# Using a temp band-aid fix atm.

# Graphics and FOV is wonky.

sin = Graphics.sin
cos = Graphics.cos
tan = Graphics.tan
rotate = Graphics.rotate
scale = Graphics.scale
dot = Graphics.dot
cross = Graphics.cross
magnitude = Graphics.magnitude
normalize = Graphics.normalize
add = Graphics.add
negative = Graphics.negative
distance = Graphics.distance
decompose = Graphics.decompose
recompose = Graphics.recompose
project = Graphics.project

f = [1, 0, 0]
basis = Graphics.createBasis(f)
o = [-1000, 0, 150.5]

vectors = [[[200, 0, 0], False], [[0, 200, 0], False], [[0, 0, 200], False],
           [[150, 0, 0], True],  [[0, 100, 0], True],  [[0, 0, 100], True]]

vectors2 = [[[251, 0, 0], False], [[0, 200, 0], False], [[0, 0, 200], False],
            [[200, 0, 0], True],  [[0, 100, 0], True],  [[0, 0, 100], True]]

vectors3 = [[[200, 0, 0], False], [[0, 350, 0], False], [[0, 0, 200], False],
            [[100, 0, 0], True],  [[0, 250, 0], True],  [[0, 0, 100], True]]

blenderImport = LoadModel.getHull(LoadModel.test)

T = R3Region(vectors)
T2 = R3Region(vectors2)
T3 = R3Region(vectors3)
Cube = Hull([T,T2])
#Cube = blenderImport
print len(Cube.hitBoxes)
Cube2 = Hull([T3])
Collision = None

while True:
    dx, dy = Graphics.update()

    # Prevents jerks when the game first starts
    if (dx*Config.xSensitivity)**2 + (dy*Config.ySensitivity)**2 > 1000:
        dx = dy = 0
    dt = Graphics.clock.get_time()
    f = normalize(rotate(f, dy*Config.ySensitivity, dx*Config.xSensitivity))
    f, u, r = basis = Graphics.createBasis(f)
    key = Graphics.getKeys()
    keyW = key[119]
    keyA = key[97]
    keyS = key[115]
    keyD = key[100]
    keySpace = key[32]
    keyControl = key[306]

    arrowUp = key[273]
    arrowDown = key[274]
    arrowRight = key[275]
    arrowLeft = key[276]
    
    displacement = [0,0,0]
    move = False
    if keyW + keyS == 1: # This is xor
        displacement = scale(f, keyW - keyS)
        move = True
    if keyA + keyD == 1:
        displacement = add(displacement, scale(r, keyD - keyA))
        move = True
    if move:
        displacement = scale(normalize(add(displacement, [0,0,-displacement[-1]])), Config.walkSpeed*dt/17)
        o = add(o, displacement)

    displacement = [0,0,0]
    move = False
    if arrowUp + arrowDown == 1: # This is xor
        displacement = scale([1, 0, 0], arrowUp - arrowDown)
        move = True
    if arrowLeft + arrowRight == 1:
        displacement = add(displacement, scale([0, 1, 0], arrowLeft - arrowRight))
        move = True
    if keySpace + keyControl == 1:
        displacement = add(displacement, scale([0, 0, keySpace - keyControl], Config.walkSpeed*dt/17))
        move = True
    if move:
        displacement = scale(normalize(displacement), Config.walkSpeed*dt/5/17)
        Cube.translate(displacement)
        Cube.reorient(basis)
        Cube.buildWireFrame() #Uncomment this to allow visible clipping through edges
        Collision = Cube.getCollision(Cube2)
        #if Collision != None:
            #print Collision.volume()
    Graphics.wipe()
    Graphics.drawLine((0,0,0), (255.0, 0, 0), o, basis, (255,0,0))
    Graphics.drawLine((0,0,0), (0, 255.0, 0), o, basis, (0,255,0))
    Graphics.drawLine((0,0,0), (0, 0, 255.0), o, basis, (0,0,255))
    Cube.draw(o, basis)
    Cube2.draw(o, basis, color=(0,0,255))
    if Collision != None:
        #if Collision.radius != 0:
        #    Sound.test()
        Collision.draw(o, basis, color=(255,0,0), thickness=2)
