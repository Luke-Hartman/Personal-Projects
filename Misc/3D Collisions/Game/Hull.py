from R3Region import R3Region, Simplex
import Config
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

class Hull:
    
    def __init__(self, R3Regions):
        self.hitBoxes = R3Regions
        self.wireFrame = []
        self.buildWireFrame()
        spheres = []
        self.basis = Graphics.createBasis([1, 0, 0])
        self.center, self.radius = self.sphereApprox()

    def getCollision(self, other):
        Collision = []
        Hit = False
        for hitBoxSelf in self.hitBoxes:
            if hitBoxSelf.built is False:
                hitBoxSelf.build()
        for hitBoxOther in other.hitBoxes:
            if hitBoxOther.built is False:
                hitBoxOther.build()
            for hitBoxSelf in self.hitBoxes:
                if hitBoxOther.radius + hitBoxOther.radius < distance(hitBoxOther.center, hitBoxSelf.center):
                    continue
                collisionRegion = R3Region(hitBoxOther.vectors + hitBoxSelf.vectors)
                collisionRegion.build()
                #print collisionRegion.volume
                if Simplex.phase1(collisionRegion):
                    Hit = True
                    Collision += [collisionRegion]
        if Hit:
            # This is a temporary fix for Hit being true when it shouldn't be
            # Normal behavior is just return Hull(Collision) or nothing.
            H = Hull(Collision)
            if H.radius != 0:
                return H
        #print "miss"
        return None

    def sphereApprox(self):
        spheres = []
        for hitBox in self.hitBoxes:
            spheres += [[hitBox.center, hitBox.radius]]
        L = len(spheres)
        if L == 0:
            return [center, 0]
        center = [0,0,0]
        for sphere in spheres:
            center = add(center, sphere[0])
        center = scale(center, 1./L)
        radius = 0
        for sphere in spheres:
            dist = distance(sphere[0], center)
            if dist + sphere[1] > radius:
                radius = dist + sphere[1]
        return [center, radius]

    def volume(self):
        for hitBox in self.hitBoxes:
            if hitBox.built is False:
                hitBox.build()
            print hitBox.volume
        return sum(hitBox.volume for hitBox in self.hitBoxes)
        
    def draw(self, o, basis, color=Config.lineColor, thickness=1):
        f, u, r = basis
        c = self.center
        F = dot(c, f)
        U = dot(c, u)
        R = dot(c, r)
        #if (U**2 + R**2)**0.5 - self.radius < tan(Config.FOV/2)*F:
        for line in self.wireFrame:
            Graphics.drawLine(line[0], line[1], o, basis, color, thickness=thickness)

    def buildWireFrame(self):
        newWireFrame = []
        for hitBox in self.hitBoxes:
            if hitBox.built is False:
                hitBox.build()
            for line in hitBox.wireFrame:
                lineflip = [line[1], line[0]]
                if line not in newWireFrame and lineflip not in newWireFrame:
                    newWireFrame += [line]
        self.wireFrame = newWireFrame

    # More complicated rotations are all to be on the children of Hull
    def translate(self, displacement):
        newHitBoxes = []
        for hitBox in self.hitBoxes:
            newVectors = []
            for a in hitBox.vectors:
                vector, sign = a
                vDir = normalize(vector)
                projection = project(displacement, vDir)
                #If during translation plane crosses over origin, need to flip sign
                if dot(add(vector, projection), vDir) < 0:
                    sign = not sign
                newVectors += [[add(vector, projection), sign]]
            newHitBoxes += [R3Region(newVectors)]
            hitBox.center = add(hitBox.center, displacement)
        self.hitBoxes = newHitBoxes
        newWireFrame = []
        for line in self.wireFrame:
            start, end = line
            newWireFrame += [[add(start, displacement), add(end, displacement)]]
        self.wireFrame = newWireFrame
        self.center = add(self.center, displacement)

    def reorient(self, basis):
        newHitBoxes = []
        f, u, r = self.basis
        for hitBox in self.hitBoxes:
            newVectors = []
            for a in hitBox.vectors:
                vector, sign = a

                projection = project(self.center, normalize(vector))
                
                # If plane goes through center
                Fix = False
                if vector == projection:
                    Fix = True
                    cut = scale(vector, 0.5)
                    vector = cut
                
                # Perp defines the plane as if the point of rotation is the origin.
                perp = add(vector, negative(projection))
                x, y, z = decompose(perp, self.basis)
        
                # Rotate Perp
                newPerp = recompose(x, y, z, basis)
                
                # Now redefine plane from origin.
                newVector = add(newPerp, project(self.center, normalize(newPerp)))
                if Fix:
                    newVector = add(newVector, negative(newPerp))
                    
                # If the rotation changes which side of the plane is facing which way
                P = magnitude(perp)**2
                c = negative(self.center)
                if (dot(c, perp) < P) and (dot(c, newPerp) > P) or (dot(c, perp) > P) and (dot(c, newPerp) < P):
                    sign = not sign
                newVectors += [[newVector, sign]]
            newHitBoxes += [R3Region(newVectors)]
        self.hitBoxes = newHitBoxes
        newWireFrame = []
        for line in self.wireFrame:
            start, end = line
            
            offset = add(start, negative(self.center))
            x, y, z = decompose(offset, self.basis)
            newStart = add(recompose(x, y, z, basis), self.center)

            offset = add(end, negative(self.center))
            x, y, z = decompose(offset, self.basis)
            newEnd = add(recompose(x, y, z, basis), self.center)
            
            newWireFrame += [[newStart, newEnd]]
        self.wireFrame = newWireFrame
        self.basis = basis
    
