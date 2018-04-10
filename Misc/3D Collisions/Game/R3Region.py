import imp
Simplex = imp.load_source('Simplex', 'C:/Users/lukeh_000/Documents/Programs/Python/LinearPrograming/Simplex.py')
from Simplex import Tableau
import Graphics

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

class R3Region(Tableau):

    #  Vectors should be [[x1, x2, x3], boolean] True if lower bound, False otherwise.
    def __init__(self, vectors):
        self.m = []
        self.iLabels = []
        self.jLabels = []
        self.w = 4
        self.h = len(vectors)
        self.vectors = vectors
        #self.radius, self.center = 0, [0,0,0]
        self.wireFrame = [] #Filled in by getHamiltonianPath
        self.built = False
        self.tableau = False

    # This method crawls along in a twisting method which hits all of the vertices exactly once.
    def getHamiltonianPath(self):
        # Defines an arbitrary z, then gets minimum
        # Picks one with all positive values so it is feasible for dual lp
        self.addrow(self.h, [481, 516, 324, 2], "z ")
        res = Simplex.phase2(self)
        if not res:
            return []
        # Now goes backwards swirling. (Always goes to a new but minimal vertex)
        vertices = [self.anticyclerow()]
        point = self.getPoint()
        points = [point]
        while True:
            first = True
            for a in self.getVertices():
                vertex, c, z = a
                if vertex in vertices:
                    continue
                labels = ["x1", "x2", "x3"]
                endPoint = [0, 0, 0]
                for a in range(3):
                    label = labels[a]
                    r, s = c
                    if label in self.jLabels and self.index(label) != s and label != s: # or self.index(label) == r or label == r:
                        pass
                    elif label in self.jLabels:
                        # Post pivot doesn't work on rows being pivoted on so it is
                        endPoint[a] = -self.get(r, "1 ")/self.get(r, s)
                    else:
                        endPoint[a] = self.getPostPivot(r, s, label, "1 ")
                self.wireFrame += [[point, endPoint]]
                if first:
                    first = False
                    minimum = z
                    pivot = c
                elif z < minimum:
                    minimum = z
                    pivot = c
            if first:
                self.removerow("z ")
                return points
            r, s = pivot
            self.pivot(r,s)
            point = self.getPoint()
            vertices += [self.anticyclerow()]
            points += [point]

    # Finds a small sphere which bounds those points
    def sphereApprox(self, points):
        L = len(points)
        center = [0,0,0]
        if L == 0:
            return [center, 0]
        for point in points:
            center = add(center, point)
        center = scale(center, 1./L)
        radius = 0
        for point in points:
            dist = distance(point, center)
            if dist > radius:
                radius = dist
        return [center, radius]

    # Needs to sort points so not super efficent
    def volume(self, points):
        v = 0
        
        for i in range(len(points) - 3):
            base = negative(points[i])
            first = add(points[i+1], base)
            second = add(points[i+2], base)
            third = add(points[i+3], base)
            v += abs(dot(first, cross(second, third))/2)
        self.volume = v
    
    def build(self):
        self.built = True
        self.buildTableau()
        self.wireFrame = []
        points = self.getHamiltonianPath()
        self.center, self.radius = self.sphereApprox(points)
        self.volume(points)

    def buildTableau(self):
        if self.tableau:
            return
        self.tableau = True
        self.iLabels = ["x" + str(i + self.w) for i in range(self.h)]
        self.jLabels = ["x" + str(j + 1) for j in range(self.w - 1)] + ["1 "]
        for a in self.vectors:
            vector, sign = a
            pythagorean = sum(v**2 for v in vector)
            flipsign = 1
            if not sign:
                flipsign = -1
            self.m += [[flipsign*float(v) for v in vector] + [-flipsign*pythagorean]]
        
    # Gets the (x1, x2, x3) coordinate of current Tableau
    def getPoint(self):
        point = []
        for label in ["x1", "x2", "x3"]:
            if label in self.iLabels:
                point += [self.get(label, "1 ")]
            else:
                point += [0]
        return point
