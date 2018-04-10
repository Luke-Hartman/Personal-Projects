import json
from R3Region import R3Region
from Hull import Hull

test = "Models/test.txt"
def getHull(filename):
    blenderInput = json.load(open(filename))
#    print blenderInput[0]
    regions = [R3Region(region) for region in blenderInput]
    print len(regions)
    regions = regions[1:2]
    print len(regions)
    regions[0].build()
    print regions[0].vectors
    #print regions[0]
    return Hull(regions)
    #return Hull([R3Region(region) for region in json.load(open(filename))])
