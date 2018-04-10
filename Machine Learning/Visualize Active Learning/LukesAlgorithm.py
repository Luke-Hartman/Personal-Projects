from random import random, sample
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestNeighbors

# Prevents oversampling along decision boundary of a single decision tree.
def ImprovedLukesGetBatch(X, Y, batchSize, samplesPerTree=10):
	newX = []
	for i in range(len(X)//samplesPerTree):
		newX += LukesGetBatch(X, Y, batchSize=samplesPerTree)
	return newX
	
# If batchSize is None, just returns the number of connected components
def LukesGetBatch(X, Y, batchSize=None, minDistance=0.1, decayRate=0.1, checkSize=1000):
    # Build decision tree
    size = len(X[0])
    clf = DecisionTreeClassifier(splitter="random")
    #clf = DecisionTreeClassifier()
    clf.fit(X, Y)
    tree = clf.tree_
    # Get graph of connected leaf nodes (This is different than the tree structure)
    class Leaf:
        def __init__(self, n, boundary):
            self.edges = [([], []) for i in range(size)]
            self.boundary = boundary
            distribution = tree.value[n][0]
            self.prediction = max(range(len(distribution)), key=lambda j: distribution[j])
            self.visited = False
            self.n = n
        def collides(self, other, feat):
            for i in range(size):
                if i == feat:
                    continue
                myBot, myTop = self.boundary[i]
                theirBot, theirTop = other.boundary[i]
                if myTop <= theirBot or theirTop <= myBot:
                    return False
            return True
        def __str__(self):
            return "Leaf %d: prediction: %d, boundary: %s" % (self.n, self.prediction, self.boundary)

    leaves = [None for i in range(tree.node_count)]
    def createLeaves(n, boundary):
        feat = tree.feature[n]
        if feat < 0: # Then it is a leaf
            leaves[n] = Leaf(n, boundary)
            return
        threshold = tree.threshold[n]
        bot, top = boundary[feat]
        # Go down left child
        leftBoundary = boundary[:]
        leftBoundary[feat] = (bot, threshold)
        createLeaves(tree.children_left[n], leftBoundary)
        # Right child
        rightBoundary = boundary[:]
        rightBoundary[feat] = (threshold, top)
        createLeaves(tree.children_right[n], rightBoundary)

    rootBoundary = [(0, 1) for i in range(size)]
    createLeaves(0, rootBoundary)

    # Make edges for the subtree
    def createEdges(n):
        feat = tree.feature[n]
        if feat < 0:
            return
        def collectLeft(m): # Collects all the leaves touching the left side of the split
            if tree.feature[m] < 0:
                return [leaves[m]]
            if tree.feature[m] == feat:
                return collectLeft(tree.children_right[m])
            return collectLeft(tree.children_left[m]) + collectLeft(tree.children_right[m])
        def collectRight(m):
            if tree.feature[m] < 0:
                return [leaves[m]]
            if tree.feature[m] == feat:
                return collectRight(tree.children_left[m])
            return collectRight(tree.children_left[m]) + collectRight(tree.children_right[m])
        left = collectLeft(tree.children_left[n])
        right = collectRight(tree.children_right[n])
        for l in left:
            for r in right:
                if l.collides(r, feat):
                    l.edges[feat][1].append(r)
                    r.edges[feat][0].append(l)
        # No real reason to do this in this order, but might as well
        createEdges(tree.children_left[n])
        createEdges(tree.children_right[n])
    createEdges(0)

    # Now traverse the graph to find how many connected components there are
    i = 0
    connectedComponents = [0 for i in range(clf.n_classes_)]
    boundaryInfo = []
    while i < tree.node_count:
        if leaves[i] is not None and leaves[i].visited is False:
            curr = leaves[i]
            componentPrediction = curr.prediction
            def visit(leaf):
                leaf.visited = True
                for feat, featureEdgeGroups in enumerate(leaf.edges): # A group for each feature
                    for b, boundaryGroup in enumerate(featureEdgeGroups): # 2 groups, top and bot
                        for node in boundaryGroup: # All the leaves it collides with along that boundary
                            if not node.visited:
                                if node.prediction == componentPrediction:
                                    visit(node)
                                else:
                                    volume = 1
                                    boundary = []
                                    for d in range(size):
                                        lBot, lTop = leaf.boundary[d]
                                        nBot, nTop = node.boundary[d]
                                        if d != feat:
                                            bot = max(lBot, nBot)
                                            top = min(lTop, nTop)
                                            boundary.append((bot, top))
                                            volume *= top - bot
                                        else: # Could just use b instead, but why error?
                                            if lBot == nTop:
                                                boundary.append(lBot)
                                            elif lTop == nBot:
                                                boundary.append(lTop)
                                            else:
                                                raise RuntimeError()
                                    boundaryInfo.append((feat, b, volume, boundary))
            visit(curr)
            connectedComponents[componentPrediction] += 1
        i += 1
    if batchSize is None:
        return connectedComponents # The connected components often have only a very small number of samples in them, I am not sure what I think of this yet
    # Build nearest neighbor classifier to efficiently get NearestNeighbors
    nn = NearestNeighbors()
    nn.fit(X)
    # Get integrated table for placing along boundary
    integrated = [0]
    for feat, b, volume, boundary in boundaryInfo:
        integrated.append(integrated[-1] + volume)
    integrated = integrated[1:]
    # Find batch
    batch = []
    while len(batch) < batchSize:
        added = False
        for i in range(checkSize):
            # Generate a random value somewhere in the decision space
            value = random()*integrated[-1]
            # Find which part of the boundary the point is on
            def binarySearch(mindex, maxdex):
                if mindex == maxdex:
                    return mindex
                middex = (mindex + maxdex)//2
                mid = integrated[middex]
                if value <= mid:
                    return binarySearch(mindex, middex)
                else:
                    return binarySearch(middex + 1, maxdex)
            index = binarySearch(0, len(integrated) - 1)
            # Now put the point somewhere on the boundary
            feat, b, volume, boundary = boundaryInfo[index]
            point = []
            for i in range(size):
                if i == feat:
                    point.append(boundary[i])
                else:
                    bot, top = boundary[i]
                    point.append((top - bot)*random() + bot)
            '''
            # Check if it is sufficiently far from other points
            if len(nn.radius_neighbors([point], radius=minDistance, return_distance=False)[0]) == 0:
                # Quickly make sure it isn't too close to any of the other points in the batch
                added = True
                for p in batch:
                    if sum((p[i] - point[i])*(p[i] - point[i]) for i in range(len(p))) <= minDistance:
                        added = False
                if added:
                    batch.append(point)
            '''
            batch.append(point)
            added = True
        if not added:
            minDistance *= 1 - decayRate
            print(minDistance)
    return sample(batch, batchSize)
